# GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation** | **str** | Required. The Operation processing this question validation process. | [optional] 
**test_cases** | [**List[V1GeneratedTestCase]**](V1GeneratedTestCase.md) | Required. Generated Test Cases, i.e., Test cases with context that was used for their generation. | [optional] 

## Example

```python
from eval_studio_client.api.models.generated_questions_validation_service_validate_generated_questions_request import GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest from a JSON string
generated_questions_validation_service_validate_generated_questions_request_instance = GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest.from_json(json)
# print the JSON string representation of the object
print(GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest.to_json())

# convert the object into a dict
generated_questions_validation_service_validate_generated_questions_request_dict = generated_questions_validation_service_validate_generated_questions_request_instance.to_dict()
# create an instance of GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest from a dict
generated_questions_validation_service_validate_generated_questions_request_from_dict = GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest.from_dict(generated_questions_validation_service_validate_generated_questions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


