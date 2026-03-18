from pydantic import BaseModel
from typing import Dict, List


class ConstraintConfig(BaseModel):
    need_kubernetes: bool = False
    low_ops_capacity: bool = False
    vendor_neutrality: bool = False


class EvaluateRequest(BaseModel):
    options: List[str]
    constraints: ConstraintConfig
    weights: Dict[str, float]