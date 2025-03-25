# floriday_supplier_client.PlantPassportsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_plant_passport_pdf**](PlantPassportsApi.md#get_plant_passport_pdf) | **POST** /plant-passports | fulfillment:read - Returns the plant passport PDF for the BatchIds.
[**get_plant_passport_pdf_by_sales_channel_order_id**](PlantPassportsApi.md#get_plant_passport_pdf_by_sales_channel_order_id) | **GET** /plant-passports/by-sales-channel-order-id/{salesChannelOrderId} | fulfillment:read - Returns plant passport PDF for the sales order.
[**get_plant_passport_pdf_by_sales_order_id**](PlantPassportsApi.md#get_plant_passport_pdf_by_sales_order_id) | **GET** /plant-passports/by-sales-order-id/{salesOrderId} | fulfillment:read - Returns plant passport PDF for the sales order.

# **get_plant_passport_pdf**
> str get_plant_passport_pdf(body)

fulfillment:read - Returns the plant passport PDF for the BatchIds.

Uses HTTP POST to prevent a limit on the query URL.

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
api_instance = floriday_supplier_client.PlantPassportsApi(floriday_supplier_client.ApiClient(configuration))
body = ['body_example'] # list[str] | 

try:
    # fulfillment:read - Returns the plant passport PDF for the BatchIds.
    api_response = api_instance.get_plant_passport_pdf(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlantPassportsApi->get_plant_passport_pdf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_plant_passport_pdf_by_sales_channel_order_id**
> str get_plant_passport_pdf_by_sales_channel_order_id(sales_channel_order_id)

fulfillment:read - Returns plant passport PDF for the sales order.

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
api_instance = floriday_supplier_client.PlantPassportsApi(floriday_supplier_client.ApiClient(configuration))
sales_channel_order_id = 'sales_channel_order_id_example' # str | 

try:
    # fulfillment:read - Returns plant passport PDF for the sales order.
    api_response = api_instance.get_plant_passport_pdf_by_sales_channel_order_id(sales_channel_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlantPassportsApi->get_plant_passport_pdf_by_sales_channel_order_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_channel_order_id** | **str**|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_plant_passport_pdf_by_sales_order_id**
> str get_plant_passport_pdf_by_sales_order_id(sales_order_id)

fulfillment:read - Returns plant passport PDF for the sales order.

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
api_instance = floriday_supplier_client.PlantPassportsApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns plant passport PDF for the sales order.
    api_response = api_instance.get_plant_passport_pdf_by_sales_order_id(sales_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlantPassportsApi->get_plant_passport_pdf_by_sales_order_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

