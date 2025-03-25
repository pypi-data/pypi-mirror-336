# floriday_supplier_client.TradeItemsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_trade_item**](TradeItemsApi.md#add_trade_item) | **POST** /trade-items | catalog:write - Creates a new trade item.
[**add_trade_item_variant**](TradeItemsApi.md#add_trade_item_variant) | **POST** /trade-items/variants | catalog:write - Creates a new trade item variant.
[**delete_trade_item**](TradeItemsApi.md#delete_trade_item) | **DELETE** /trade-items/{tradeItemId} | catalog:write - Deletes a trade item.
[**edit_trade_item**](TradeItemsApi.md#edit_trade_item) | **PUT** /trade-items/{tradeItemId} | catalog:write - Updates a trade item.
[**edit_trade_item_variant**](TradeItemsApi.md#edit_trade_item_variant) | **PUT** /trade-items/variants/{tradeItemId} | catalog:write - Update a trade item variant.
[**get_trade_item_by_id**](TradeItemsApi.md#get_trade_item_by_id) | **GET** /trade-items/{tradeItemId} | catalog:read - Returns a trade item.
[**get_trade_item_by_id_and_version**](TradeItemsApi.md#get_trade_item_by_id_and_version) | **GET** /trade-items/{tradeItemId}/{version} | catalog:read - Returns a trade item.
[**get_trade_items**](TradeItemsApi.md#get_trade_items) | **GET** /trade-items | catalog:read - Returns trade items.
[**get_trade_items_by_sequence_number**](TradeItemsApi.md#get_trade_items_by_sequence_number) | **GET** /trade-items/sync/{sequenceNumber} | catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade items starting from a specified sequence number.
[**get_trade_items_max_sequence**](TradeItemsApi.md#get_trade_items_max_sequence) | **GET** /trade-items/current-max-sequence | catalog:read - Returns the maximum sequence number found in trade items.
[**get_trade_items_summary**](TradeItemsApi.md#get_trade_items_summary) | **GET** /trade-items/summary | catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns public trade item information of a supplier.

# **add_trade_item**
> add_trade_item(body)

catalog:write - Creates a new trade item.

Photo URLs posted as Floriday media must conform with the following format https://image.floriday.io/mediaId.jpg

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.TradeItemBase() # TradeItemBase | 

try:
    # catalog:write - Creates a new trade item.
    api_instance.add_trade_item(body)
except ApiException as e:
    print("Exception when calling TradeItemsApi->add_trade_item: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TradeItemBase**](TradeItemBase.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_trade_item_variant**
> add_trade_item_variant(body)

catalog:write - Creates a new trade item variant.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.TradeItemVariant() # TradeItemVariant | 

try:
    # catalog:write - Creates a new trade item variant.
    api_instance.add_trade_item_variant(body)
except ApiException as e:
    print("Exception when calling TradeItemsApi->add_trade_item_variant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TradeItemVariant**](TradeItemVariant.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_trade_item**
> delete_trade_item(trade_item_id)

catalog:write - Deletes a trade item.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Deletes a trade item.
    api_instance.delete_trade_item(trade_item_id)
except ApiException as e:
    print("Exception when calling TradeItemsApi->delete_trade_item: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_trade_item**
> edit_trade_item(body, trade_item_id)

catalog:write - Updates a trade item.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.TradeItemUpdate() # TradeItemUpdate | 
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Updates a trade item.
    api_instance.edit_trade_item(body, trade_item_id)
except ApiException as e:
    print("Exception when calling TradeItemsApi->edit_trade_item: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TradeItemUpdate**](TradeItemUpdate.md)|  | 
 **trade_item_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_trade_item_variant**
> edit_trade_item_variant(body, trade_item_id)

catalog:write - Update a trade item variant.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.TradeItemVariantUpdate() # TradeItemVariantUpdate | 
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Update a trade item variant.
    api_instance.edit_trade_item_variant(body, trade_item_id)
except ApiException as e:
    print("Exception when calling TradeItemsApi->edit_trade_item_variant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TradeItemVariantUpdate**](TradeItemVariantUpdate.md)|  | 
 **trade_item_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_by_id**
> TradeItem get_trade_item_by_id(trade_item_id)

catalog:read - Returns a trade item.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns a trade item.
    api_response = api_instance.get_trade_item_by_id(trade_item_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_item_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 

### Return type

[**TradeItem**](TradeItem.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_by_id_and_version**
> TradeItem get_trade_item_by_id_and_version(trade_item_id, version)

catalog:read - Returns a trade item.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
version = 56 # int | 

try:
    # catalog:read - Returns a trade item.
    api_response = api_instance.get_trade_item_by_id_and_version(trade_item_id, version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_item_by_id_and_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 
 **version** | **int**|  | 

### Return type

[**TradeItem**](TradeItem.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_items**
> list[TradeItem] get_trade_items(page=page, limit_result=limit_result, include_deleted=include_deleted)

catalog:read - Returns trade items.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
page = 1 # int |  (optional) (default to 1)
limit_result = 1000 # int |  (optional) (default to 1000)
include_deleted = false # bool |  (optional) (default to false)

try:
    # catalog:read - Returns trade items.
    api_response = api_instance.get_trade_items(page=page, limit_result=limit_result, include_deleted=include_deleted)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_items: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**|  | [optional] [default to 1]
 **limit_result** | **int**|  | [optional] [default to 1000]
 **include_deleted** | **bool**|  | [optional] [default to false]

### Return type

[**list[TradeItem]**](TradeItem.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_items_by_sequence_number**
> SyncResultOfTradeItem get_trade_items_by_sequence_number(sequence_number, limit_result=limit_result)

catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade items starting from a specified sequence number.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 trade items starting from a specified sequence number.
    api_response = api_instance.get_trade_items_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_items_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfTradeItem**](SyncResultOfTradeItem.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_items_max_sequence**
> int get_trade_items_max_sequence()

catalog:read - Returns the maximum sequence number found in trade items.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - Returns the maximum sequence number found in trade items.
    api_response = api_instance.get_trade_items_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_items_max_sequence: %s\n" % e)
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

# **get_trade_items_summary**
> list[TradeItemSummary] get_trade_items_summary(trade_item_ids=trade_item_ids, supplier_organization_id=supplier_organization_id)

catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns public trade item information of a supplier.

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
api_instance = floriday_supplier_client.TradeItemsApi(floriday_supplier_client.ApiClient(configuration))
trade_item_ids = ['trade_item_ids_example'] # list[str] |  (optional)
supplier_organization_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str |  (optional)

try:
    # catalog:read - rate limit: 2.0 per second - burst limit: 200 - Returns public trade item information of a supplier.
    api_response = api_instance.get_trade_items_summary(trade_item_ids=trade_item_ids, supplier_organization_id=supplier_organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeItemsApi->get_trade_items_summary: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_ids** | [**list[str]**](str.md)|  | [optional] 
 **supplier_organization_id** | [**str**](.md)|  | [optional] 

### Return type

[**list[TradeItemSummary]**](TradeItemSummary.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

