from pydantic import BaseModel, Field, PositiveFloat


class Meta(BaseModel):
    source_name: str
    hostname: str
    host_id: str


class Metric(BaseModel):
    name: str
    value: PositiveFloat
    units: str


class MetricModel(BaseModel):
    timestamp: int = Field(alias="ts")
    metric: Metric
    meta: Meta
