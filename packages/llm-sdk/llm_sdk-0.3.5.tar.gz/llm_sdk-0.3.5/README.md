# LLM SDK (AI MODELS)

### What is LLM SDK ?
LLM SDK is an API wrapper designed to access and manage all available LLM models, including LLM, Multimodal, and Embedding models. It employs agents to automate the process of collecting information about available models, ensuring a comprehensive list of models is available. Despite the automation, human verification is required to ensure accuracy.

### Installation
`pip install llm-sdk`

### Usage
The LLM SDK provides a simple interface to interact with the API and retrieve information about models, providers, and model creators. Below is an example of how to use the SDK.

```python
from llm_sdk import ai_models

# Get a list of available models
available_models = ai_models.get_available_models(model_type_name="LLM", provider_name="OpenAI", is_verified=True)
for model in available_models:
    print(model.name)
```

```python
# Get a list of providers
providers = ai_models.get_providers(model_type_name="LLM")
for provider in providers:
    print(provider.name)
```
```python
# Get a list of model creators
model_creators = ai_models.get_model_creators(model_type_name="LLM")
for creator in model_creators:
    print(creator.name)
```
```python
# Get details of a specific model creator by ID
model_creator = ai_models.get_model_creator(creator_id=1)
print(model_creator.name)
```


### API Methods


* `get_available_models`: Retrieve a list of available models based on optional filters.

  ##### Filters:
  * `model_type_name` (Optional[str]): Filter by model type name.
  * `provider_name` (Optional[str]): Filter by provider name.
  * `is_verified` (Optional[bool]): Filter by verification status.


* `get_providers`: Retrieve a list of providers based on an optional model type filter.
  
  ##### Filters:
  * `model_type_name` (Optional[str]): Filter by model type name.


* `get_model_creators`: Retrieve a list of model creators based on an optional model type filter.

  ##### Filters:
    * `model_type_name` (Optional[str]): Filter by model type name.
 

* `get_model_creator`: Retrieve details of a specific model creator by their ID.

  ##### Parameters:
  * `creator_id` (int): The ID of the model creator.