from typing import Optional

from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class TestBase(FromCamelCaseBaseModel):
    name: str
    type: str
    product_id: str
    ground_truth_uri: Optional[str] = None
    uri: Optional[str] = None

class Test(TestBase):
    id: str
    created_at: str
    deleted_at: Optional[str] = None