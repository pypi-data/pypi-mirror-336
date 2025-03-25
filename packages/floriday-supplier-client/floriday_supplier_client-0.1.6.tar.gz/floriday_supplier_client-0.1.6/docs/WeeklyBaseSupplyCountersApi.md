# floriday_supplier_client.WeeklyBaseSupplyCountersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_weekly_base_supply_counter_template_to_trade_item_async**](WeeklyBaseSupplyCountersApi.md#add_weekly_base_supply_counter_template_to_trade_item_async) | **PUT** /weekly-base-supply-counters/templates/{weeklyBaseSupplyCounterTemplateId}/add-to-trade-item | supply:write - Add WeeklyBaseSupplyCounterTemplate to trade item.
[**claim_number_of_pieces_from_weekly_base_supply_counter**](WeeklyBaseSupplyCountersApi.md#claim_number_of_pieces_from_weekly_base_supply_counter) | **PUT** /weekly-base-supply-counters/claim/{weeklyBaseSupplyCounterId} | supply:write - Claim NumberOfPieces from weekly base supply counter.
[**delete_weekly_base_supply_counter_template**](WeeklyBaseSupplyCountersApi.md#delete_weekly_base_supply_counter_template) | **DELETE** /weekly-base-supply-counters/templates/{weeklyBaseSupplyCounterTemplateId} | supply:write - Delete weekly base supply counter template.
[**get_weekly_base_supply_counter**](WeeklyBaseSupplyCountersApi.md#get_weekly_base_supply_counter) | **GET** /weekly-base-supply-counters/{weeklyBaseSupplyCounterId} | supply:read - Returns a weekly base supply counter.
[**get_weekly_base_supply_counter_by_template_id**](WeeklyBaseSupplyCountersApi.md#get_weekly_base_supply_counter_by_template_id) | **GET** /weekly-base-supply-counters/by-template-id/{weeklyBaseSupplyCounterTemplateId} | supply:read - Returns weekly base supply counters by templateId.
[**get_weekly_base_supply_template_by_id**](WeeklyBaseSupplyCountersApi.md#get_weekly_base_supply_template_by_id) | **GET** /weekly-base-supply-counters/templates/{weeklyBaseSupplyCounterTemplateId} | supply:read - Returns a weekly base supply counter template.
[**get_weekly_base_supply_templates**](WeeklyBaseSupplyCountersApi.md#get_weekly_base_supply_templates) | **GET** /weekly-base-supply-counters/templates | supply:read - Returns weekly base supply counter templates.
[**upsert_weekly_base_supply_counter_template**](WeeklyBaseSupplyCountersApi.md#upsert_weekly_base_supply_counter_template) | **PUT** /weekly-base-supply-counters/templates | supply:write - Upsert weekly base supply counter template.

# **add_weekly_base_supply_counter_template_to_trade_item_async**
> add_weekly_base_supply_counter_template_to_trade_item_async(body, weekly_base_supply_counter_template_id)

supply:write - Add WeeklyBaseSupplyCounterTemplate to trade item.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WeeklyBaseSupplyCounterTemplateToTradeItem() # WeeklyBaseSupplyCounterTemplateToTradeItem | 
weekly_base_supply_counter_template_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Add WeeklyBaseSupplyCounterTemplate to trade item.
    api_instance.add_weekly_base_supply_counter_template_to_trade_item_async(body, weekly_base_supply_counter_template_id)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->add_weekly_base_supply_counter_template_to_trade_item_async: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WeeklyBaseSupplyCounterTemplateToTradeItem**](WeeklyBaseSupplyCounterTemplateToTradeItem.md)|  | 
 **weekly_base_supply_counter_template_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **claim_number_of_pieces_from_weekly_base_supply_counter**
> claim_number_of_pieces_from_weekly_base_supply_counter(body, weekly_base_supply_counter_id)

supply:write - Claim NumberOfPieces from weekly base supply counter.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.ClaimFromWeeklyBaseSupplyCounter() # ClaimFromWeeklyBaseSupplyCounter | 
weekly_base_supply_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Claim NumberOfPieces from weekly base supply counter.
    api_instance.claim_number_of_pieces_from_weekly_base_supply_counter(body, weekly_base_supply_counter_id)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->claim_number_of_pieces_from_weekly_base_supply_counter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ClaimFromWeeklyBaseSupplyCounter**](ClaimFromWeeklyBaseSupplyCounter.md)|  | 
 **weekly_base_supply_counter_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_weekly_base_supply_counter_template**
> delete_weekly_base_supply_counter_template(weekly_base_supply_counter_template_id)

supply:write - Delete weekly base supply counter template.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_base_supply_counter_template_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Delete weekly base supply counter template.
    api_instance.delete_weekly_base_supply_counter_template(weekly_base_supply_counter_template_id)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->delete_weekly_base_supply_counter_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_base_supply_counter_template_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_base_supply_counter**
> WeeklyBaseSupplyCounter get_weekly_base_supply_counter(weekly_base_supply_counter_id)

supply:read - Returns a weekly base supply counter.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_base_supply_counter_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a weekly base supply counter.
    api_response = api_instance.get_weekly_base_supply_counter(weekly_base_supply_counter_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->get_weekly_base_supply_counter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_base_supply_counter_id** | [**str**](.md)|  | 

### Return type

[**WeeklyBaseSupplyCounter**](WeeklyBaseSupplyCounter.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_base_supply_counter_by_template_id**
> list[WeeklyBaseSupplyCounter] get_weekly_base_supply_counter_by_template_id(weekly_base_supply_counter_template_id)

supply:read - Returns weekly base supply counters by templateId.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_base_supply_counter_template_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns weekly base supply counters by templateId.
    api_response = api_instance.get_weekly_base_supply_counter_by_template_id(weekly_base_supply_counter_template_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->get_weekly_base_supply_counter_by_template_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_base_supply_counter_template_id** | [**str**](.md)|  | 

### Return type

[**list[WeeklyBaseSupplyCounter]**](WeeklyBaseSupplyCounter.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_base_supply_template_by_id**
> WeeklyBaseSupplyCounterTemplate get_weekly_base_supply_template_by_id(weekly_base_supply_counter_template_id)

supply:read - Returns a weekly base supply counter template.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
weekly_base_supply_counter_template_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a weekly base supply counter template.
    api_response = api_instance.get_weekly_base_supply_template_by_id(weekly_base_supply_counter_template_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->get_weekly_base_supply_template_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **weekly_base_supply_counter_template_id** | [**str**](.md)|  | 

### Return type

[**WeeklyBaseSupplyCounterTemplate**](WeeklyBaseSupplyCounterTemplate.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_weekly_base_supply_templates**
> list[WeeklyBaseSupplyCounterTemplate] get_weekly_base_supply_templates()

supply:read - Returns weekly base supply counter templates.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - Returns weekly base supply counter templates.
    api_response = api_instance.get_weekly_base_supply_templates()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->get_weekly_base_supply_templates: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[WeeklyBaseSupplyCounterTemplate]**](WeeklyBaseSupplyCounterTemplate.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upsert_weekly_base_supply_counter_template**
> upsert_weekly_base_supply_counter_template(body)

supply:write - Upsert weekly base supply counter template.

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
api_instance = floriday_supplier_client.WeeklyBaseSupplyCountersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditWeeklyBaseSupplyCounterTemplate() # EditWeeklyBaseSupplyCounterTemplate | 

try:
    # supply:write - Upsert weekly base supply counter template.
    api_instance.upsert_weekly_base_supply_counter_template(body)
except ApiException as e:
    print("Exception when calling WeeklyBaseSupplyCountersApi->upsert_weekly_base_supply_counter_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditWeeklyBaseSupplyCounterTemplate**](EditWeeklyBaseSupplyCounterTemplate.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

