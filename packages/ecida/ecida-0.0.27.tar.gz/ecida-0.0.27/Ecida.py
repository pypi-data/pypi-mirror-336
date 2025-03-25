import os
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import shutil
import logging


def isDeployed():
    flag_value = os.getenv("ECIDA_DEPLOY", "").lower()
    return flag_value == "true"


def now():
    return "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"


def convert_to_dns_name(string):
    # Convert the string to lowercase
    string = string.lower()

    # Replace non-alphanumeric characters with hyphens
    string = "".join("-" if not c.isalnum() else c for c in string)

    # Remove leading and trailing hyphens
    string = string.strip("-")

    # Replace multiple consecutive hyphens with a single hyphen
    string = "-".join(filter(None, string.split("-")))

    # Ensure the resulting string is not empty
    if not string:
        raise ValueError("Invalid string: Cannot convert to DNS name.")

    return string


def create_directory(directory_path):
    if os.path.exists(directory_path):
        logging.info(f"Deleting existing directory: {directory_path}")
        shutil.rmtree(directory_path)

    try:
        logging.info(f"Creating directory: {directory_path}")
        os.mkdir(directory_path)
    except OSError as e:
        logging.error(f"Failed to create directory: {directory_path}")
        logging.error(f"Error: {str(e)}")


