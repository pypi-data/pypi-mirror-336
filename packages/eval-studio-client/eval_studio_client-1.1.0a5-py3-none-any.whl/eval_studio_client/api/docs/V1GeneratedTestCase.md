# V1GeneratedTestCase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_case** | [**V1TestCase**](V1TestCase.md) |  | [optional] 
**context** | [**List[V1Context]**](V1Context.md) | Context used for test_case generation. | [optional] 

## Example

```python
from eval_studio_client.api.models.v1_generated_test_case import V1GeneratedTestCase

# TODO update the JSON string below
json = "{}"
# create an instance of V1GeneratedTestCase from a JSON string
v1_generated_test_case_instance = V1GeneratedTestCase.from_json(json)
# print the JSON string representation of the object
print(V1GeneratedTestCase.to_json())

# convert the object into a dict
v1_generated_test_case_dict = v1_generated_test_case_instance.to_dict()
# create an instance of V1GeneratedTestCase from a dict
v1_generated_test_case_from_dict = V1GeneratedTestCase.from_dict(v1_generated_test_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


