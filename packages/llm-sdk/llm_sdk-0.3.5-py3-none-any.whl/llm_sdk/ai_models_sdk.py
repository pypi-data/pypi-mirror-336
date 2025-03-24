import requests
from typing import List, Optional
from pydantic import parse_obj_as
from .schemas_sdk import AvailableModelModel, ProviderModel, ModelCreatorModel, ModelTypeModel


class ModelsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_available_models(
            self, stage_name: str,  model_type_name: Optional[str] = None, provider_name: Optional[str] = None,
            is_verified: Optional[bool] = None, model_type_id: Optional[int] = None, provider_id: Optional[int] = None,
            creator_id: Optional[int] = None, is_primary: Optional[bool] = None, name: Optional[str] = None
    ) -> List[AvailableModelModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if provider_name:
            params['provider_name'] = provider_name
        if is_verified is not None:
            params['is_verified'] = str(is_verified).lower()
        if is_primary is not None:
            params['is_primary'] = str(is_primary).lower()
        if model_type_id:
            params['model_type_id'] = model_type_id
        if provider_id:
            params['provider_id'] = provider_id
        if creator_id:
            params['creator_id'] = creator_id
        if name:
            params['name'] = name
        response = requests.get(f"{self.base_url}/available-models/", params=params)
        response.raise_for_status()
        return parse_obj_as(List[AvailableModelModel], response.json())

    def get_available_model(self, available_model_id: int) -> AvailableModelModel:
        response = requests.get(f"{self.base_url}/available-models/{available_model_id}")
        response.raise_for_status()
        return parse_obj_as(AvailableModelModel, response.json())

    def get_providers(self, stage_name: str, model_type_name: Optional[str] = None,
                      model_type_id: Optional[str] = None) -> List[ProviderModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id
        response = requests.get(f"{self.base_url}/providers/", params=params)
        response.raise_for_status()
        return parse_obj_as(List[ProviderModel], response.json())

    def get_model_creators(self, stage_name: str, model_type_name: Optional[str] = None,
                           model_type_id: Optional[str] = None) -> List[ModelCreatorModel]:
        params = {'stage_name': stage_name}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if model_type_id:
            params['model_type_id'] = model_type_id
        response = requests.get(f"{self.base_url}/model-creators/", params=params)
        response.raise_for_status()
        return parse_obj_as(List[ModelCreatorModel], response.json())

    def get_model_types(self) -> List[ModelTypeModel]:
        response = requests.get(f"{self.base_url}/model-types/")
        response.raise_for_status()
        return parse_obj_as(List[ModelTypeModel], response.json())

    def get_model_creator(self, creator_id: int) -> ModelCreatorModel:
        response = requests.get(f"{self.base_url}/model-creators/{creator_id}")
        response.raise_for_status()
        return parse_obj_as(ModelCreatorModel, response.json())


ai_models = ModelsAPI('http://ai-model-lbalancer-24mar-2142272186.us-east-1.elb.amazonaws.com:8000')
