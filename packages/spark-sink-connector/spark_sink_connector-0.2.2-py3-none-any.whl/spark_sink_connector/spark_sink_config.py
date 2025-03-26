import os


#todo : extract data classes

class SparkSinkConfig:
    """Configuration container for SparkSinkConnector."""

    def __init__(self, **kwargs):
        # Kafka settings
        self.kafka_broker = kwargs.get('kafka_broker') or os.getenv("KAFKA_BROKER", "kafka.de.data.snapp.tech:9092")
        self.kafka_topic = kwargs.get('kafka_topic') or os.getenv("KAFKA_TOPIC")
        self.kafka_user = kwargs.get('kafka_user') or os.getenv("KAFKA_USER")
        self.kafka_password = kwargs.get('kafka_password') or os.getenv("KAFKA_PASSWORD")
        self.kafka_request_timeout = kwargs.get('kafka_request_timeout') or os.getenv("KAFKA_REQUEST_TIMEOUT", "30000")
        self.kafka_session_timeout = kwargs.get('kafka_session_timeout') or os.getenv("KAFKA_SESSION_TIMEOUT", "30000")
        self.min_offset = kwargs.get('min_offset') or os.getenv("MIN_OFFSET", "1")
        self.max_offset = kwargs.get('max_offset') or os.getenv("MAX_OFFSET", "2000000")
        self.starting_offsets = kwargs.get('starting_offsets') or os.getenv("STARTING_OFFSET", "earliest")

        # S3 settings
        self.s3_endpoint = kwargs.get('s3_endpoint') or "http://s3.teh-1.snappcloud.io"
        self.s3_access_key = kwargs.get('s3_access_key') or os.getenv("S3_ACCESS_KEY")
        self.s3_secret_key = kwargs.get('s3_secret_key') or os.getenv("S3_SECRET_KEY")
        self.s3_bucket_name = kwargs.get('s3_bucket_name') or os.getenv("S3_BUCKET_NAME")

        # Schema Registry settings
        self.schema_registry_url = kwargs.get('schema_registry_url') or os.environ.get("SCHEMA_REGISTRY_URL",
                                                                                       "http://schema-registry.de.data.snapp.tech:8081")

        # Spark settings
        self.spark_jars = kwargs.get('spark_jars') or (
            "org.apache.spark:spark-avro_2.12:3.5.1,"
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
            "org.apache.kafka:kafka-clients:3.9.0,"
            "org.apache.spark:spark-protobuf_2.12:3.5.1"
        )

        # Logging settings
        self.logger_format = kwargs.get('logger_format') or (
            "%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s"
        )
