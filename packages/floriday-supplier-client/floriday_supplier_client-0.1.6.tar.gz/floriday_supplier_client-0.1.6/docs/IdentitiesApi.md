# floriday_supplier_client.IdentitiesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_identity**](IdentitiesApi.md#get_identity) | **GET** /auth/key | Provides the identity associated with an api key.

# **get_identity**
> Identity get_identity()

Provides the identity associated with an api key.

Use this endpoint to check the identity keys associated with an api key.

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
api_instance = floriday_supplier_client.IdentitiesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # Provides the identity associated with an api key.
    api_response = api_instance.get_identity()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentitiesApi->get_identity: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Identity**](Identity.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

