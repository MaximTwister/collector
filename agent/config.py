from ruamel.yaml import YAML


class AgentConfig:

    source_name = None
    interval = None
    cpu = False
    memory = False
    host_identificator = 0
    agent_yaml = YAML()
    config = {}

    def __init__(self, configuration_file):
        self.__config_file = configuration_file
        self.parse_config()

    def load_config_from_yaml(self) -> dict:
        with open(self.__config_file, "r") as f:
            return self.agent_yaml.load(f)

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
            "host_identificator": self.transform_identificator
        }

        transformator = transformation_mapper.get(key, None)

        if transformator:
            return transformator(value)
        else:
            return value

    # TODO write transform_interval(suffix <s> suffix <m> suffix <h>)
    # TODO write transform_identificator(if value: 0 -> uuid.uuid4)
    # TODO load_config_to_yaml to save config with <host_identificator>


ac = AgentConfig("./agent/configs/agent.yaml")
