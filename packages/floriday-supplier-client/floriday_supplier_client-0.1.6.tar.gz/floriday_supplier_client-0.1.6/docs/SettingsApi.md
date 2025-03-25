# floriday_supplier_client.SettingsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**set_florecom_order_messages_deactivated**](SettingsApi.md#set_florecom_order_messages_deactivated) | **PATCH** /settings/deactivate-florecom-order-messages | fulfillment:write - Deactivates Florecom order/orderresponse messages

# **set_florecom_order_messages_deactivated**
> set_florecom_order_messages_deactivated()

fulfillment:write - Deactivates Florecom order/orderresponse messages

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
api_instance = floriday_supplier_client.SettingsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # fulfillment:write - Deactivates Florecom order/orderresponse messages
    api_instance.set_florecom_order_messages_deactivated()
except ApiException as e:
    print("Exception when calling SettingsApi->set_florecom_order_messages_deactivated: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

