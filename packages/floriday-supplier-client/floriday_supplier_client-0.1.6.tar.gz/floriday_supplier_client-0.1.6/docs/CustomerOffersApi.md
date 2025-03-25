# floriday_supplier_client.CustomerOffersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_customer_offer**](CustomerOffersApi.md#add_customer_offer) | **POST** /customer-offers | supply:write - create a customer offer
[**delete_customer_offers**](CustomerOffersApi.md#delete_customer_offers) | **DELETE** /customer-offers/{supplyLineId} | supply:write - delete a customer offer
[**edit_customer_offer**](CustomerOffersApi.md#edit_customer_offer) | **PUT** /customer-offers/{supplyLineId} | supply:write - update a customer offer

# **add_customer_offer**
> add_customer_offer(body)

supply:write - create a customer offer

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
api_instance = floriday_supplier_client.CustomerOffersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddCustomerOffer() # AddCustomerOffer | 

try:
    # supply:write - create a customer offer
    api_instance.add_customer_offer(body)
except ApiException as e:
    print("Exception when calling CustomerOffersApi->add_customer_offer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddCustomerOffer**](AddCustomerOffer.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_customer_offers**
> delete_customer_offers(supply_line_id)

supply:write - delete a customer offer

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
api_instance = floriday_supplier_client.CustomerOffersApi(floriday_supplier_client.ApiClient(configuration))
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - delete a customer offer
    api_instance.delete_customer_offers(supply_line_id)
except ApiException as e:
    print("Exception when calling CustomerOffersApi->delete_customer_offers: %s\n" % e)
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

# **edit_customer_offer**
> edit_customer_offer(body, supply_line_id)

supply:write - update a customer offer

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
api_instance = floriday_supplier_client.CustomerOffersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditCustomerOffer() # EditCustomerOffer | 
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - update a customer offer
    api_instance.edit_customer_offer(body, supply_line_id)
except ApiException as e:
    print("Exception when calling CustomerOffersApi->edit_customer_offer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditCustomerOffer**](EditCustomerOffer.md)|  | 
 **supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

