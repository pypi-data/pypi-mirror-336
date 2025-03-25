# floriday_supplier_client.TradeItemRequestsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_trade_item_request_by_id**](TradeItemRequestsApi.md#get_trade_item_request_by_id) | **GET** /trade-item-requests/{tradeItemRequestId} | catalog:read - Returns a trade item request.
[**get_trade_item_requests_by_sequence_number**](TradeItemRequestsApi.md#get_trade_item_requests_by_sequence_number) | **GET** /trade-item-requests/sync/{sequenceNumber} | catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade item requests starting from a specified sequence number.
[**get_trade_item_requests_max_sequence**](TradeItemRequestsApi.md#get_trade_item_requests_max_sequence) | **GET** /trade-item-requests/current-max-sequence | catalog:read - Returns the maximum sequence number found in trade item requests.
[**set_trade_item_request_accepted**](TradeItemRequestsApi.md#set_trade_item_request_accepted) | **PATCH** /trade-item-requests/{tradeItemRequestId}/accept/{tradeItemId} | catalog:write - Accepts the trade item request.
[**set_trade_item_request_rejected**](TradeItemRequestsApi.md#set_trade_item_request_rejected) | **PATCH** /trade-item-requests/{tradeItemRequestId}/reject | catalog:write - Rejects the trade item request.

# **get_trade_item_request_by_id**
> TradeItemRequest get_trade_item_request_by_id(trade_item_request_id)

catalog:read - Returns a trade item request.

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
api_instance = floriday_supplier_client.TradeItemRequestsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns a trade item request.
    api_response = api_instance.get_trade_item_request_by_id(trade_item_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemRequestsApi->get_trade_item_request_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_request_id** | [**str**](.md)|  | 

### Return type

[**TradeItemRequest**](TradeItemRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_requests_by_sequence_number**
> SyncResultOfTradeItemRequest get_trade_item_requests_by_sequence_number(sequence_number, limit_result=limit_result)

catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade item requests starting from a specified sequence number.

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
api_instance = floriday_supplier_client.TradeItemRequestsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade item requests starting from a specified sequence number.
    api_response = api_instance.get_trade_item_requests_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemRequestsApi->get_trade_item_requests_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfTradeItemRequest**](SyncResultOfTradeItemRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_requests_max_sequence**
> int get_trade_item_requests_max_sequence()

catalog:read - Returns the maximum sequence number found in trade item requests.

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
api_instance = floriday_supplier_client.TradeItemRequestsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - Returns the maximum sequence number found in trade item requests.
    api_response = api_instance.get_trade_item_requests_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemRequestsApi->get_trade_item_requests_max_sequence: %s\n" % e)
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

# **set_trade_item_request_accepted**
> set_trade_item_request_accepted(trade_item_request_id, trade_item_id)

catalog:write - Accepts the trade item request.

Changes the `status` to ACCEPTED and sets the `tradeItemId`. The chosen trade item must be available for the customer and must contain the correct packing configuration

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
api_instance = floriday_supplier_client.TradeItemRequestsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Accepts the trade item request.
    api_instance.set_trade_item_request_accepted(trade_item_request_id, trade_item_id)
except ApiException as e:
    print("Exception when calling TradeItemRequestsApi->set_trade_item_request_accepted: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_request_id** | [**str**](.md)|  | 
 **trade_item_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_trade_item_request_rejected**
> set_trade_item_request_rejected(trade_item_request_id)

catalog:write - Rejects the trade item request.

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
api_instance = floriday_supplier_client.TradeItemRequestsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Rejects the trade item request.
    api_instance.set_trade_item_request_rejected(trade_item_request_id)
except ApiException as e:
    print("Exception when calling TradeItemRequestsApi->set_trade_item_request_rejected: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

