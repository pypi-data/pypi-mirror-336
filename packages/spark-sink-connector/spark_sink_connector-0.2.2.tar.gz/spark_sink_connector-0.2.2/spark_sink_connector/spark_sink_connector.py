import logging
import os
from typing import Callable, Optional

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import expr, col
from pyspark.sql.protobuf.functions import from_protobuf

from .enums import *
from .schema_helper import get_schemas_from_registry, process_data_with_schema_evolution, schema_id_udf
from .spark_sink_config import SparkSinkConfig


class SparkSinkConnector:
    """
    A connector for reading data from Kafka and writing to S3 in Delta or Hudi format.
    """

    def __init__(self, connector_mode: ConnectorMode, config: Optional[SparkSinkConfig] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize the SparkSinkConnector with configuration.

        Args:
            connector_mode: Whether to use streaming mode or batch mode
            config: Configuration object for the connector
            logger: Optional logger instance
        """
        self.config = config or SparkSinkConfig()
        self._setup_logger(logger)
        self.connector_mode = connector_mode
        self.dataframe = None
        self.writer = None
        self.spark_session = self._create_spark_session()

    def _setup_logger(self, logger: Optional[logging.Logger] = None):
        """Set up the logger for this class."""
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(
                format=self.config.logger_format,
                level=logging.INFO
            )

    def _create_spark_session(self) -> SparkSession:
        """
        Create and configure a Spark session.

        Returns:
            SparkSession: Configured Spark session

        Raises:
            Exception: If Spark session creation fails
        """
        try:
            spark_conf = SparkConf()
            spark_conf.set("spark.logLevel", "INFO")
            spark_conf.set("spark.appName", f"s3_sink_{os.path.basename(__file__)}")

            # S3 configuration
            spark_conf.set("spark.hadoop.fs.s3a.access.key", self.config.s3_access_key)
            spark_conf.set("spark.hadoop.fs.s3a.secret.key", self.config.s3_secret_key)
            spark_conf.set("spark.hadoop.fs.s3a.endpoint", self.config.s3_endpoint)
            spark_conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
            spark_conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            spark_conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

            # Spark SQL and Delta configuration
            spark_conf.set("spark.sql.session.timeZone", "Asia/Tehran")
            spark_conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            spark_conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

            # Packages
            spark_conf.set("spark.jars.packages", self.config.spark_jars)

            spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
            self.logger.info("✅ Spark session created successfully.")
            return spark
        except Exception as e:
            self.logger.error(f"❌ Failed to create Spark session: {e}")
            raise

    def read_from_kafka(self, kafka_topic: str = None) -> 'SparkSinkConnector':
        """
        Read data from Kafka topic.

        Args:
            kafka_topic: Kafka topic name

        Returns:
            self: For method chaining
        """
        kafka_options = {
            "kafka.bootstrap.servers": self.config.kafka_broker,
            "subscribe": kafka_topic or self.config.kafka_topic,
            "minOffsetsPerTrigger": self.config.min_offset,
            "maxOffsetsPerTrigger": self.config.max_offset,
            "failOnDataLoss": "false",
            "startingOffsets": self.config.starting_offsets,
            "kafkaConsumer.pollTimeoutMs": self.config.kafka_session_timeout,
            "kafka.request.timeout.ms": self.config.kafka_request_timeout,
            "kafka.session.timeout.ms": self.config.kafka_session_timeout,
        }
        self.logger.info(f"Kafka configurations are: ")
        self.logger.info(kafka_options)

        # Add authentication options if credentials are provided
        if self.config.kafka_user and self.config.kafka_password:
            kafka_options.update({
                "kafka.sasl.mechanism": "SCRAM-SHA-512",
                "kafka.security.protocol": "SASL_PLAINTEXT",
                "kafka.sasl.jaas.config": (
                    f"org.apache.kafka.common.security.scram.ScramLoginModule required "
                    f"username='{self.config.kafka_user}' password='{self.config.kafka_password}';"
                )
            })

        # Build the reader with all options
        reader = self.spark_session.readStream if self.connector_mode == ConnectorMode.STREAM else self.spark_session.read
        reader = reader.format("kafka")
        for key, value in kafka_options.items():
            reader = reader.option(key, value)

        self.dataframe = reader.load()
        self.logger.info(f"✅ Successfully read Kafka batch.")
        return self

    def get_dataframe(self) -> DataFrame:
        """
        Returns the Spark DataFrame.

        Returns:
            self.dataframe
        """
        return self.dataframe

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger.

        Returns:
            self.logger
        """
        return self.logger

    def set_dataframe(self, dataframe: DataFrame):
        """
        Sets the Spark DataFrame.

        Args:
            dataframe: Spark DataFrame
        """
        self.dataframe = dataframe

    def apply_schema_from_file(self, kind: SchemaKind, file_name: str, message_name: str) -> 'SparkSinkConnector':
        """
        Apply schema from a file to the DataFrame.

        Args:
            kind: Type of schema (AVRO or PROTOBUF)
            file_name: Path to the schema file
            message_name: Name of the message in the schema

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if kind == SchemaKind.PROTOBUF:
            self.dataframe = self.dataframe.select(
                from_protobuf("value", message_name, file_name).alias("event")
            )
            self.dataframe = self.dataframe.select("event.*")
            self.logger.info(f"✅ Applied Protobuf schema from file: {file_name}")
        else:
            self.logger.warning(f"⚠️ Schema kind {kind} not implemented for file-based schemas")

        return self

    def apply_schema_from_registry(self, kind: SchemaKind) -> 'SparkSinkConnector':
        """
        Apply schema from registry to the DataFrame.

        Args:
            kind: Type of schema (AVRO or PROTOBUF)

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if kind == SchemaKind.AVRO:
            # Extract schema ID from Kafka message
            self.dataframe = self.dataframe.withColumn("schema_id_bytes", expr("substring(value, 2, 4)"))
            self.dataframe = self.dataframe.withColumn("schema_id", schema_id_udf(col("schema_id_bytes")))
            self.dataframe = self.dataframe.withColumn("avro_payload", expr("substring(value, 6, length(value)-5)"))

            # Get unique schema IDs
            unique_schema_ids = [row["schema_id"] for row in self.dataframe.select("schema_id").distinct().collect()]
            record_count = self.dataframe.count()
            self.logger.info(
                f"✅ Successfully read Kafka batch. Loaded {record_count} records from Kafka "
                f"with {len(unique_schema_ids)} unique schema IDs"
            )

            # Fetch schemas and process data
            schemas = get_schemas_from_registry(
                schema_ids=unique_schema_ids,
                schema_registry_url=self.config.schema_registry_url,
                logger=self.logger
            )
            self.dataframe = process_data_with_schema_evolution(df=self.dataframe, schemas=schemas, logger=self.logger)
        else:
            self.logger.warning(f"⚠️ Schema kind {kind} not implemented for registry-based schemas")

        return self

    def transform(self, transformation_fn: Optional[Callable[[DataFrame], DataFrame]] = None) -> 'SparkSinkConnector':
        """
        Apply transformations to the DataFrame.

        Args:
            transformation_fn: Function that takes a DataFrame and returns a transformed DataFrame

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if transformation_fn:
            self.dataframe = transformation_fn(self.dataframe)
            self.logger.info("✅ Custom transformations applied to DataFrame")

        return self

    def write_delta_to_s3(self, partition_key: str, output_mode: ConnectorOutputMode,
                          bucket_name: str) -> 'SparkSinkConnector':
        """
        Configure writing data to S3 in Delta format.

        Args:
            partition_key: Column to partition data by
            output_mode: Output mode (append, upsert or overwrite)
            bucket_name: S3 bucket name

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        # Extract base name for paths
        bucket_name = bucket_name or self.config.s3_bucket_name
        base_name = bucket_name.replace('-bucket', '')
        checkpoint_location = f"s3a://{bucket_name}/checkpoints/{base_name}"
        output_path = f"s3a://{bucket_name}/{base_name}"

        if self.connector_mode == ConnectorMode.STREAM:
            self.writer = self.dataframe.writeStream \
                .format("delta") \
                .partitionBy(partition_key) \
                .outputMode(output_mode.value) \
                .trigger(availableNow=True) \
                .option("checkpointLocation", checkpoint_location) \
                .option("path", output_path)
        else:
            self.writer = self.dataframe.coalesce(1).write \
                .format("delta") \
                .partitionBy(partition_key) \
                .mode(output_mode.value) \
                .option("checkpointLocation", checkpoint_location) \
                .option("path", output_path)

        self.logger.info(f"✅ Configured Delta write to {output_path}")
        return self

    def write_hudi_to_s3(self,
                         partition_key: str,
                         output_mode: ConnectorOutputMode,
                         bucket_name: str,
                         hudi_options: dict[str,str]) -> 'SparkSinkConnector':
        """
        Configure writing data to S3 in Hudi format.

        Args:
            partition_key: Column to partition data by
            output_mode: Output mode (append, upsert or overwrite)
            bucket_name: S3 bucket name
            hudi_options: Hudi options in dictionary format

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if self.connector_mode == ConnectorMode.STREAM:
            hudi_base_path = f"s3a://{self.full_table_name}-bucket/{self.full_table_name}"
            self.dataframe.write \
                .format("hudi") \
                .partitionBy(partition_key) \
                .options(**hudi_options) \
                .mode(output_mode) \
                .save(hudi_base_path)
            self.logger.info(f"✅ Data written to {hudi_base_path} in Hudi format.")
        else:
            raise NotImplementedError

        return self

    def start(self) -> None:
        """
        Start the writing job and await termination.
        """
        if not self.writer:
            self.logger.error("❌ Writer not initialized. Call write_delta_to_s3() or write_hudi_to_s3() first.")
            raise ValueError("Writer not initialized")

        if self.connector_mode == ConnectorMode.STREAM:
            self.writer.start().awaitTermination()
        else:
            self.writer.save()
