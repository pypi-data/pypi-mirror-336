# floriday_supplier_client.BlanketOrdersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_blanket_order**](BlanketOrdersApi.md#add_blanket_order) | **POST** /blanket-orders | contract:write - Creates a blanket order
[**delete_blanket_order**](BlanketOrdersApi.md#delete_blanket_order) | **DELETE** /blanket-orders/{blanketOrderId} | contract:write - Deletes a blanket order.
[**edit_blanket_order**](BlanketOrdersApi.md#edit_blanket_order) | **PUT** /blanket-orders/{blanketOrderId} | contract:write - Modifies an existing blanket order.
[**get_blanket_order_by_id**](BlanketOrdersApi.md#get_blanket_order_by_id) | **GET** /blanket-orders/{blanketOrderId} | contract:read - Returns a blanket order by id.
[**get_blanket_orders_by_sequence_number**](BlanketOrdersApi.md#get_blanket_orders_by_sequence_number) | **GET** /blanket-orders/sync/{sequenceNumber} | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contracts starting from a specified sequence number.
[**get_blanket_orders_max_sequence**](BlanketOrdersApi.md#get_blanket_orders_max_sequence) | **GET** /blanket-orders/current-max-sequence | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in blanket orders.
[**set_blanket_order_approved**](BlanketOrdersApi.md#set_blanket_order_approved) | **PATCH** /blanket-orders/{blanketOrderId}/approve | contract:write - Approves a blanket order

# **add_blanket_order**
> add_blanket_order(body)

contract:write - Creates a blanket order

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddBlanketOrder() # AddBlanketOrder | 

try:
    # contract:write - Creates a blanket order
    api_instance.add_blanket_order(body)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->add_blanket_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddBlanketOrder**](AddBlanketOrder.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_blanket_order**
> delete_blanket_order(blanket_order_id)

contract:write - Deletes a blanket order.

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
blanket_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Deletes a blanket order.
    api_instance.delete_blanket_order(blanket_order_id)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->delete_blanket_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **blanket_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_blanket_order**
> edit_blanket_order(body, blanket_order_id)

contract:write - Modifies an existing blanket order.

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditBlanketOrder() # EditBlanketOrder | 
blanket_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Modifies an existing blanket order.
    api_instance.edit_blanket_order(body, blanket_order_id)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->edit_blanket_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditBlanketOrder**](EditBlanketOrder.md)|  | 
 **blanket_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_blanket_order_by_id**
> BlanketOrder get_blanket_order_by_id(blanket_order_id)

contract:read - Returns a blanket order by id.

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
blanket_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:read - Returns a blanket order by id.
    api_response = api_instance.get_blanket_order_by_id(blanket_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->get_blanket_order_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **blanket_order_id** | [**str**](.md)|  | 

### Return type

[**BlanketOrder**](BlanketOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_blanket_orders_by_sequence_number**
> SyncResultOfBlanketOrder get_blanket_orders_by_sequence_number(sequence_number, limit_result=limit_result)

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contracts starting from a specified sequence number.

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contracts starting from a specified sequence number.
    api_response = api_instance.get_blanket_orders_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->get_blanket_orders_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfBlanketOrder**](SyncResultOfBlanketOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_blanket_orders_max_sequence**
> int get_blanket_orders_max_sequence()

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in blanket orders.

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in blanket orders.
    api_response = api_instance.get_blanket_orders_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->get_blanket_orders_max_sequence: %s\n" % e)
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

# **set_blanket_order_approved**
> set_blanket_order_approved(blanket_order_id)

contract:write - Approves a blanket order

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
api_instance = floriday_supplier_client.BlanketOrdersApi(floriday_supplier_client.ApiClient(configuration))
blanket_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Approves a blanket order
    api_instance.set_blanket_order_approved(blanket_order_id)
except ApiException as e:
    print("Exception when calling BlanketOrdersApi->set_blanket_order_approved: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **blanket_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

