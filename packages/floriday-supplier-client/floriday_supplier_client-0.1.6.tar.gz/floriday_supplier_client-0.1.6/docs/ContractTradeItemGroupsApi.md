# floriday_supplier_client.ContractTradeItemGroupsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_contract_trade_item_group_by_id**](ContractTradeItemGroupsApi.md#get_contract_trade_item_group_by_id) | **GET** /contract-trade-item-groups/{contractTradeItemGroupId} | catalog:read - Returns an contract trade item group.
[**get_contract_trade_item_groups_by_sequence_number**](ContractTradeItemGroupsApi.md#get_contract_trade_item_groups_by_sequence_number) | **GET** /contract-trade-item-groups/sync/{sequenceNumber} | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contract trade item groups starting from a specified sequence number.
[**get_contract_trade_item_groups_max_sequence**](ContractTradeItemGroupsApi.md#get_contract_trade_item_groups_max_sequence) | **GET** /contract-trade-item-groups/current-max-sequence | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contract trade item groups.

# **get_contract_trade_item_group_by_id**
> ContractTradeItemGroup get_contract_trade_item_group_by_id(contract_trade_item_group_id)

catalog:read - Returns an contract trade item group.

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
api_instance = floriday_supplier_client.ContractTradeItemGroupsApi(floriday_supplier_client.ApiClient(configuration))
contract_trade_item_group_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # catalog:read - Returns an contract trade item group.
    api_response = api_instance.get_contract_trade_item_group_by_id(contract_trade_item_group_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractTradeItemGroupsApi->get_contract_trade_item_group_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_trade_item_group_id** | [**str**](.md)|  | 

### Return type

[**ContractTradeItemGroup**](ContractTradeItemGroup.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract_trade_item_groups_by_sequence_number**
> SyncResultOfContractTradeItemGroup get_contract_trade_item_groups_by_sequence_number(sequence_number, limit=limit)

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contract trade item groups starting from a specified sequence number.

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
api_instance = floriday_supplier_client.ContractTradeItemGroupsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 contract trade item groups starting from a specified sequence number.
    api_response = api_instance.get_contract_trade_item_groups_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractTradeItemGroupsApi->get_contract_trade_item_groups_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfContractTradeItemGroup**](SyncResultOfContractTradeItemGroup.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract_trade_item_groups_max_sequence**
> int get_contract_trade_item_groups_max_sequence()

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contract trade item groups.

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
api_instance = floriday_supplier_client.ContractTradeItemGroupsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contract trade item groups.
    api_response = api_instance.get_contract_trade_item_groups_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractTradeItemGroupsApi->get_contract_trade_item_groups_max_sequence: %s\n" % e)
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

