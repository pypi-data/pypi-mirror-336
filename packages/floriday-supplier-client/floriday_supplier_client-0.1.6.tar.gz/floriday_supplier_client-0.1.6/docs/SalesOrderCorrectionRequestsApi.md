# floriday_supplier_client.SalesOrderCorrectionRequestsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accept_sales_order_correction_request**](SalesOrderCorrectionRequestsApi.md#accept_sales_order_correction_request) | **PATCH** /sales-order-correction-requests/{salesOrderCorrectionRequestId}/accept | sales-order:write - Accept sales order correction request.
[**add_sales_order_correction_request**](SalesOrderCorrectionRequestsApi.md#add_sales_order_correction_request) | **POST** /sales-order-correction-requests | sales-order:write - Creates a new sales order correction request.
[**decline_sales_order_correction_request**](SalesOrderCorrectionRequestsApi.md#decline_sales_order_correction_request) | **PATCH** /sales-order-correction-requests/{salesOrderCorrectionRequestId}/decline | sales-order:write - Decline sales order correction request.
[**delete_sales_order_correction_request**](SalesOrderCorrectionRequestsApi.md#delete_sales_order_correction_request) | **DELETE** /sales-order-correction-requests/{salesOrderCorrectionRequestId} | sales-order:write - Delete a sales order correction request.
[**get_sales_order_correction_request_by_id**](SalesOrderCorrectionRequestsApi.md#get_sales_order_correction_request_by_id) | **GET** /sales-order-correction-requests/{salesOrderCorrectionRequestId} | sales-order:read - Returns a sales order correction request.
[**get_sales_order_correction_requests_by_sequence_number**](SalesOrderCorrectionRequestsApi.md#get_sales_order_correction_requests_by_sequence_number) | **GET** /sales-order-correction-requests/sync/{sequenceNumber} | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales order correction requests starting from a specified sequence number.
[**get_sales_order_correction_requests_max_sequence**](SalesOrderCorrectionRequestsApi.md#get_sales_order_correction_requests_max_sequence) | **GET** /sales-order-correction-requests/current-max-sequence | sales-order:read - rate limit: 3.4 per second - burst limit: 1000 -  Returns the maximum sequence number found in sales order correction requests.

# **accept_sales_order_correction_request**
> accept_sales_order_correction_request(body, sales_order_correction_request_id)

sales-order:write - Accept sales order correction request.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SalesOrderCorrectionRequestAccept() # SalesOrderCorrectionRequestAccept | 
sales_order_correction_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Accept sales order correction request.
    api_instance.accept_sales_order_correction_request(body, sales_order_correction_request_id)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->accept_sales_order_correction_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SalesOrderCorrectionRequestAccept**](SalesOrderCorrectionRequestAccept.md)|  | 
 **sales_order_correction_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sales_order_correction_request**
> add_sales_order_correction_request(body)

sales-order:write - Creates a new sales order correction request.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddSalesOrderCorrectionRequest() # AddSalesOrderCorrectionRequest | 

try:
    # sales-order:write - Creates a new sales order correction request.
    api_instance.add_sales_order_correction_request(body)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->add_sales_order_correction_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddSalesOrderCorrectionRequest**](AddSalesOrderCorrectionRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **decline_sales_order_correction_request**
> decline_sales_order_correction_request(body, sales_order_correction_request_id)

sales-order:write - Decline sales order correction request.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SalesOrderCorrectionRequestDecline() # SalesOrderCorrectionRequestDecline | 
sales_order_correction_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Decline sales order correction request.
    api_instance.decline_sales_order_correction_request(body, sales_order_correction_request_id)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->decline_sales_order_correction_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SalesOrderCorrectionRequestDecline**](SalesOrderCorrectionRequestDecline.md)|  | 
 **sales_order_correction_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sales_order_correction_request**
> delete_sales_order_correction_request(sales_order_correction_request_id)

sales-order:write - Delete a sales order correction request.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
sales_order_correction_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Delete a sales order correction request.
    api_instance.delete_sales_order_correction_request(sales_order_correction_request_id)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->delete_sales_order_correction_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_correction_request_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_order_correction_request_by_id**
> SalesOrderCorrectionRequest get_sales_order_correction_request_by_id(sales_order_correction_request_id)

sales-order:read - Returns a sales order correction request.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
sales_order_correction_request_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:read - Returns a sales order correction request.
    api_response = api_instance.get_sales_order_correction_request_by_id(sales_order_correction_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->get_sales_order_correction_request_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sales_order_correction_request_id** | [**str**](.md)|  | 

### Return type

[**SalesOrderCorrectionRequest**](SalesOrderCorrectionRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_order_correction_requests_by_sequence_number**
> SyncResultOfSalesOrderCorrectionRequest get_sales_order_correction_requests_by_sequence_number(sequence_number, limit_result=limit_result)

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales order correction requests starting from a specified sequence number.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 sales order correction requests starting from a specified sequence number.
    api_response = api_instance.get_sales_order_correction_requests_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->get_sales_order_correction_requests_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfSalesOrderCorrectionRequest**](SyncResultOfSalesOrderCorrectionRequest.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sales_order_correction_requests_max_sequence**
> int get_sales_order_correction_requests_max_sequence()

sales-order:read - rate limit: 3.4 per second - burst limit: 1000 -  Returns the maximum sequence number found in sales order correction requests.

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
api_instance = floriday_supplier_client.SalesOrderCorrectionRequestsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # sales-order:read - rate limit: 3.4 per second - burst limit: 1000 -  Returns the maximum sequence number found in sales order correction requests.
    api_response = api_instance.get_sales_order_correction_requests_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SalesOrderCorrectionRequestsApi->get_sales_order_correction_requests_max_sequence: %s\n" % e)
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

