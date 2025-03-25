# floriday_supplier_client.PriceGroupsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_price_group_by_id**](PriceGroupsApi.md#get_price_group_by_id) | **GET** /price-groups/{priceGroupId} | supply:read - Returns a price group.
[**get_price_groups_by_sequence_number**](PriceGroupsApi.md#get_price_groups_by_sequence_number) | **GET** /price-groups/sync/{sequenceNumber} | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 price groups starting from a specified sequence number.
[**get_price_groups_max_sequence**](PriceGroupsApi.md#get_price_groups_max_sequence) | **GET** /price-groups/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in price groups.

# **get_price_group_by_id**
> PriceGroup get_price_group_by_id(price_group_id)

supply:read - Returns a price group.

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
api_instance = floriday_supplier_client.PriceGroupsApi(floriday_supplier_client.ApiClient(configuration))
price_group_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a price group.
    api_response = api_instance.get_price_group_by_id(price_group_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PriceGroupsApi->get_price_group_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **price_group_id** | [**str**](.md)|  | 

### Return type

[**PriceGroup**](PriceGroup.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_price_groups_by_sequence_number**
> SyncResultOfPriceGroup get_price_groups_by_sequence_number(sequence_number, limit=limit)

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 price groups starting from a specified sequence number.

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
api_instance = floriday_supplier_client.PriceGroupsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 price groups starting from a specified sequence number.
    api_response = api_instance.get_price_groups_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PriceGroupsApi->get_price_groups_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfPriceGroup**](SyncResultOfPriceGroup.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_price_groups_max_sequence**
> int get_price_groups_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in price groups.

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
api_instance = floriday_supplier_client.PriceGroupsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in price groups.
    api_response = api_instance.get_price_groups_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PriceGroupsApi->get_price_groups_max_sequence: %s\n" % e)
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

