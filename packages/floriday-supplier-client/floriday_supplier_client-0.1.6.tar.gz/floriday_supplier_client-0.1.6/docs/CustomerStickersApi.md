# floriday_supplier_client.CustomerStickersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_customer_sticker_pdf_by_id**](CustomerStickersApi.md#get_customer_sticker_pdf_by_id) | **GET** /customer-stickers/{stickerId} | sticker:read - Returns customer sticker in pdf format
[**get_customer_sticker_pdf_by_ids**](CustomerStickersApi.md#get_customer_sticker_pdf_by_ids) | **GET** /customer-stickers | sticker:read - Returns customer stickers in pdf format. Pages are duplicated based on the number of copies in the customer sticker.
[**get_customer_stickers_by_sequence_number**](CustomerStickersApi.md#get_customer_stickers_by_sequence_number) | **GET** /customer-stickers/sync/{sequenceNumber} | sticker:read - Returns a list of max 1000 customer stickers metadata starting from a specified sequence number.
[**get_customer_stickers_max_sequence**](CustomerStickersApi.md#get_customer_stickers_max_sequence) | **GET** /customer-stickers/current-max-sequence | sticker:read - Returns the maximum sequence number found in customer stickers.
[**set_customer_stickers_is_handled**](CustomerStickersApi.md#set_customer_stickers_is_handled) | **PATCH** /customer-stickers/handled | sticker:write - Indicate which stickers are printed and placed.

# **get_customer_sticker_pdf_by_id**
> str get_customer_sticker_pdf_by_id(sticker_id, duplicate_pages_based_on_number_of_copies)

sticker:read - Returns customer sticker in pdf format

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
api_instance = floriday_supplier_client.CustomerStickersApi(floriday_supplier_client.ApiClient(configuration))
sticker_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
duplicate_pages_based_on_number_of_copies = true # bool | 

try:
    # sticker:read - Returns customer sticker in pdf format
    api_response = api_instance.get_customer_sticker_pdf_by_id(sticker_id, duplicate_pages_based_on_number_of_copies)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerStickersApi->get_customer_sticker_pdf_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sticker_id** | [**str**](.md)|  | 
 **duplicate_pages_based_on_number_of_copies** | **bool**|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_sticker_pdf_by_ids**
> str get_customer_sticker_pdf_by_ids(sticker_ids)

sticker:read - Returns customer stickers in pdf format. Pages are duplicated based on the number of copies in the customer sticker.

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
api_instance = floriday_supplier_client.CustomerStickersApi(floriday_supplier_client.ApiClient(configuration))
sticker_ids = ['sticker_ids_example'] # list[str] | 

try:
    # sticker:read - Returns customer stickers in pdf format. Pages are duplicated based on the number of copies in the customer sticker.
    api_response = api_instance.get_customer_sticker_pdf_by_ids(sticker_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerStickersApi->get_customer_sticker_pdf_by_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sticker_ids** | [**list[str]**](str.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_stickers_by_sequence_number**
> SyncResultOfCustomerSticker get_customer_stickers_by_sequence_number(sequence_number, limit_result=limit_result)

sticker:read - Returns a list of max 1000 customer stickers metadata starting from a specified sequence number.

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
api_instance = floriday_supplier_client.CustomerStickersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # sticker:read - Returns a list of max 1000 customer stickers metadata starting from a specified sequence number.
    api_response = api_instance.get_customer_stickers_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerStickersApi->get_customer_stickers_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfCustomerSticker**](SyncResultOfCustomerSticker.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_stickers_max_sequence**
> int get_customer_stickers_max_sequence()

sticker:read - Returns the maximum sequence number found in customer stickers.

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
api_instance = floriday_supplier_client.CustomerStickersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # sticker:read - Returns the maximum sequence number found in customer stickers.
    api_response = api_instance.get_customer_stickers_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerStickersApi->get_customer_stickers_max_sequence: %s\n" % e)
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

# **set_customer_stickers_is_handled**
> set_customer_stickers_is_handled(sticker_ids)

sticker:write - Indicate which stickers are printed and placed.

IsHandled indication will be set to true.

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
api_instance = floriday_supplier_client.CustomerStickersApi(floriday_supplier_client.ApiClient(configuration))
sticker_ids = ['sticker_ids_example'] # list[str] | 

try:
    # sticker:write - Indicate which stickers are printed and placed.
    api_instance.set_customer_stickers_is_handled(sticker_ids)
except ApiException as e:
    print("Exception when calling CustomerStickersApi->set_customer_stickers_is_handled: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sticker_ids** | [**list[str]**](str.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

