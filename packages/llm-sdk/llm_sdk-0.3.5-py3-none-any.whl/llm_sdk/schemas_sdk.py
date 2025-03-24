from pydantic import BaseModel
from typing import Optional


class ProviderModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    logo: Optional[str]
    req_config_params: Optional[dict]


class ModelCreatorModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    logo: Optional[str]


class ModelTypeModel(BaseModel):
    id: int
    name: str
    description: Optional[str]


class AvailableModelModel(BaseModel):
    id: int
    provider: ProviderModel
    creator: ModelCreatorModel
    model_type: ModelTypeModel
    name: str
    req_config_params: Optional[dict]
    model_name: Optional[str]
    model_version: Optional[str]
    is_verified: bool
    is_primary: bool
    cost_input_token: float
    cost_output_token: float
