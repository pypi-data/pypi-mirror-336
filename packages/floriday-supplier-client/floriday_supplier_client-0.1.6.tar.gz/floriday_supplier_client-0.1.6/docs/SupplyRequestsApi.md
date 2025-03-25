# floriday_supplier_client.SupplyRequestsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_supply_request_by_id**](SupplyRequestsApi.md#get_supply_request_by_id) | **GET** /supply-requests/{supplyRequestId} | supply:read - Returns a supply request.
[**get_supply_requests_by_sequence_number**](SupplyRequestsApi.md#get_supply_requests_by_sequence_number) | **GET** /supply-requests/sync/{sequenceNumber} | supply:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 supply requests starting from a specified sequence number.
[**get_supply_requests_max_sequence**](SupplyRequestsApi.md#get_supply_requests_max_sequence) | **GET** /supply-requests/current-max-sequence | supply:read - Returns the maximum sequence number found in supply requests.
[**set_supply_request_line_accepted**](SupplyRequestsApi.md#set_supply_request_line_accepted) | **PATCH** /supply-requests/line/{supplyRequestLineId}/accept | supply:write - Accepts the supply request line.
[**set_supply_request_line_rejected**](SupplyRequestsApi.md#set_supply_request_line_rejected) | **PATCH** /supply-requests/line/{supplyRequestLineId}/reject | supply:write - Rejects the supply request line.

# **get_supply_request_by_id**
> SupplyRequest get_supply_request_by_id(supply_request_id)

supply:read - Returns a supply request.

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
api_instance = floriday_supplier_client.SupplyRequestsApi(floriday_supplier_client.ApiClient(configuration))
supply_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a supply request.
    api_response = api_instance.get_supply_request_by_id(supply_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SupplyRequestsApi->get_supply_request_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_request_id** | [**str**](.md)|  | 

### Return type

[**SupplyRequest**](SupplyRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_requests_by_sequence_number**
> SyncResultOfSupplyRequest get_supply_requests_by_sequence_number(sequence_number, limit_result=limit_result)

supply:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 supply requests starting from a specified sequence number.

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
api_instance = floriday_supplier_client.SupplyRequestsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 supply requests starting from a specified sequence number.
    api_response = api_instance.get_supply_requests_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SupplyRequestsApi->get_supply_requests_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfSupplyRequest**](SyncResultOfSupplyRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_requests_max_sequence**
> int get_supply_requests_max_sequence()

supply:read - Returns the maximum sequence number found in supply requests.

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
api_instance = floriday_supplier_client.SupplyRequestsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - Returns the maximum sequence number found in supply requests.
    api_response = api_instance.get_supply_requests_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SupplyRequestsApi->get_supply_requests_max_sequence: %s\n" % e)
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

# **set_supply_request_line_accepted**
> set_supply_request_line_accepted(body, supply_request_line_id)

supply:write - Accepts the supply request line.

Changes the `status` to ACCEPTED and creates a new supplyLine in a new or existing customerOffer.

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
api_instance = floriday_supplier_client.SupplyRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AcceptSupplyRequestLine() # AcceptSupplyRequestLine | 
supply_request_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Accepts the supply request line.
    api_instance.set_supply_request_line_accepted(body, supply_request_line_id)
except ApiException as e:
    print("Exception when calling SupplyRequestsApi->set_supply_request_line_accepted: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AcceptSupplyRequestLine**](AcceptSupplyRequestLine.md)|  | 
 **supply_request_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_supply_request_line_rejected**
> set_supply_request_line_rejected(body, supply_request_line_id)

supply:write - Rejects the supply request line.

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
api_instance = floriday_supplier_client.SupplyRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = 'body_example' # str | 
supply_request_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Rejects the supply request line.
    api_instance.set_supply_request_line_rejected(body, supply_request_line_id)
except ApiException as e:
    print("Exception when calling SupplyRequestsApi->set_supply_request_line_rejected: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)|  | 
 **supply_request_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

