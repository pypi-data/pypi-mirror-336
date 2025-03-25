# floriday_supplier_client.SalesOrdersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_sales_order**](SalesOrdersApi.md#add_sales_order) | **POST** /sales-orders | sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.
[**add_sales_order_external_integration**](SalesOrdersApi.md#add_sales_order_external_integration) | **POST** /sales-orders/external-integration | sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.
[**get_sales_order_by_id**](SalesOrdersApi.md#get_sales_order_by_id) | **GET** /sales-orders/{salesOrderId} | sales-order:read - Returns a sales order.
[**get_sales_order_by_id_and_version**](SalesOrdersApi.md#get_sales_order_by_id_and_version) | **GET** /sales-orders/{salesOrderId}/version | sales-order:read - Returns the sales order by ID and version.
[**get_sales_orders**](SalesOrdersApi.md#get_sales_orders) | **GET** /sales-orders | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns sales orders.
[**get_sales_orders_by_sequence_number**](SalesOrdersApi.md#get_sales_orders_by_sequence_number) | **GET** /sales-orders/sync/{sequenceNumber} | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales orders starting from a specified sequence number.
[**get_sales_orders_max_sequence**](SalesOrdersApi.md#get_sales_orders_max_sequence) | **GET** /sales-orders/current-max-sequence | sales-order:read - Returns the maximum sequence number found in sales orders.
[**set_sales_order_cancelled**](SalesOrdersApi.md#set_sales_order_cancelled) | **PATCH** /sales-orders/{salesOrderId}/cancel | sales-order:write - Cancel a sales order that is still in status ACCEPTED.
[**set_sales_order_committed**](SalesOrdersApi.md#set_sales_order_committed) | **PATCH** /sales-orders/{salesOrderId}/commit | sales-order:write - Commit a sales order that is still in status ACCEPTED.

# **add_sales_order**
> add_sales_order(body)

sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.

Creates a new sales order with a supply reference

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SalesOrderRequest() # SalesOrderRequest | 

try:
    # sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.
    api_instance.add_sales_order(body)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->add_sales_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SalesOrderRequest**](SalesOrderRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sales_order_external_integration**
> add_sales_order_external_integration(body)

sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.

Creates a new sales order without a supply line or blanket order reference.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SalesOrderExternalIntegrationRequest() # SalesOrderExternalIntegrationRequest | 

try:
    # sales-order:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a new sales order.
    api_instance.add_sales_order_external_integration(body)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->add_sales_order_external_integration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SalesOrderExternalIntegrationRequest**](SalesOrderExternalIntegrationRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_order_by_id**
> SalesOrder get_sales_order_by_id(sales_order_id)

sales-order:read - Returns a sales order.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:read - Returns a sales order.
    api_response = api_instance.get_sales_order_by_id(sales_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->get_sales_order_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 

### Return type

[**SalesOrder**](SalesOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_order_by_id_and_version**
> SalesOrderVersion get_sales_order_by_id_and_version(sales_order_id, sales_order_version)

sales-order:read - Returns the sales order by ID and version.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
sales_order_version = 56 # int | 

try:
    # sales-order:read - Returns the sales order by ID and version.
    api_response = api_instance.get_sales_order_by_id_and_version(sales_order_id, sales_order_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->get_sales_order_by_id_and_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 
 **sales_order_version** | **int**|  | 

### Return type

[**SalesOrderVersion**](SalesOrderVersion.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_orders**
> list[SalesOrder] get_sales_orders(start_date_time=start_date_time, end_date_time=end_date_time, trade_instrument=trade_instrument, sequence=sequence, limit_result=limit_result)

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns sales orders.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
start_date_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
end_date_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
trade_instrument = 'trade_instrument_example' # str |  (optional)
sequence = 789 # int |  (optional)
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns sales orders.
    api_response = api_instance.get_sales_orders(start_date_time=start_date_time, end_date_time=end_date_time, trade_instrument=trade_instrument, sequence=sequence, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->get_sales_orders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date_time** | **datetime**|  | [optional] 
 **end_date_time** | **datetime**|  | [optional] 
 **trade_instrument** | **str**|  | [optional] 
 **sequence** | **int**|  | [optional] 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**list[SalesOrder]**](SalesOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_orders_by_sequence_number**
> SyncResultOfSalesOrder get_sales_orders_by_sequence_number(sequence_number, limit_result=limit_result)

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales orders starting from a specified sequence number.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales orders starting from a specified sequence number.
    api_response = api_instance.get_sales_orders_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->get_sales_orders_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfSalesOrder**](SyncResultOfSalesOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_orders_max_sequence**
> int get_sales_orders_max_sequence()

sales-order:read - Returns the maximum sequence number found in sales orders.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # sales-order:read - Returns the maximum sequence number found in sales orders.
    api_response = api_instance.get_sales_orders_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->get_sales_orders_max_sequence: %s\n" % e)
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

# **set_sales_order_cancelled**
> set_sales_order_cancelled(sales_order_id)

sales-order:write - Cancel a sales order that is still in status ACCEPTED.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Cancel a sales order that is still in status ACCEPTED.
    api_instance.set_sales_order_cancelled(sales_order_id)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->set_sales_order_cancelled: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_sales_order_committed**
> set_sales_order_committed(sales_order_id)

sales-order:write - Commit a sales order that is still in status ACCEPTED.

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
api_instance = floriday_supplier_client.SalesOrdersApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Commit a sales order that is still in status ACCEPTED.
    api_instance.set_sales_order_committed(sales_order_id)
except ApiException as e:
    print("Exception when calling SalesOrdersApi->set_sales_order_committed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

