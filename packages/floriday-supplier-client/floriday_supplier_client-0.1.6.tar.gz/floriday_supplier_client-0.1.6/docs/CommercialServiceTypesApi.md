# floriday_supplier_client.CommercialServiceTypesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_commercial_service_types**](CommercialServiceTypesApi.md#get_commercial_service_types) | **GET** /commercial-service-types | catalog:read - Returns overview of commercial service types
[**get_commercial_service_types_by_sequence_number**](CommercialServiceTypesApi.md#get_commercial_service_types_by_sequence_number) | **GET** /commercial-service-types/sync/{sequenceNumber} | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 commercial service types starting from a specified sequence number.
[**get_commercial_service_types_max_sequence**](CommercialServiceTypesApi.md#get_commercial_service_types_max_sequence) | **GET** /commercial-service-types/current-max-sequence | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in commercial service types.

# **get_commercial_service_types**
> list[CommercialServiceType] get_commercial_service_types(language_code=language_code)

catalog:read - Returns overview of commercial service types

### Example
```python
from __future__ import print_function
import time
import floriday_supplier_client
from floriday_supplier_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: JWT Token
configuration = floriday_supplier_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure API key authorization: X-Api-Key
configuration = floriday_supplier_client.Configuration()
configuration.api_key['X-Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = floriday_supplier_client.CommercialServiceTypesApi(floriday_supplier_client.ApiClient(configuration))
language_code = 'language_code_example' # str |  (optional)

try:
    # catalog:read - Returns overview of commercial service types
    api_response = api_instance.get_commercial_service_types(language_code=language_code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CommercialServiceTypesApi->get_commercial_service_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **language_code** | **str**|  | [optional] 

### Return type

[**list[CommercialServiceType]**](CommercialServiceType.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_commercial_service_types_by_sequence_number**
> SyncResultOfCommercialServiceType get_commercial_service_types_by_sequence_number(sequence_number, limit=limit)

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 commercial service types starting from a specified sequence number.

**Synchronization endpoint** Fetches the succeeding modified records (including deleted records) based on `Limit` and the given `SequenceNumber`.  **Note** Your data is up to date when your given `SequenceNumber` is equal to the received `MaximumSequenceNumber`.

### Example
```python
from __future__ import print_function
import time
import floriday_supplier_client
from floriday_supplier_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: JWT Token
configuration = floriday_supplier_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure API key authorization: X-Api-Key
configuration = floriday_supplier_client.Configuration()
configuration.api_key['X-Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = floriday_supplier_client.CommercialServiceTypesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 commercial service types starting from a specified sequence number.
    api_response = api_instance.get_commercial_service_types_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CommercialServiceTypesApi->get_commercial_service_types_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfCommercialServiceType**](SyncResultOfCommercialServiceType.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_commercial_service_types_max_sequence**
> int get_commercial_service_types_max_sequence()

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in commercial service types.

### Example
```python
from __future__ import print_function
import time
import floriday_supplier_client
from floriday_supplier_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: JWT Token
configuration = floriday_supplier_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure API key authorization: X-Api-Key
configuration = floriday_supplier_client.Configuration()
configuration.api_key['X-Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = floriday_supplier_client.CommercialServiceTypesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in commercial service types.
    api_response = api_instance.get_commercial_service_types_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CommercialServiceTypesApi->get_commercial_service_types_max_sequence: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**int**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

