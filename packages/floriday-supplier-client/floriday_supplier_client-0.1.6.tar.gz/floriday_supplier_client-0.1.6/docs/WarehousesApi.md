# floriday_supplier_client.WarehousesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_warehouses**](WarehousesApi.md#get_warehouses) | **GET** /warehouses | organization:read - Returns warehouses.
[**get_warehouses_auction**](WarehousesApi.md#get_warehouses_auction) | **GET** /warehouses/auction | organization:read - Returns warehouses with auction capability.
[**get_warehouses_by_sequence_number**](WarehousesApi.md#get_warehouses_by_sequence_number) | **GET** /warehouses/sync/{sequenceNumber} | organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 warehouses starting from a specified sequence number.
[**get_warehouses_external_stock**](WarehousesApi.md#get_warehouses_external_stock) | **GET** /warehouses/external-stock | organization:read - Returns warehouses for external stock management.
[**get_warehouses_max_sequence**](WarehousesApi.md#get_warehouses_max_sequence) | **GET** /warehouses/current-max-sequence | organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.

# **get_warehouses**
> list[Warehouse] get_warehouses(exclude_external_warehouses=exclude_external_warehouses)

organization:read - Returns warehouses.

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
api_instance = floriday_supplier_client.WarehousesApi(floriday_supplier_client.ApiClient(configuration))
exclude_external_warehouses = false # bool |  (optional) (default to false)

try:
    # organization:read - Returns warehouses.
    api_response = api_instance.get_warehouses(exclude_external_warehouses=exclude_external_warehouses)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehousesApi->get_warehouses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude_external_warehouses** | **bool**|  | [optional] [default to false]

### Return type

[**list[Warehouse]**](Warehouse.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_warehouses_auction**
> list[Warehouse] get_warehouses_auction()

organization:read - Returns warehouses with auction capability.

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
api_instance = floriday_supplier_client.WarehousesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # organization:read - Returns warehouses with auction capability.
    api_response = api_instance.get_warehouses_auction()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehousesApi->get_warehouses_auction: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Warehouse]**](Warehouse.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_warehouses_by_sequence_number**
> SyncResultOfWarehouse get_warehouses_by_sequence_number(sequence_number, limit_result=limit_result)

organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 warehouses starting from a specified sequence number.

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
api_instance = floriday_supplier_client.WarehousesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 warehouses starting from a specified sequence number.
    api_response = api_instance.get_warehouses_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehousesApi->get_warehouses_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfWarehouse**](SyncResultOfWarehouse.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_warehouses_external_stock**
> list[Warehouse] get_warehouses_external_stock()

organization:read - Returns warehouses for external stock management.

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
api_instance = floriday_supplier_client.WarehousesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # organization:read - Returns warehouses for external stock management.
    api_response = api_instance.get_warehouses_external_stock()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehousesApi->get_warehouses_external_stock: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Warehouse]**](Warehouse.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_warehouses_max_sequence**
> int get_warehouses_max_sequence()

organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.

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
api_instance = floriday_supplier_client.WarehousesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.
    api_response = api_instance.get_warehouses_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WarehousesApi->get_warehouses_max_sequence: %s\n" % e)
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