class EcidaModule:
    def __init__(self, name, version, log_level=logging.INFO):
        # Configure logging with the provided log level
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        self._name = name
        self._version = version
        self._inputs = {}
        self._outputs = {}
        self._topics_envVars = {}
        self._topics_names = {}
        self._consumers = {}
        self._directories = {}
        self._description = ""
        self._producer = None
        self._initialized = False
        self._deployed = isDeployed()
        self._kafka_config = {}  # Add default empty dict for Kafka config
        logging.info(
            f"{name}:{version} is initialized with deployed = {self._deployed}"
        )

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def topics_envVars(self):
        return self._topics_envVars

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def directories(self):
        return self._directories

    @property
    def description(self):
        return self._description

    @name.setter
    def name(self, value):
        raise AttributeError("Attribute is read-only")

    @version.setter
    def version(self, value):
        raise AttributeError("Attribute is read-only")

    @version.setter
    def deployed(self, value):
        raise AttributeError("Attribute is read-only")

    def add_input(self, inp: str, type):
        self._inputs[inp] = type
        self._topics_envVars[inp] = "KAFKA_TOPIC_" + inp.upper()

    def add_output(self, out: str, type):
        self._outputs[out] = type
        self._topics_envVars[out] = "KAFKA_TOPIC_" + out.upper()

    def add_input_directory(self, inp: str):
        localPath = convert_to_dns_name(inp)
        self._inputs[inp] = "directory"
        self.directories[inp] = {}
        self.directories[inp]["localPath"] = localPath

    def add_output_directory(self, out: str):
        localPath = convert_to_dns_name(out)
        self._outputs[out] = "directory"
        self.directories[out] = {}
        self.directories[out]["localPath"] = localPath

    def add_input_from_git(self, name: str, git: str, path: str):
        self.add_input_directory(name)
        self.__add_git_to_directory(name, git, path)

    def add_output_to_git(self, name: str, git: str, path: str):
        self.add_output_directory(name)
        self.__add_git_to_directory(name, git, path)

    def add_description(self, description: str):
        self._description = description

    def get_path(self, name):
        if self._deployed:
            return "/" + self.directories[name]["localPath"]
        else:
            return "./" + self.directories[name]["localPath"]

    def __add_git_to_directory(self, name: str, git: str, path: str):
        self._directories[name]["source"] = git
        self._directories[name]["folder"] = path

    def to_yaml(self) -> str:
        return str(self._inputs) + "\n" + str(self._outputs)

    def set_kafka_config(self, config_dict):
        """
        Set Kafka consumer and producer configuration parameters.

        Args:
            config_dict (dict): Dictionary containing Kafka configuration parameters
                                like 'session.timeout.ms', 'heartbeat.interval.ms', etc.
        """
        self._kafka_config = config_dict
        logging.info(f"Kafka configuration updated: {config_dict}")
        return self

    def initialize(self):
        if self._deployed:
            isKafkaInput = False
            for _, value in self._inputs.items():
                if value != "directory":
                    isKafkaInput = True
            isKafkaOutput = False
            for _, value in self._outputs.items():
                if value != "directory":
                    isKafkaOutput = True

            if isKafkaInput or isKafkaOutput:
                self._KAFKA_BOOTSTRAP_SERVER = os.environ["KAFKA_BOOTSTRAP_SERVER"]
                self._KAFKA_SASL_MECHANISM = os.environ["KAFKA_SASL_MECHANISM"]
                self._KAFKA_SECURITY_PROTOCOL = os.environ["KAFKA_SECURITY_PROTOCOL"]
                self._KAFKA_USERNAME = os.environ["KAFKA_USERNAME"]
                self._KAFKA_PASSWORD = os.environ["KAFKA_PASSWORD"]
                self._KAFKA_GROUP_ID = os.environ["KAFKA_USERNAME"]
                self._KAFKA_CA_CERT_PATH = os.environ["KAFKA_CA_CERT_PATH"]

            for key, value in self._inputs.items():
                if value == "directory":
                    continue
                topicName = os.environ[self._topics_envVars[key]]
                self._topics_names[key] = topicName

                # Base consumer configuration
                consumer_config = {
                    "bootstrap_servers": self._KAFKA_BOOTSTRAP_SERVER,
                    "sasl_plain_username": self._KAFKA_USERNAME,
                    "sasl_plain_password": self._KAFKA_PASSWORD,
                    "sasl_mechanism": self._KAFKA_SASL_MECHANISM,
                    "security_protocol": self._KAFKA_SECURITY_PROTOCOL,
                    "group_id": self._KAFKA_GROUP_ID,
                    "ssl_cafile": self._KAFKA_CA_CERT_PATH,
                }

                # Apply any custom Kafka configuration
                for config_key, config_value in self._kafka_config.items():
                    consumer_config[config_key] = config_value

                consumer = KafkaConsumer(topicName, **consumer_config)
                self._consumers[key] = consumer

            if len(self._outputs) > 0 and isKafkaOutput:
                # Base producer configuration
                producer_config = {
                    "bootstrap_servers": self._KAFKA_BOOTSTRAP_SERVER,
                    "sasl_plain_username": self._KAFKA_USERNAME,
                    "sasl_plain_password": self._KAFKA_PASSWORD,
                    "sasl_mechanism": self._KAFKA_SASL_MECHANISM,
                    "security_protocol": self._KAFKA_SECURITY_PROTOCOL,
                    "ssl_cafile": self._KAFKA_CA_CERT_PATH,
                }

                # Apply relevant producer configs from kafka_config
                producer_keys = [
                    "batch_size",
                    "linger_ms",
                    "buffer_memory",
                    "max_request_size",
                ]
                for key in producer_keys:
                    if key in self._kafka_config:
                        producer_config[key] = self._kafka_config[key]

                self._producer = KafkaProducer(**producer_config)

            for key, value in self._outputs.items():
                if value == "directory":
                    continue
                topicName = os.environ[self._topics_envVars[key]]
                self._topics_names[key] = topicName

            self._initialized = True

        else:
            for output in self._outputs:
                if output in self._directories:
                    path = self.get_path(self._directories[output]["localPath"])
                    create_directory(path)

    def push(self, output_channel: str, message) -> bool:
        if self._deployed:
            if output_channel in self._outputs:
                self._producer.send(
                    self._topics_names[output_channel],
                    value=str(message).encode("utf-8"),
                )
                return True
            return False
        else:
            return print(f"{now()} {output_channel}: {message}")

    def pull(self, input_name, timeout_ms=30000):
        """
        Pull data from the specified input with a configurable timeout.

        Args:
            input_name (str): The name of the input to pull from
            timeout_ms (int): Timeout in milliseconds for the Kafka consumer poll

        Returns:
            str: The data pulled from the input
        """
        if self._deployed:
            if input_name in self._inputs:
                records = self._consumers[input_name].poll(timeout_ms=timeout_ms)
                for msg in records:
                    return msg.value.decode("utf-8")
            return None
        else:
            return input(f"{now()} {input_name}:")

    def enable_large_messages(self):
        """Allow sending and receiving larger messages than default."""
        self.set_kafka_config(
            {
                "auto_offset_reset": "earliest",
                "enable_auto_commit": True,
                "fetch_max_bytes": 104857600,  # 100MB max fetch size
                "max_partition_fetch_bytes": 104857600,  # 100MB max partition fetch
                "max_poll_records": 500,  # Process 500 messages per poll
                "max_poll_interval_ms": 300000,  # 5 minutes to avoid rebalancing
                "request_timeout_ms": 305000,  # Slightly higher than max_poll_interval
                "session_timeout_ms": 60000,  # 60 seconds timeout
                "heartbeat_interval_ms": 20000,  # Heartbeat every 20 seconds
            }
        )
