# floriday_supplier_client.DeliveryOrdersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_clock_delivery_order**](DeliveryOrdersApi.md#add_clock_delivery_order) | **POST** /delivery-orders/{deliveryOrderId}/auction | fulfillment:write - Create a delivery order for auction warehouse.
[**add_delivery_order_goods_movement**](DeliveryOrdersApi.md#add_delivery_order_goods_movement) | **POST** /delivery-orders/{deliveryOrderId}/goods-movement | fulfillment:write - Create a delivery order for external warehouse.
[**delete_clock_delivery_order**](DeliveryOrdersApi.md#delete_clock_delivery_order) | **DELETE** /delivery-orders/{deliveryOrderId}/auction | fulfillment:write - Delete a delivery order for auction.
[**delete_delivery_order_goods_movement**](DeliveryOrdersApi.md#delete_delivery_order_goods_movement) | **DELETE** /delivery-orders/{deliveryOrderId}/goods-movement | fulfillment:write - Delete a delivery order for goods movement.
[**get_delivery_order_by_id**](DeliveryOrdersApi.md#get_delivery_order_by_id) | **GET** /delivery-orders/{deliveryOrderId} | fulfillment:read - Returns a delivery order.
[**get_delivery_orders_by_sequence_number**](DeliveryOrdersApi.md#get_delivery_orders_by_sequence_number) | **GET** /delivery-orders/sync/{sequenceNumber} | fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 delivery orders starting from a specified sequence number.
[**get_delivery_orders_max_sequence**](DeliveryOrdersApi.md#get_delivery_orders_max_sequence) | **GET** /delivery-orders/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery orders.
[**get_tray_labels_as_pdf_by_id**](DeliveryOrdersApi.md#get_tray_labels_as_pdf_by_id) | **GET** /delivery-orders/{deliveryOrderId}/stickers | fulfillment:read - Returns tray stickers as pdf for a delivery order.

# **add_clock_delivery_order**
> add_clock_delivery_order(body, delivery_order_id)

fulfillment:write - Create a delivery order for auction warehouse.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.DeliveryOrderAuction() # DeliveryOrderAuction | 
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Create a delivery order for auction warehouse.
    api_instance.add_clock_delivery_order(body, delivery_order_id)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->add_clock_delivery_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeliveryOrderAuction**](DeliveryOrderAuction.md)|  | 
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_delivery_order_goods_movement**
> add_delivery_order_goods_movement(body, delivery_order_id)

fulfillment:write - Create a delivery order for external warehouse.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.DeliveryOrderGoodsMovement() # DeliveryOrderGoodsMovement | 
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Create a delivery order for external warehouse.
    api_instance.add_delivery_order_goods_movement(body, delivery_order_id)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->add_delivery_order_goods_movement: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeliveryOrderGoodsMovement**](DeliveryOrderGoodsMovement.md)|  | 
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_clock_delivery_order**
> delete_clock_delivery_order(delivery_order_id)

fulfillment:write - Delete a delivery order for auction.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Delete a delivery order for auction.
    api_instance.delete_clock_delivery_order(delivery_order_id)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->delete_clock_delivery_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_delivery_order_goods_movement**
> delete_delivery_order_goods_movement(delivery_order_id)

fulfillment:write - Delete a delivery order for goods movement.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Delete a delivery order for goods movement.
    api_instance.delete_delivery_order_goods_movement(delivery_order_id)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->delete_delivery_order_goods_movement: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_order_by_id**
> DeliveryOrder get_delivery_order_by_id(delivery_order_id)

fulfillment:read - Returns a delivery order.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns a delivery order.
    api_response = api_instance.get_delivery_order_by_id(delivery_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->get_delivery_order_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

[**DeliveryOrder**](DeliveryOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_orders_by_sequence_number**
> SyncResultOfDeliveryOrder get_delivery_orders_by_sequence_number(sequence_number, limit_result=limit_result)

fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 delivery orders starting from a specified sequence number.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 delivery orders starting from a specified sequence number.
    api_response = api_instance.get_delivery_orders_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->get_delivery_orders_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfDeliveryOrder**](SyncResultOfDeliveryOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_orders_max_sequence**
> int get_delivery_orders_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery orders.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery orders.
    api_response = api_instance.get_delivery_orders_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->get_delivery_orders_max_sequence: %s\n" % e)
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

# **get_tray_labels_as_pdf_by_id**
> str get_tray_labels_as_pdf_by_id(delivery_order_id)

fulfillment:read - Returns tray stickers as pdf for a delivery order.

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
api_instance = floriday_supplier_client.DeliveryOrdersApi(floriday_supplier_client.ApiClient(configuration))
delivery_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns tray stickers as pdf for a delivery order.
    api_response = api_instance.get_tray_labels_as_pdf_by_id(delivery_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryOrdersApi->get_tray_labels_as_pdf_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_order_id** | [**str**](.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

