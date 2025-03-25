# floriday_supplier_client.WeeklySupplyLineCountersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_weekly_supply_line_counter**](WeeklySupplyLineCountersApi.md#add_weekly_supply_line_counter) | **POST** /weekly-supply-line-counters | supply:write - Creates a new WeeklySupplyLineCounter.
[**add_weekly_supply_line_counter_to_supply_line**](WeeklySupplyLineCountersApi.md#add_weekly_supply_line_counter_to_supply_line) | **PATCH** /weekly-supply-line-counters/{weeklySupplyLineCounterId}/add-to-supplyline/{supplyLineId} | supply:write - Links the supply line to the WeeklySupplyLineCounter. The &#x60;numberOfPieces&#x60; in the supply line will be based on the counter.
[**delete_weekly_supply_line_counter**](WeeklySupplyLineCountersApi.md#delete_weekly_supply_line_counter) | **DELETE** /weekly-supply-line-counters/{weeklySupplyLineCounterId} | supply:write - Deletes the WeeklySupplyLineCounter and removes all the supply line links.
[**get_weekly_supply_line_counter_by_id**](WeeklySupplyLineCountersApi.md#get_weekly_supply_line_counter_by_id) | **GET** /weekly-supply-line-counters/{weeklySupplyLineCounterId} | supply:read - Returns the WeeklySupplyLineCounters by id.
[**get_weekly_supply_line_counters**](WeeklySupplyLineCountersApi.md#get_weekly_supply_line_counters) | **GET** /weekly-supply-line-counters | supply:read - Returns all available WeeklySupplyLineCounters created via the Suppliers API.
[**remove_weekly_supply_line_counter_from_supply_line**](WeeklySupplyLineCountersApi.md#remove_weekly_supply_line_counter_from_supply_line) | **PATCH** /weekly-supply-line-counters/{weeklySupplyLineCounterId}/remove-from-supplyline/{supplyLineId} | supply:write - Removes the supply line from the WeeklySupplyLineCounter.

# **add_weekly_supply_line_counter**
> add_weekly_supply_line_counter(body)

supply:write - Creates a new WeeklySupplyLineCounter.

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WeeklySupplyLineCounterCreate() # WeeklySupplyLineCounterCreate | 

try:
    # supply:write - Creates a new WeeklySupplyLineCounter.
    api_instance.add_weekly_supply_line_counter(body)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->add_weekly_supply_line_counter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WeeklySupplyLineCounterCreate**](WeeklySupplyLineCounterCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_weekly_supply_line_counter_to_supply_line**
> add_weekly_supply_line_counter_to_supply_line(weekly_supply_line_counter_id, supply_line_id)

supply:write - Links the supply line to the WeeklySupplyLineCounter. The `numberOfPieces` in the supply line will be based on the counter.

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_supply_line_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Links the supply line to the WeeklySupplyLineCounter. The `numberOfPieces` in the supply line will be based on the counter.
    api_instance.add_weekly_supply_line_counter_to_supply_line(weekly_supply_line_counter_id, supply_line_id)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->add_weekly_supply_line_counter_to_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_supply_line_counter_id** | [**str**](.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_weekly_supply_line_counter**
> delete_weekly_supply_line_counter(weekly_supply_line_counter_id)

supply:write - Deletes the WeeklySupplyLineCounter and removes all the supply line links.

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_supply_line_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Deletes the WeeklySupplyLineCounter and removes all the supply line links.
    api_instance.delete_weekly_supply_line_counter(weekly_supply_line_counter_id)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->delete_weekly_supply_line_counter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_supply_line_counter_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_supply_line_counter_by_id**
> WeeklySupplyLineCounter get_weekly_supply_line_counter_by_id(weekly_supply_line_counter_id)

supply:read - Returns the WeeklySupplyLineCounters by id.

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_supply_line_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns the WeeklySupplyLineCounters by id.
    api_response = api_instance.get_weekly_supply_line_counter_by_id(weekly_supply_line_counter_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->get_weekly_supply_line_counter_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_supply_line_counter_id** | [**str**](.md)|  | 

### Return type

[**WeeklySupplyLineCounter**](WeeklySupplyLineCounter.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_supply_line_counters**
> list[WeeklySupplyLineCounter] get_weekly_supply_line_counters()

supply:read - Returns all available WeeklySupplyLineCounters created via the Suppliers API.

WeeklySupplyLineCounters are used to create a countdown in the supply lines. The `numberOfPieces` in the supply line will be linked to the counter

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - Returns all available WeeklySupplyLineCounters created via the Suppliers API.
    api_response = api_instance.get_weekly_supply_line_counters()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->get_weekly_supply_line_counters: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[WeeklySupplyLineCounter]**](WeeklySupplyLineCounter.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_weekly_supply_line_counter_from_supply_line**
> remove_weekly_supply_line_counter_from_supply_line(weekly_supply_line_counter_id, supply_line_id)

supply:write - Removes the supply line from the WeeklySupplyLineCounter.

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
api_instance = floriday_supplier_client.WeeklySupplyLineCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_supply_line_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Removes the supply line from the WeeklySupplyLineCounter.
    api_instance.remove_weekly_supply_line_counter_from_supply_line(weekly_supply_line_counter_id, supply_line_id)
except ApiException as e:
    print("Exception when calling WeeklySupplyLineCountersApi->remove_weekly_supply_line_counter_from_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_supply_line_counter_id** | [**str**](.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

