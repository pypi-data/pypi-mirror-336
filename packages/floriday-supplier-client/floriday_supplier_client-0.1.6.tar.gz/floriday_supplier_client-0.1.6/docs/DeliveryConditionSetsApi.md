# floriday_supplier_client.DeliveryConditionSetsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_delivery_condition_set_by_id**](DeliveryConditionSetsApi.md#get_delivery_condition_set_by_id) | **GET** /delivery-condition-sets/{deliveryConditionSetId} | delivery-conditions:read - Returns a delivery condition set.
[**get_delivery_condition_sets**](DeliveryConditionSetsApi.md#get_delivery_condition_sets) | **GET** /delivery-condition-sets | delivery-conditions:read - Returns delivery condition sets.
[**get_delivery_condition_sets_by_sequence_number**](DeliveryConditionSetsApi.md#get_delivery_condition_sets_by_sequence_number) | **GET** /delivery-condition-sets/sync/{sequenceNumber} | delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 delivery condition sets starting from a specified sequence number.
[**get_delivery_condition_sets_max_sequence**](DeliveryConditionSetsApi.md#get_delivery_condition_sets_max_sequence) | **GET** /delivery-condition-sets/current-max-sequence | delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery condition sets.

# **get_delivery_condition_set_by_id**
> DeliveryConditionSet get_delivery_condition_set_by_id(delivery_condition_set_id)

delivery-conditions:read - Returns a delivery condition set.

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
api_instance = floriday_supplier_client.DeliveryConditionSetsApi(floriday_supplier_client.ApiClient(configuration))
delivery_condition_set_id = 'delivery_condition_set_id_example' # str | 

try:
    # delivery-conditions:read - Returns a delivery condition set.
    api_response = api_instance.get_delivery_condition_set_by_id(delivery_condition_set_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryConditionSetsApi->get_delivery_condition_set_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_condition_set_id** | **str**|  | 

### Return type

[**DeliveryConditionSet**](DeliveryConditionSet.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_condition_sets**
> list[DeliveryConditionSet] get_delivery_condition_sets()

delivery-conditions:read - Returns delivery condition sets.

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
api_instance = floriday_supplier_client.DeliveryConditionSetsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # delivery-conditions:read - Returns delivery condition sets.
    api_response = api_instance.get_delivery_condition_sets()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryConditionSetsApi->get_delivery_condition_sets: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DeliveryConditionSet]**](DeliveryConditionSet.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_condition_sets_by_sequence_number**
> SyncResultOfDeliveryConditionSet get_delivery_condition_sets_by_sequence_number(sequence_number, limit_result=limit_result)

delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 delivery condition sets starting from a specified sequence number.

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
api_instance = floriday_supplier_client.DeliveryConditionSetsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 100 # int |  (optional) (default to 100)

try:
    # delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 delivery condition sets starting from a specified sequence number.
    api_response = api_instance.get_delivery_condition_sets_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryConditionSetsApi->get_delivery_condition_sets_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 100]

### Return type

[**SyncResultOfDeliveryConditionSet**](SyncResultOfDeliveryConditionSet.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_condition_sets_max_sequence**
> int get_delivery_condition_sets_max_sequence()

delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery condition sets.

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
api_instance = floriday_supplier_client.DeliveryConditionSetsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # delivery-conditions:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in delivery condition sets.
    api_response = api_instance.get_delivery_condition_sets_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryConditionSetsApi->get_delivery_condition_sets_max_sequence: %s\n" % e)
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

