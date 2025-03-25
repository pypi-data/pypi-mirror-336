# floriday_supplier_client.WarehouseProvidersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_fulfillment_orders_inbound_by_sequence_number**](WarehouseProvidersApi.md#get_fulfillment_orders_inbound_by_sequence_number) | **GET** /fulfillment-orders/inbound/sync/{sequenceNumber} | fulfillment:read - Returns a list of inbound fulfillment orders.
[**set_fulfillment_order_receipt**](WarehouseProvidersApi.md#set_fulfillment_order_receipt) | **PUT** /fulfillment-orders/{fulfillmentOrderId}/goods-receipt | fulfillment:write - Receive a inbound fulfillment order.

# **get_fulfillment_orders_inbound_by_sequence_number**
> SyncResultOfFulfillmentOrderInbound get_fulfillment_orders_inbound_by_sequence_number(sequence_number, limit_result=limit_result)

fulfillment:read - Returns a list of inbound fulfillment orders.

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
api_instance = floriday_supplier_client.WarehouseProvidersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - Returns a list of inbound fulfillment orders.
    api_response = api_instance.get_fulfillment_orders_inbound_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehouseProvidersApi->get_fulfillment_orders_inbound_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfFulfillmentOrderInbound**](SyncResultOfFulfillmentOrderInbound.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_fulfillment_order_receipt**
> set_fulfillment_order_receipt(body, fulfillment_order_id)

fulfillment:write - Receive a inbound fulfillment order.

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
api_instance = floriday_supplier_client.WarehouseProvidersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.GoodsReceipt() # GoodsReceipt | 
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Receive a inbound fulfillment order.
    api_instance.set_fulfillment_order_receipt(body, fulfillment_order_id)
except ApiException as e:
    print("Exception when calling WarehouseProvidersApi->set_fulfillment_order_receipt: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GoodsReceipt**](GoodsReceipt.md)|  | 
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

