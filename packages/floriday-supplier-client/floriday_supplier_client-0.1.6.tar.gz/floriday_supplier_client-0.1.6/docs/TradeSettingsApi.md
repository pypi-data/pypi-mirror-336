# floriday_supplier_client.TradeSettingsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_customer_trade_settings_by_organization_id**](TradeSettingsApi.md#get_customer_trade_settings_by_organization_id) | **GET** /trade-settings/customer/{customerOrganizationId} | network:read - Returns the trade settings for a given customer.
[**get_customer_trade_settings_by_sequence_number**](TradeSettingsApi.md#get_customer_trade_settings_by_sequence_number) | **GET** /trade-settings/customer/sync/{sequenceNumber} | network:read - Returns a list of max 1000 customer trade settings starting from a specified sequence number.
[**get_customer_trade_settings_max_sequence**](TradeSettingsApi.md#get_customer_trade_settings_max_sequence) | **GET** /trade-settings/customer/max-sequence | network:read - Returns the maximum sequence number found in customer trade settings. The customer trade settings sequence differs from the supplier trade settings sequence.
[**get_supplier_trade_settings_from_organization**](TradeSettingsApi.md#get_supplier_trade_settings_from_organization) | **GET** /trade-settings/supplier/current-organization | network:read - Returns the trade settings of the current organization.

# **get_customer_trade_settings_by_organization_id**
> CustomerTradeSettings get_customer_trade_settings_by_organization_id(customer_organization_id)

network:read - Returns the trade settings for a given customer.

If the sequence is 0 that means there are no trade settings found for this customer and we have returned the defaults instead.

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
api_instance = floriday_supplier_client.TradeSettingsApi(floriday_supplier_client.ApiClient(configuration))
customer_organization_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # network:read - Returns the trade settings for a given customer.
    api_response = api_instance.get_customer_trade_settings_by_organization_id(customer_organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeSettingsApi->get_customer_trade_settings_by_organization_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_organization_id** | [**str**](.md)|  | 

### Return type

[**CustomerTradeSettings**](CustomerTradeSettings.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_trade_settings_by_sequence_number**
> SyncResultOfCustomerTradeSettings get_customer_trade_settings_by_sequence_number(sequence_number, limit_result)

network:read - Returns a list of max 1000 customer trade settings starting from a specified sequence number.

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
api_instance = floriday_supplier_client.TradeSettingsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 56 # int | 

try:
    # network:read - Returns a list of max 1000 customer trade settings starting from a specified sequence number.
    api_response = api_instance.get_customer_trade_settings_by_sequence_number(sequence_number, limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeSettingsApi->get_customer_trade_settings_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | 

### Return type

[**SyncResultOfCustomerTradeSettings**](SyncResultOfCustomerTradeSettings.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_trade_settings_max_sequence**
> int get_customer_trade_settings_max_sequence()

network:read - Returns the maximum sequence number found in customer trade settings. The customer trade settings sequence differs from the supplier trade settings sequence.

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
api_instance = floriday_supplier_client.TradeSettingsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # network:read - Returns the maximum sequence number found in customer trade settings. The customer trade settings sequence differs from the supplier trade settings sequence.
    api_response = api_instance.get_customer_trade_settings_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeSettingsApi->get_customer_trade_settings_max_sequence: %s\n" % e)
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

# **get_supplier_trade_settings_from_organization**
> SupplierTradeSettings get_supplier_trade_settings_from_organization()

network:read - Returns the trade settings of the current organization.

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
api_instance = floriday_supplier_client.TradeSettingsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # network:read - Returns the trade settings of the current organization.
    api_response = api_instance.get_supplier_trade_settings_from_organization()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeSettingsApi->get_supplier_trade_settings_from_organization: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**SupplierTradeSettings**](SupplierTradeSettings.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

