import uuid
import socket

from ruamel.yaml import YAML

from metric import Meta


class AgentConfig:

    source_name = None
    interval = None
    cpu = False
    memory = False
    hostname = socket.gethostname()
    host_id = 0
    agent_yaml = YAML()
    config = {}

    def __init__(self, configuration_file):
        self.__config_file = configuration_file
        self.parse_config()
        self.meta: Meta = self.create_meta_object()

    def load_config_from_yaml(self) -> dict:
        with open(self.__config_file, "r") as f:
            return self.agent_yaml.load(f)

    def load_config_to_yaml(self, config):
        with open(self.__config_file, "w") as f:
            self.agent_yaml.dump(config, f)

    def parse_config(self):
        class_variables = AgentConfig.__dict__.keys()
        self.config = self.load_config_from_yaml()
        for key, value in self.config.items():
            if key in class_variables:
                value = self.transform_values(key, value)
                setattr(AgentConfig, key, value)

    def transform_values(self, key, value):
        transformation_mapper = {
            "interval": self.transform_interval,
            "host_id": self.transform_host_id,
        }

        transformator = transformation_mapper.get(key, None)

        if transformator:
            return transformator(value)
        else:
            return value

    def transform_host_id(self, value) -> str:
        if value != 0:
            return value
        else:
            _uuid = str(uuid.uuid4())
            self.config["host_id"] = _uuid
            self.load_config_to_yaml(self.config)
            return _uuid

    @staticmethod
    def transform_interval(value: str) -> int:
        multipliers = {"s": 1, "m": 60, "h": 3600}
        SUFFIX_INDEX = -1

        units = value[SUFFIX_INDEX]
        interval_value = value[:SUFFIX_INDEX]

        if not isinstance(interval_value, str) and not interval_value.isdigit():
            raise TypeError(f"err: wrong type for interval: {value}")

        multiplier = multipliers.get(units)
        return int(interval_value) * multiplier

    def create_meta_object(self) -> Meta:
        meta_kwargs = {
            "source_name": self.source_name,
            "hostname": self.hostname,
            "host_id": self.host_id
        }
        return Meta.parse_obj(meta_kwargs)
