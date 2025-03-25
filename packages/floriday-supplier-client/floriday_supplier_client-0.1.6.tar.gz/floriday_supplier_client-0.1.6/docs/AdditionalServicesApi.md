# floriday_supplier_client.AdditionalServicesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_additional_service_by_id**](AdditionalServicesApi.md#get_additional_service_by_id) | **GET** /additional-services/{additionalServiceId} | catalog:read - Returns an additional service.
[**get_additional_service_by_sequence_number**](AdditionalServicesApi.md#get_additional_service_by_sequence_number) | **GET** /additional-services/sync/{sequenceNumber} | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 additional services starting from a specified sequence number.
[**get_additional_services**](AdditionalServicesApi.md#get_additional_services) | **GET** /additional-services | catalog:read - Returns overview of additional services.
[**get_additional_services_max_sequence**](AdditionalServicesApi.md#get_additional_services_max_sequence) | **GET** /additional-services/current-max-sequence | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in additional services.

# **get_additional_service_by_id**
> AdditionalService get_additional_service_by_id(additional_service_id)

catalog:read - Returns an additional service.

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
api_instance = floriday_supplier_client.AdditionalServicesApi(floriday_supplier_client.ApiClient(configuration))
additional_service_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns an additional service.
    api_response = api_instance.get_additional_service_by_id(additional_service_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdditionalServicesApi->get_additional_service_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **additional_service_id** | [**str**](.md)|  | 

### Return type

[**AdditionalService**](AdditionalService.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_service_by_sequence_number**
> SyncResultOfAdditionalService get_additional_service_by_sequence_number(sequence_number, limit=limit)

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 additional services starting from a specified sequence number.

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
api_instance = floriday_supplier_client.AdditionalServicesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 additional services starting from a specified sequence number.
    api_response = api_instance.get_additional_service_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdditionalServicesApi->get_additional_service_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfAdditionalService**](SyncResultOfAdditionalService.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_services**
> list[AdditionalService] get_additional_services()

catalog:read - Returns overview of additional services.

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
api_instance = floriday_supplier_client.AdditionalServicesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - Returns overview of additional services.
    api_response = api_instance.get_additional_services()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdditionalServicesApi->get_additional_services: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[AdditionalService]**](AdditionalService.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_services_max_sequence**
> int get_additional_services_max_sequence()

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in additional services.

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
api_instance = floriday_supplier_client.AdditionalServicesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in additional services.
    api_response = api_instance.get_additional_services_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdditionalServicesApi->get_additional_services_max_sequence: %s\n" % e)
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

