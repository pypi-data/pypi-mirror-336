from typing import Optional, List
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class MetricTypeBase(FromCamelCaseBaseModel):
    name: str
    criteria: Optional[str] = None
    evaluation_steps: Optional[List[str]] = None

class MetricType(MetricTypeBase):
    id: str
    organization_id: str
    created_at: str
    deleted_at: Optional[str] = None