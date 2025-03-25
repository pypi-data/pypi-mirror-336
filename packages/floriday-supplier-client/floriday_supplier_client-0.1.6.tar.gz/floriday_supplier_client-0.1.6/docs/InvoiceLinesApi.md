# floriday_supplier_client.InvoiceLinesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_invoice_lines_by_sales_order_id**](InvoiceLinesApi.md#get_invoice_lines_by_sales_order_id) | **GET** /invoice-lines/{salesOrderId} | sales-order:read - Returns invoice lines by sales order
[**get_invoice_lines_by_sequence_number**](InvoiceLinesApi.md#get_invoice_lines_by_sequence_number) | **GET** /invoice-lines/sync/{sequenceNumber} | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 invoice lines starting from a specified sequence number.
[**get_invoice_lines_max_sequence**](InvoiceLinesApi.md#get_invoice_lines_max_sequence) | **GET** /invoice-lines/current-max-sequence | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in invoice lines.

# **get_invoice_lines_by_sales_order_id**
> list[InvoiceLine] get_invoice_lines_by_sales_order_id(sales_order_id)

sales-order:read - Returns invoice lines by sales order

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
api_instance = floriday_supplier_client.InvoiceLinesApi(floriday_supplier_client.ApiClient(configuration))
sales_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:read - Returns invoice lines by sales order
    api_response = api_instance.get_invoice_lines_by_sales_order_id(sales_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoiceLinesApi->get_invoice_lines_by_sales_order_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_id** | [**str**](.md)|  | 

### Return type

[**list[InvoiceLine]**](InvoiceLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invoice_lines_by_sequence_number**
> SyncResultOfInvoiceLine get_invoice_lines_by_sequence_number(sequence_number, limit_result=limit_result)

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 invoice lines starting from a specified sequence number.

**Synchronization endpoint** Fetches the succeeding modified records based on `Limit` and the given `SequenceNumber`.   **Note** Your data is up to date when your given `SequenceNumber` is equal to the received `MaximumSequenceNumber`.

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
api_instance = floriday_supplier_client.InvoiceLinesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 56 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 invoice lines starting from a specified sequence number.
    api_response = api_instance.get_invoice_lines_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoiceLinesApi->get_invoice_lines_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfInvoiceLine**](SyncResultOfInvoiceLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invoice_lines_max_sequence**
> int get_invoice_lines_max_sequence()

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in invoice lines.

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
api_instance = floriday_supplier_client.InvoiceLinesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in invoice lines.
    api_response = api_instance.get_invoice_lines_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvoiceLinesApi->get_invoice_lines_max_sequence: %s\n" % e)
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

