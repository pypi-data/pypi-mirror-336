# floriday_supplier_client.CatalogPricesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_weekly_supply_line**](CatalogPricesApi.md#add_weekly_supply_line) | **POST** /weekly-supply-lines | supply:write - Creates a new weekly supply line for trade item.
[**delete_weekly_supply_lines**](CatalogPricesApi.md#delete_weekly_supply_lines) | **DELETE** /weekly-supply-lines/{supplyLineId} | supply:write - Deletes a weekly supply line.
[**edit_continuous_stock**](CatalogPricesApi.md#edit_continuous_stock) | **PUT** /trade-items/{tradeItemId}/continuous-stock | supply:write - rate limit: 10 per second - burst limit: 1000 - Set availabilities for a trade item
[**edit_weekly_base_supply**](CatalogPricesApi.md#edit_weekly_base_supply) | **PUT** /trade-items/{tradeItemId}/base-supply/{year}/{week} | supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines based on pre-entered price groups.
[**edit_weekly_base_supply_lines**](CatalogPricesApi.md#edit_weekly_base_supply_lines) | **PUT** /trade-items/base-supply/{year}/{week} | supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines for multiple trade items based on calculated and manual price groups.
[**edit_weekly_supply_line**](CatalogPricesApi.md#edit_weekly_supply_line) | **PUT** /weekly-supply-lines/{supplyLineId} | supply:write - Updates a weekly supply line for trade item.
[**get_continuous_stock**](CatalogPricesApi.md#get_continuous_stock) | **GET** /trade-items/{tradeItemId}/continuous-stock | supply:read - Returns the availability of a trade item.
[**get_trade_item_availabilities**](CatalogPricesApi.md#get_trade_item_availabilities) | **GET** /trade-items/availabilities | supply:read - rate limit: 2 per second - burst limit: 200 - Returns the current availability of all trade items.
[**get_trade_item_availabilities_by_sequence_number**](CatalogPricesApi.md#get_trade_item_availabilities_by_sequence_number) | **GET** /trade-items/availabilities/sync/{sequenceNumber} | supply:read - Returns a list of max 1000 trade item availabilities starting from a specified sequence number.
[**get_trade_item_availabilities_max_sequence**](CatalogPricesApi.md#get_trade_item_availabilities_max_sequence) | **GET** /trade-items/availabilities/current-max-sequence | supply:read - Returns the maximum sequence number found in trade item availabilities.
[**get_weekly_base_supplies**](CatalogPricesApi.md#get_weekly_base_supplies) | **GET** /trade-items/base-supply | supply:read - rate limit: 1 per second - burst limit: 20 - Returns the base supply per year/week for trade items.
[**set_trade_item_warehouse**](CatalogPricesApi.md#set_trade_item_warehouse) | **PATCH** /trade-items/{tradeItemId}/warehouse | supply:write - Add a warehouse for a trade item ( only continuous stock )
[**set_weekly_base_supply_number_of_pieces**](CatalogPricesApi.md#set_weekly_base_supply_number_of_pieces) | **PATCH** /trade-items/{tradeItemId}/base-supply/{year}/{week} | supply:write - rate limit: 10 per second - burst limit: 1000 - Patch the number of pieces of an existing base supply.

# **add_weekly_supply_line**
> add_weekly_supply_line(body)

supply:write - Creates a new weekly supply line for trade item.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WeeklySupplyLine() # WeeklySupplyLine | 

try:
    # supply:write - Creates a new weekly supply line for trade item.
    api_instance.add_weekly_supply_line(body)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->add_weekly_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WeeklySupplyLine**](WeeklySupplyLine.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_weekly_supply_lines**
> delete_weekly_supply_lines(supply_line_id)

supply:write - Deletes a weekly supply line.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Deletes a weekly supply line.
    api_instance.delete_weekly_supply_lines(supply_line_id)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->delete_weekly_supply_lines: %s\n" % e)
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

# **edit_continuous_stock**
> edit_continuous_stock(body, trade_item_id)

supply:write - rate limit: 10 per second - burst limit: 1000 - Set availabilities for a trade item

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.ContinuousStock() # ContinuousStock | 
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - rate limit: 10 per second - burst limit: 1000 - Set availabilities for a trade item
    api_instance.edit_continuous_stock(body, trade_item_id)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->edit_continuous_stock: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContinuousStock**](ContinuousStock.md)|  | 
 **trade_item_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_weekly_base_supply**
> edit_weekly_base_supply(body, trade_item_id, year, week)

supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines based on pre-entered price groups.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WeeklyBaseSupplyCreate() # WeeklyBaseSupplyCreate | 
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
year = 56 # int | 
week = 56 # int | 

try:
    # supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines based on pre-entered price groups.
    api_instance.edit_weekly_base_supply(body, trade_item_id, year, week)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->edit_weekly_base_supply: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WeeklyBaseSupplyCreate**](WeeklyBaseSupplyCreate.md)|  | 
 **trade_item_id** | [**str**](.md)|  | 
 **year** | **int**|  | 
 **week** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_weekly_base_supply_lines**
> edit_weekly_base_supply_lines(body, year, week)

supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines for multiple trade items based on calculated and manual price groups.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
body = [floriday_supplier_client.EditWeeklyBaseSupplyLines()] # list[EditWeeklyBaseSupplyLines] | 
year = 56 # int | 
week = 56 # int | 

try:
    # supply:write - rate limit: 10 per second - burst limit: 1000 - Generates new weekly supply lines for multiple trade items based on calculated and manual price groups.
    api_instance.edit_weekly_base_supply_lines(body, year, week)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->edit_weekly_base_supply_lines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[EditWeeklyBaseSupplyLines]**](EditWeeklyBaseSupplyLines.md)|  | 
 **year** | **int**|  | 
 **week** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_weekly_supply_line**
> edit_weekly_supply_line(body, supply_line_id)

supply:write - Updates a weekly supply line for trade item.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WeeklySupplyLineUpdate() # WeeklySupplyLineUpdate | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Updates a weekly supply line for trade item.
    api_instance.edit_weekly_supply_line(body, supply_line_id)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->edit_weekly_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WeeklySupplyLineUpdate**](WeeklySupplyLineUpdate.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_continuous_stock**
> ContinuousStock get_continuous_stock(trade_item_id)

supply:read - Returns the availability of a trade item.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns the availability of a trade item.
    api_response = api_instance.get_continuous_stock(trade_item_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->get_continuous_stock: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 

### Return type

[**ContinuousStock**](ContinuousStock.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_availabilities**
> list[TradeItemAvailability] get_trade_item_availabilities()

supply:read - rate limit: 2 per second - burst limit: 200 - Returns the current availability of all trade items.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 2 per second - burst limit: 200 - Returns the current availability of all trade items.
    api_response = api_instance.get_trade_item_availabilities()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->get_trade_item_availabilities: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[TradeItemAvailability]**](TradeItemAvailability.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_availabilities_by_sequence_number**
> SyncResultOfTradeItemAvailability get_trade_item_availabilities_by_sequence_number(sequence_number, limit=limit)

supply:read - Returns a list of max 1000 trade item availabilities starting from a specified sequence number.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - Returns a list of max 1000 trade item availabilities starting from a specified sequence number.
    api_response = api_instance.get_trade_item_availabilities_by_sequence_number(sequence_number, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->get_trade_item_availabilities_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfTradeItemAvailability**](SyncResultOfTradeItemAvailability.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_item_availabilities_max_sequence**
> int get_trade_item_availabilities_max_sequence()

supply:read - Returns the maximum sequence number found in trade item availabilities.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - Returns the maximum sequence number found in trade item availabilities.
    api_response = api_instance.get_trade_item_availabilities_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->get_trade_item_availabilities_max_sequence: %s\n" % e)
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

# **get_weekly_base_supplies**
> list[WeeklyBaseSupply] get_weekly_base_supplies(year, week)

supply:read - rate limit: 1 per second - burst limit: 20 - Returns the base supply per year/week for trade items.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
year = 56 # int | 
week = 56 # int | 

try:
    # supply:read - rate limit: 1 per second - burst limit: 20 - Returns the base supply per year/week for trade items.
    api_response = api_instance.get_weekly_base_supplies(year, week)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->get_weekly_base_supplies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 
 **week** | **int**|  | 

### Return type

[**list[WeeklyBaseSupply]**](WeeklyBaseSupply.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_trade_item_warehouse**
> set_trade_item_warehouse(trade_item_id, warehouse_id)

supply:write - Add a warehouse for a trade item ( only continuous stock )

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
warehouse_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Add a warehouse for a trade item ( only continuous stock )
    api_instance.set_trade_item_warehouse(trade_item_id, warehouse_id)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->set_trade_item_warehouse: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 
 **warehouse_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_weekly_base_supply_number_of_pieces**
> set_weekly_base_supply_number_of_pieces(trade_item_id, year, week, number_of_pieces=number_of_pieces)

supply:write - rate limit: 10 per second - burst limit: 1000 - Patch the number of pieces of an existing base supply.

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
api_instance = floriday_supplier_client.CatalogPricesApi(floriday_supplier_client.ApiClient(configuration))
trade_item_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 
year = 56 # int | 
week = 56 # int | 
number_of_pieces = 56 # int |  (optional)

try:
    # supply:write - rate limit: 10 per second - burst limit: 1000 - Patch the number of pieces of an existing base supply.
    api_instance.set_weekly_base_supply_number_of_pieces(trade_item_id, year, week, number_of_pieces=number_of_pieces)
except ApiException as e:
    print("Exception when calling CatalogPricesApi->set_weekly_base_supply_number_of_pieces: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trade_item_id** | [**str**](.md)|  | 
 **year** | **int**|  | 
 **week** | **int**|  | 
 **number_of_pieces** | **int**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

