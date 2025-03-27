# V1Context


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection_id** | **str** | Collection Id. | [optional] 
**chunk_id** | **int** | Chunk Id. | [optional] 
**score** | **float** | Chunk score. | [optional] 
**content** | **str** | Content. | [optional] 

## Example

```python
from eval_studio_client.api.models.v1_context import V1Context

# TODO update the JSON string below
json = "{}"
# create an instance of V1Context from a JSON string
v1_context_instance = V1Context.from_json(json)
# print the JSON string representation of the object
print(V1Context.to_json())

# convert the object into a dict
v1_context_dict = v1_context_instance.to_dict()
# create an instance of V1Context from a dict
v1_context_from_dict = V1Context.from_dict(v1_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


