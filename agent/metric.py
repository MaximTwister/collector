class Metric:

    def __init__(self, name, value, units):
        self.name = name
        self.value = value
        self.units = units
        self.meta = {}

    def to_json(self):
        return {
            "metric": {
                "name": self.name,
                "value": self.value,
                "units": self.units,
            },
            "meta": self.meta
        }
