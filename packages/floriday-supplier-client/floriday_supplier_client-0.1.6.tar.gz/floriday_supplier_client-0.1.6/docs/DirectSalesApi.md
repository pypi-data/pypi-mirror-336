# floriday_supplier_client.DirectSalesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_supply_line**](DirectSalesApi.md#add_supply_line) | **POST** /supply-lines | supply:write - Create a supply line with type BATCH_PRICE
[**delete_supply_line**](DirectSalesApi.md#delete_supply_line) | **DELETE** /supply-lines/{supplyLineId} | supply:write - Delete a supply line
[**edit_base_supply**](DirectSalesApi.md#edit_base_supply) | **PUT** /batches/{batchId}/base-supply | supply:write - Set base supply for a batch. Supply lines will be generated based on pre-entered price groups.
[**get_supply_line_by_id**](DirectSalesApi.md#get_supply_line_by_id) | **GET** /supply-lines/{supplyLineId} | supply:read - Returns a supply line.
[**get_supply_lines**](DirectSalesApi.md#get_supply_lines) | **GET** /supply-lines | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns supply lines created within the given timeframe
[**get_supply_lines_by_sequence_number**](DirectSalesApi.md#get_supply_lines_by_sequence_number) | **GET** /supply-lines/sync/{sequenceNumber} | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 supply lines starting from a specified sequence number.
[**get_supply_lines_max_sequence**](DirectSalesApi.md#get_supply_lines_max_sequence) | **GET** /supply-lines/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in supply lines.
[**set_supply_line_price**](DirectSalesApi.md#set_supply_line_price) | **PATCH** /supply-lines/{supplyLineId}/price | supply:write - Update the price of the supply line with type BATCH_PRICE.
[**set_supply_line_status**](DirectSalesApi.md#set_supply_line_status) | **PATCH** /supply-lines/{supplyLineId}/status | supply:write - Update the status of the supply line with type BATCH_PRICE.

# **add_supply_line**
> add_supply_line(body)

supply:write - Create a supply line with type BATCH_PRICE

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SupplyLineCreate() # SupplyLineCreate | 

try:
    # supply:write - Create a supply line with type BATCH_PRICE
    api_instance.add_supply_line(body)
except ApiException as e:
    print("Exception when calling DirectSalesApi->add_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SupplyLineCreate**](SupplyLineCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_supply_line**
> delete_supply_line(supply_line_id)

supply:write - Delete a supply line

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Delete a supply line
    api_instance.delete_supply_line(supply_line_id)
except ApiException as e:
    print("Exception when calling DirectSalesApi->delete_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_base_supply**
> edit_base_supply(body, batch_id)

supply:write - Set base supply for a batch. Supply lines will be generated based on pre-entered price groups.

After entering the base price, Floriday will create multiple supply lines based on a variety of settings within Floriday.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.BaseSupply() # BaseSupply | 
batch_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Set base supply for a batch. Supply lines will be generated based on pre-entered price groups.
    api_instance.edit_base_supply(body, batch_id)
except ApiException as e:
    print("Exception when calling DirectSalesApi->edit_base_supply: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BaseSupply**](BaseSupply.md)|  | 
 **batch_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_line_by_id**
> SupplyLine get_supply_line_by_id(supply_line_id)

supply:read - Returns a supply line.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a supply line.
    api_response = api_instance.get_supply_line_by_id(supply_line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectSalesApi->get_supply_line_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_line_id** | [**str**](.md)|  | 

### Return type

[**SupplyLine**](SupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_lines**
> list[SupplyLine] get_supply_lines(start_date_time=start_date_time, end_date_time=end_date_time, batch_id=batch_id, limit_result=limit_result)

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns supply lines created within the given timeframe

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
start_date_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
end_date_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
batch_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str |  (optional)
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns supply lines created within the given timeframe
    api_response = api_instance.get_supply_lines(start_date_time=start_date_time, end_date_time=end_date_time, batch_id=batch_id, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectSalesApi->get_supply_lines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date_time** | **datetime**|  | [optional] 
 **end_date_time** | **datetime**|  | [optional] 
 **batch_id** | [**str**](.md)|  | [optional] 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**list[SupplyLine]**](SupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_lines_by_sequence_number**
> SyncResultOfSupplyLine get_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 supply lines starting from a specified sequence number.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 supply lines starting from a specified sequence number.
    api_response = api_instance.get_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectSalesApi->get_supply_lines_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfSupplyLine**](SyncResultOfSupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_lines_max_sequence**
> int get_supply_lines_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in supply lines.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in supply lines.
    api_response = api_instance.get_supply_lines_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DirectSalesApi->get_supply_lines_max_sequence: %s\n" % e)
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

# **set_supply_line_price**
> set_supply_line_price(body, supply_line_id)

supply:write - Update the price of the supply line with type BATCH_PRICE.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SupplyLinePriceUpdate() # SupplyLinePriceUpdate | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Update the price of the supply line with type BATCH_PRICE.
    api_instance.set_supply_line_price(body, supply_line_id)
except ApiException as e:
    print("Exception when calling DirectSalesApi->set_supply_line_price: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SupplyLinePriceUpdate**](SupplyLinePriceUpdate.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_supply_line_status**
> set_supply_line_status(body, supply_line_id)

supply:write - Update the status of the supply line with type BATCH_PRICE.

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
api_instance = floriday_supplier_client.DirectSalesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.SupplyAvailabilityStatus() # SupplyAvailabilityStatus | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Update the status of the supply line with type BATCH_PRICE.
    api_instance.set_supply_line_status(body, supply_line_id)
except ApiException as e:
    print("Exception when calling DirectSalesApi->set_supply_line_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SupplyAvailabilityStatus**](SupplyAvailabilityStatus.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

