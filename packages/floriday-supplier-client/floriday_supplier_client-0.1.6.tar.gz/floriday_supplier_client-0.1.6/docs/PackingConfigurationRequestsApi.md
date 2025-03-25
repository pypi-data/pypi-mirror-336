# floriday_supplier_client.PackingConfigurationRequestsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_packing_configuration_request_by_id**](PackingConfigurationRequestsApi.md#get_packing_configuration_request_by_id) | **GET** /packing-configuration-requests/{packingConfigurationRequestId} | catalog:read - Returns a packing configuration request.
[**get_packing_configuration_requests_by_sequence_number**](PackingConfigurationRequestsApi.md#get_packing_configuration_requests_by_sequence_number) | **GET** /packing-configuration-requests/sync/{sequenceNumber} | catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 packing configuration request starting from a specified sequence number.
[**get_packing_configuration_requests_max_sequence**](PackingConfigurationRequestsApi.md#get_packing_configuration_requests_max_sequence) | **GET** /packing-configuration-requests/current-max-sequence | catalog:read - Returns the maximum sequence number found in packing configuration request.
[**set_packing_configuration_request_accepted**](PackingConfigurationRequestsApi.md#set_packing_configuration_request_accepted) | **PATCH** /packing-configuration-requests/{packingConfigurationRequestId}/accept | catalog:write - Accepts the packing configuration request.
[**set_packing_configuration_request_rejected**](PackingConfigurationRequestsApi.md#set_packing_configuration_request_rejected) | **PATCH** /packing-configuration-requests/{packingConfigurationRequestId}/reject | catalog:write - Rejects the packing configuration request.

# **get_packing_configuration_request_by_id**
> PackingConfigurationRequest get_packing_configuration_request_by_id(packing_configuration_request_id)

catalog:read - Returns a packing configuration request.

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
api_instance = floriday_supplier_client.PackingConfigurationRequestsApi(floriday_supplier_client.ApiClient(configuration))
packing_configuration_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns a packing configuration request.
    api_response = api_instance.get_packing_configuration_request_by_id(packing_configuration_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackingConfigurationRequestsApi->get_packing_configuration_request_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **packing_configuration_request_id** | [**str**](.md)|  | 

### Return type

[**PackingConfigurationRequest**](PackingConfigurationRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_packing_configuration_requests_by_sequence_number**
> SyncResultOfPackingConfigurationRequest get_packing_configuration_requests_by_sequence_number(sequence_number, limit_result=limit_result)

catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 packing configuration request starting from a specified sequence number.

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
api_instance = floriday_supplier_client.PackingConfigurationRequestsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 packing configuration request starting from a specified sequence number.
    api_response = api_instance.get_packing_configuration_requests_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackingConfigurationRequestsApi->get_packing_configuration_requests_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfPackingConfigurationRequest**](SyncResultOfPackingConfigurationRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_packing_configuration_requests_max_sequence**
> int get_packing_configuration_requests_max_sequence()

catalog:read - Returns the maximum sequence number found in packing configuration request.

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
api_instance = floriday_supplier_client.PackingConfigurationRequestsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - Returns the maximum sequence number found in packing configuration request.
    api_response = api_instance.get_packing_configuration_requests_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackingConfigurationRequestsApi->get_packing_configuration_requests_max_sequence: %s\n" % e)
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

# **set_packing_configuration_request_accepted**
> set_packing_configuration_request_accepted(packing_configuration_request_id)

catalog:write - Accepts the packing configuration request.

Changes the `status` to ACCEPTED. The trade item must contain the packing configuration available for the customer.

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
api_instance = floriday_supplier_client.PackingConfigurationRequestsApi(floriday_supplier_client.ApiClient(configuration))
packing_configuration_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Accepts the packing configuration request.
    api_instance.set_packing_configuration_request_accepted(packing_configuration_request_id)
except ApiException as e:
    print("Exception when calling PackingConfigurationRequestsApi->set_packing_configuration_request_accepted: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **packing_configuration_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_packing_configuration_request_rejected**
> set_packing_configuration_request_rejected(packing_configuration_request_id)

catalog:write - Rejects the packing configuration request.

Changes the `status` to REJECTED.

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
api_instance = floriday_supplier_client.PackingConfigurationRequestsApi(floriday_supplier_client.ApiClient(configuration))
packing_configuration_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Rejects the packing configuration request.
    api_instance.set_packing_configuration_request_rejected(packing_configuration_request_id)
except ApiException as e:
    print("Exception when calling PackingConfigurationRequestsApi->set_packing_configuration_request_rejected: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **packing_configuration_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

