# floriday_supplier_client.WebhooksApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_webhook_subscription**](WebhooksApi.md#add_webhook_subscription) | **POST** /webhooks/subscriptions | webhooks:write - Subscribe to a events webhook.
[**delete_webhook_subscription**](WebhooksApi.md#delete_webhook_subscription) | **DELETE** /webhooks/subscriptions | webhooks:write - Delete a events webhook.

# **add_webhook_subscription**
> Event add_webhook_subscription(body)

webhooks:write - Subscribe to a events webhook.

The Events will be POSTed to the specified URL.                             Events are published for these aggregateTypes:                             - SALESORDER                             - BATCH                             - DELIVERYORDER                             - FULFILLMENTORDER

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
api_instance = floriday_supplier_client.WebhooksApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WebhookSubscription() # WebhookSubscription | 

try:
    # webhooks:write - Subscribe to a events webhook.
    api_response = api_instance.add_webhook_subscription(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WebhooksApi->add_webhook_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WebhookSubscription**](WebhookSubscription.md)|  | 

### Return type

[**Event**](Event.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_webhook_subscription**
> delete_webhook_subscription(body)

webhooks:write - Delete a events webhook.

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
api_instance = floriday_supplier_client.WebhooksApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.WebhookSubscription() # WebhookSubscription | 

try:
    # webhooks:write - Delete a events webhook.
    api_instance.delete_webhook_subscription(body)
except ApiException as e:
    print("Exception when calling WebhooksApi->delete_webhook_subscription: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WebhookSubscription**](WebhookSubscription.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

