# floriday_supplier_client.OrderRequestsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_order_request_by_id**](OrderRequestsApi.md#get_order_request_by_id) | **GET** /order-requests/{orderRequestId} | sales-order:read - Returns the order request by id.
[**get_order_requests_by_sequence_number**](OrderRequestsApi.md#get_order_requests_by_sequence_number) | **GET** /order-requests/sync/{sequenceNumber} | sales-order:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 order requests starting from a specified sequence number.
[**get_order_requests_max_sequence**](OrderRequestsApi.md#get_order_requests_max_sequence) | **GET** /order-requests/current-max-sequence | sales-order:read - Returns the maximum sequence number found in order request.
[**set_order_request_accepted**](OrderRequestsApi.md#set_order_request_accepted) | **PATCH** /order-requests/{orderRequestId}/accept | sales-order:write - Accepts the order request.
[**set_order_request_rejected**](OrderRequestsApi.md#set_order_request_rejected) | **PATCH** /order-requests/{orderRequestId}/reject | sales-order:write - Rejects the order request.

# **get_order_request_by_id**
> OrderRequest get_order_request_by_id(order_request_id)

sales-order:read - Returns the order request by id.

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
api_instance = floriday_supplier_client.OrderRequestsApi(floriday_supplier_client.ApiClient(configuration))
order_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:read - Returns the order request by id.
    api_response = api_instance.get_order_request_by_id(order_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderRequestsApi->get_order_request_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_request_id** | [**str**](.md)|  | 

### Return type

[**OrderRequest**](OrderRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_requests_by_sequence_number**
> SyncResultOfOrderRequest get_order_requests_by_sequence_number(sequence_number, limit_result=limit_result)

sales-order:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 order requests starting from a specified sequence number.

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
api_instance = floriday_supplier_client.OrderRequestsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sales-order:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 order requests starting from a specified sequence number.
    api_response = api_instance.get_order_requests_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderRequestsApi->get_order_requests_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfOrderRequest**](SyncResultOfOrderRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_requests_max_sequence**
> int get_order_requests_max_sequence()

sales-order:read - Returns the maximum sequence number found in order request.

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
api_instance = floriday_supplier_client.OrderRequestsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # sales-order:read - Returns the maximum sequence number found in order request.
    api_response = api_instance.get_order_requests_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderRequestsApi->get_order_requests_max_sequence: %s\n" % e)
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

# **set_order_request_accepted**
> set_order_request_accepted(body, order_request_id)

sales-order:write - Accepts the order request.

Changes the `status` to ACCEPTED and creates a new sales order.

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
api_instance = floriday_supplier_client.OrderRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AcceptOrderRequest() # AcceptOrderRequest | 
order_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Accepts the order request.
    api_instance.set_order_request_accepted(body, order_request_id)
except ApiException as e:
    print("Exception when calling OrderRequestsApi->set_order_request_accepted: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AcceptOrderRequest**](AcceptOrderRequest.md)|  | 
 **order_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_order_request_rejected**
> set_order_request_rejected(body, order_request_id)

sales-order:write - Rejects the order request.

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
api_instance = floriday_supplier_client.OrderRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.RejectOrderRequest() # RejectOrderRequest | 
order_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Rejects the order request.
    api_instance.set_order_request_rejected(body, order_request_id)
except ApiException as e:
    print("Exception when calling OrderRequestsApi->set_order_request_rejected: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RejectOrderRequest**](RejectOrderRequest.md)|  | 
 **order_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

