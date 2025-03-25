# floriday_supplier_client.CustomPackagesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_custom_package_by_id**](CustomPackagesApi.md#get_custom_package_by_id) | **GET** /custom-packages/{customPackageId} | catalog:read - Get a custom package.
[**get_custom_packages**](CustomPackagesApi.md#get_custom_packages) | **GET** /custom-packages | catalog:read - Returns custom packages.
[**get_custom_packages_by_sequence_number**](CustomPackagesApi.md#get_custom_packages_by_sequence_number) | **GET** /custom-packages/sync/{sequenceNumber} | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 custom packages starting from a specified sequence number.
[**get_custom_packages_max_sequence**](CustomPackagesApi.md#get_custom_packages_max_sequence) | **GET** /custom-packages/current-max-sequence | catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in custom packages.

# **get_custom_package_by_id**
> CustomPackage get_custom_package_by_id(custom_package_id)

catalog:read - Get a custom package.

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
api_instance = floriday_supplier_client.CustomPackagesApi(floriday_supplier_client.ApiClient(configuration))
custom_package_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Get a custom package.
    api_response = api_instance.get_custom_package_by_id(custom_package_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomPackagesApi->get_custom_package_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_package_id** | [**str**](.md)|  | 

### Return type

[**CustomPackage**](CustomPackage.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_packages**
> list[CustomPackage] get_custom_packages()

catalog:read - Returns custom packages.

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
api_instance = floriday_supplier_client.CustomPackagesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - Returns custom packages.
    api_response = api_instance.get_custom_packages()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomPackagesApi->get_custom_packages: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CustomPackage]**](CustomPackage.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_packages_by_sequence_number**
> SyncResultOfCustomPackage get_custom_packages_by_sequence_number(sequence_number, limit=limit)

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 custom packages starting from a specified sequence number.

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
api_instance = floriday_supplier_client.CustomPackagesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 custom packages starting from a specified sequence number.
    api_response = api_instance.get_custom_packages_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomPackagesApi->get_custom_packages_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfCustomPackage**](SyncResultOfCustomPackage.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_packages_max_sequence**
> int get_custom_packages_max_sequence()

catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in custom packages.

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
api_instance = floriday_supplier_client.CustomPackagesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # catalog:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in custom packages.
    api_response = api_instance.get_custom_packages_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomPackagesApi->get_custom_packages_max_sequence: %s\n" % e)
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

