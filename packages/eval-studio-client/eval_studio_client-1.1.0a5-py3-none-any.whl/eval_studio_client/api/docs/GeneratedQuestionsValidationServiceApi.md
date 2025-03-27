# eval_studio_client.api.GeneratedQuestionsValidationServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generated_questions_validation_service_validate_generated_questions**](GeneratedQuestionsValidationServiceApi.md#generated_questions_validation_service_validate_generated_questions) | **POST** /v1/{name}:validateGeneratedQuestions | 


# **generated_questions_validation_service_validate_generated_questions**
> V1Operation generated_questions_validation_service_validate_generated_questions(name, body)



### Example


```python
import eval_studio_client.api
from eval_studio_client.api.models.generated_questions_validation_service_validate_generated_questions_request import GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest
from eval_studio_client.api.models.v1_operation import V1Operation
from eval_studio_client.api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = eval_studio_client.api.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with eval_studio_client.api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = eval_studio_client.api.GeneratedQuestionsValidationServiceApi(api_client)
    name = 'name_example' # str | Required. The Test for which to generate TestCases.
    body = eval_studio_client.api.GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest() # GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest | 

    try:
        api_response = api_instance.generated_questions_validation_service_validate_generated_questions(name, body)
        print("The response of GeneratedQuestionsValidationServiceApi->generated_questions_validation_service_validate_generated_questions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeneratedQuestionsValidationServiceApi->generated_questions_validation_service_validate_generated_questions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Required. The Test for which to generate TestCases. | 
 **body** | [**GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest**](GeneratedQuestionsValidationServiceValidateGeneratedQuestionsRequest.md)|  | 

### Return type

[**V1Operation**](V1Operation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

