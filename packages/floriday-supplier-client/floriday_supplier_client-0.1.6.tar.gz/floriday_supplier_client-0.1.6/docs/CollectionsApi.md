# floriday_supplier_client.CollectionsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_collection**](CollectionsApi.md#add_collection) | **POST** /collections | catalog:write - Create a collection.
[**add_trade_items_to_collection**](CollectionsApi.md#add_trade_items_to_collection) | **POST** /collections/{collectionId}/trade-items | catalog:write - Add trade items to collection.
[**delete_collection**](CollectionsApi.md#delete_collection) | **DELETE** /collections/{collectionId} | catalog:write - Delete a collection.
[**delete_collection_trade_items**](CollectionsApi.md#delete_collection_trade_items) | **DELETE** /collections/{collectionId}/trade-items | catalog:write - Remove trade items from collection.
[**edit_collection**](CollectionsApi.md#edit_collection) | **PUT** /collections/{collectionId} | catalog:write - Update a collection.
[**get_collection_by_id**](CollectionsApi.md#get_collection_by_id) | **GET** /collections/{collectionId} | catalog:read - Returns an collection.
[**get_collections_by_sequence_number**](CollectionsApi.md#get_collections_by_sequence_number) | **GET** /collections/sync/{sequenceNumber} | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 collections starting from a specified sequence number.
[**get_collections_max_sequence**](CollectionsApi.md#get_collections_max_sequence) | **GET** /collections/current-max-sequence | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in collections.
[**set_sort_order_for_collection**](CollectionsApi.md#set_sort_order_for_collection) | **PATCH** /collections/{collectionId}/sort-order | catalog:write - Set sort order for collection.

# **add_collection**
> add_collection(body)

catalog:write - Create a collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.CollectionCreate() # CollectionCreate | 

try:
    # catalog:write - Create a collection.
    api_instance.add_collection(body)
except ApiException as e:
    print("Exception when calling CollectionsApi->add_collection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CollectionCreate**](CollectionCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_trade_items_to_collection**
> add_trade_items_to_collection(body, collection_id)

catalog:write - Add trade items to collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.CollectionTradeItemIds() # CollectionTradeItemIds | 
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Add trade items to collection.
    api_instance.add_trade_items_to_collection(body, collection_id)
except ApiException as e:
    print("Exception when calling CollectionsApi->add_trade_items_to_collection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CollectionTradeItemIds**](CollectionTradeItemIds.md)|  | 
 **collection_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_collection**
> delete_collection(collection_id)

catalog:write - Delete a collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Delete a collection.
    api_instance.delete_collection(collection_id)
except ApiException as e:
    print("Exception when calling CollectionsApi->delete_collection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_collection_trade_items**
> delete_collection_trade_items(body, collection_id)

catalog:write - Remove trade items from collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.CollectionTradeItemIds() # CollectionTradeItemIds | 
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Remove trade items from collection.
    api_instance.delete_collection_trade_items(body, collection_id)
except ApiException as e:
    print("Exception when calling CollectionsApi->delete_collection_trade_items: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CollectionTradeItemIds**](CollectionTradeItemIds.md)|  | 
 **collection_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_collection**
> edit_collection(body, collection_id)

catalog:write - Update a collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.CollectionUpdate() # CollectionUpdate | 
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:write - Update a collection.
    api_instance.edit_collection(body, collection_id)
except ApiException as e:
    print("Exception when calling CollectionsApi->edit_collection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CollectionUpdate**](CollectionUpdate.md)|  | 
 **collection_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collection_by_id**
> Collection get_collection_by_id(collection_id)

catalog:read - Returns an collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns an collection.
    api_response = api_instance.get_collection_by_id(collection_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CollectionsApi->get_collection_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | [**str**](.md)|  | 

### Return type

[**Collection**](Collection.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collections_by_sequence_number**
> SyncResultOfCollection get_collections_by_sequence_number(sequence_number, limit_result=limit_result)

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 collections starting from a specified sequence number.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 collections starting from a specified sequence number.
    api_response = api_instance.get_collections_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CollectionsApi->get_collections_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfCollection**](SyncResultOfCollection.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collections_max_sequence**
> int get_collections_max_sequence()

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in collections.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in collections.
    api_response = api_instance.get_collections_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CollectionsApi->get_collections_max_sequence: %s\n" % e)
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

# **set_sort_order_for_collection**
> set_sort_order_for_collection(collection_id, sort_order)

catalog:write - Set sort order for collection.

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
api_instance = floriday_supplier_client.CollectionsApi(floriday_supplier_client.ApiClient(configuration))
collection_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
sort_order = 56 # int | 

try:
    # catalog:write - Set sort order for collection.
    api_instance.set_sort_order_for_collection(collection_id, sort_order)
except ApiException as e:
    print("Exception when calling CollectionsApi->set_sort_order_for_collection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | [**str**](.md)|  | 
 **sort_order** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

