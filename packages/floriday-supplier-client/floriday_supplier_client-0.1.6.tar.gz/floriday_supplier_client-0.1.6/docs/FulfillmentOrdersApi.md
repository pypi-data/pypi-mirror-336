# floriday_supplier_client.FulfillmentOrdersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_fulfillment_order**](FulfillmentOrdersApi.md#add_fulfillment_order) | **POST** /fulfillment-orders | fulfillment:write - Creates a fulfillment order.
[**add_fulfillment_order_correction**](FulfillmentOrdersApi.md#add_fulfillment_order_correction) | **POST** /fulfillment-orders/{fulfillmentOrderId}/corrections | fulfillment:write - Corrects a fulfillment order.
[**delete_fulfillment_order**](FulfillmentOrdersApi.md#delete_fulfillment_order) | **DELETE** /fulfillment-orders/{fulfillmentOrderId} | fulfillment:write - Delete a fulfillment order.
[**edit_fulfillment_order**](FulfillmentOrdersApi.md#edit_fulfillment_order) | **PUT** /fulfillment-orders/{fulfillmentOrderId} | fulfillment:write - Updates a fulfillment order.
[**get_fulfillment_order_by_id**](FulfillmentOrdersApi.md#get_fulfillment_order_by_id) | **GET** /fulfillment-orders/{fulfillmentOrderId} | fulfillment:read - Returns a fulfillment order.
[**get_fulfillment_order_corrections_by_id**](FulfillmentOrdersApi.md#get_fulfillment_order_corrections_by_id) | **GET** /fulfillment-orders/{fulfillmentOrderId}/corrections | fulfillment:read - Returns fulfillment order corrections.
[**get_fulfillment_order_status_by_id**](FulfillmentOrdersApi.md#get_fulfillment_order_status_by_id) | **GET** /fulfillment-orders/{fulfillmentOrderId}/status | fulfillment:read - Returns the status of a fulfillment order.
[**get_fulfillment_orders_by_sequence_number**](FulfillmentOrdersApi.md#get_fulfillment_orders_by_sequence_number) | **GET** /fulfillment-orders/sync/{sequenceNumber} | fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 fulfillment orders starting from a specified sequence number.
[**get_fulfillment_orders_max_sequence**](FulfillmentOrdersApi.md#get_fulfillment_orders_max_sequence) | **GET** /fulfillment-orders/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in fulfillment orders.
[**get_logistic_labels_by_id**](FulfillmentOrdersApi.md#get_logistic_labels_by_id) | **GET** /fulfillment-orders/{fulfillmentOrderId}/logistic-labels | fulfillment:read - rate limit: 1.0 per second - burst limit: 60 - Returns logistic labels (SSCC or delivery notes) as pdf for a fulfillment order.
[**get_tray_labels_as_pdf_by_fulfillment_order_id**](FulfillmentOrdersApi.md#get_tray_labels_as_pdf_by_fulfillment_order_id) | **GET** /fulfillment-orders/{fulfillmentOrderId}/stickers | fulfillment:read - Returns tray stickers as pdf for a fulfillment order.

# **add_fulfillment_order**
> add_fulfillment_order(body)

fulfillment:write - Creates a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.FulfillmentOrderCreate() # FulfillmentOrderCreate | 

try:
    # fulfillment:write - Creates a fulfillment order.
    api_instance.add_fulfillment_order(body)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->add_fulfillment_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FulfillmentOrderCreate**](FulfillmentOrderCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_fulfillment_order_correction**
> add_fulfillment_order_correction(body, fulfillment_order_id)

fulfillment:write - Corrects a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddFulfillmentOrderCorrection() # AddFulfillmentOrderCorrection | 
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Corrects a fulfillment order.
    api_instance.add_fulfillment_order_correction(body, fulfillment_order_id)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->add_fulfillment_order_correction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddFulfillmentOrderCorrection**](AddFulfillmentOrderCorrection.md)|  | 
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_fulfillment_order**
> delete_fulfillment_order(fulfillment_order_id)

fulfillment:write - Delete a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Delete a fulfillment order.
    api_instance.delete_fulfillment_order(fulfillment_order_id)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->delete_fulfillment_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_fulfillment_order**
> edit_fulfillment_order(body, fulfillment_order_id)

fulfillment:write - Updates a fulfillment order.

Update to the new number of load carriers ( lower than original value ). Load carrier(s) with highest sequence-number(s) will be removed first.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.FulfillmentOrderUpdate() # FulfillmentOrderUpdate | 
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - Updates a fulfillment order.
    api_instance.edit_fulfillment_order(body, fulfillment_order_id)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->edit_fulfillment_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FulfillmentOrderUpdate**](FulfillmentOrderUpdate.md)|  | 
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fulfillment_order_by_id**
> FulfillmentOrder get_fulfillment_order_by_id(fulfillment_order_id)

fulfillment:read - Returns a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns a fulfillment order.
    api_response = api_instance.get_fulfillment_order_by_id(fulfillment_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_fulfillment_order_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

[**FulfillmentOrder**](FulfillmentOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fulfillment_order_corrections_by_id**
> list[FulfillmentOrderCorrection] get_fulfillment_order_corrections_by_id(fulfillment_order_id)

fulfillment:read - Returns fulfillment order corrections.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns fulfillment order corrections.
    api_response = api_instance.get_fulfillment_order_corrections_by_id(fulfillment_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_fulfillment_order_corrections_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

[**list[FulfillmentOrderCorrection]**](FulfillmentOrderCorrection.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fulfillment_order_status_by_id**
> FulfillmentOrderStatus get_fulfillment_order_status_by_id(fulfillment_order_id)

fulfillment:read - Returns the status of a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns the status of a fulfillment order.
    api_response = api_instance.get_fulfillment_order_status_by_id(fulfillment_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_fulfillment_order_status_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

[**FulfillmentOrderStatus**](FulfillmentOrderStatus.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fulfillment_orders_by_sequence_number**
> SyncResultOfFulfillmentOrder get_fulfillment_orders_by_sequence_number(sequence_number, limit_result=limit_result)

fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 fulfillment orders starting from a specified sequence number.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 fulfillment orders starting from a specified sequence number.
    api_response = api_instance.get_fulfillment_orders_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_fulfillment_orders_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfFulfillmentOrder**](SyncResultOfFulfillmentOrder.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fulfillment_orders_max_sequence**
> int get_fulfillment_orders_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in fulfillment orders.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in fulfillment orders.
    api_response = api_instance.get_fulfillment_orders_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_fulfillment_orders_max_sequence: %s\n" % e)
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

# **get_logistic_labels_by_id**
> str get_logistic_labels_by_id(fulfillment_order_id)

fulfillment:read - rate limit: 1.0 per second - burst limit: 60 - Returns logistic labels (SSCC or delivery notes) as pdf for a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - rate limit: 1.0 per second - burst limit: 60 - Returns logistic labels (SSCC or delivery notes) as pdf for a fulfillment order.
    api_response = api_instance.get_logistic_labels_by_id(fulfillment_order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_logistic_labels_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tray_labels_as_pdf_by_fulfillment_order_id**
> str get_tray_labels_as_pdf_by_fulfillment_order_id(fulfillment_order_id, show_customer_on_sticker, single_sticker_per_batch=single_sticker_per_batch)

fulfillment:read - Returns tray stickers as pdf for a fulfillment order.

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
api_instance = floriday_supplier_client.FulfillmentOrdersApi(floriday_supplier_client.ApiClient(configuration))
fulfillment_order_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
show_customer_on_sticker = true # bool | 
single_sticker_per_batch = true # bool |  (optional)

try:
    # fulfillment:read - Returns tray stickers as pdf for a fulfillment order.
    api_response = api_instance.get_tray_labels_as_pdf_by_fulfillment_order_id(fulfillment_order_id, show_customer_on_sticker, single_sticker_per_batch=single_sticker_per_batch)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FulfillmentOrdersApi->get_tray_labels_as_pdf_by_fulfillment_order_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fulfillment_order_id** | [**str**](.md)|  | 
 **show_customer_on_sticker** | **bool**|  | 
 **single_sticker_per_batch** | **bool**|  | [optional] 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

