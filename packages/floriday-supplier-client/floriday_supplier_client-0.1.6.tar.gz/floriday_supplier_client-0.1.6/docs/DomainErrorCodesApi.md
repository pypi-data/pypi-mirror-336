# floriday_supplier_client.DomainErrorCodesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_domain_error_codes**](DomainErrorCodesApi.md#get_domain_error_codes) | **GET** /domain-error-codes | - Returns all domain error codes.

# **get_domain_error_codes**
> list[DomainErrorCode] get_domain_error_codes()

- Returns all domain error codes.

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
api_instance = floriday_supplier_client.DomainErrorCodesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # - Returns all domain error codes.
    api_response = api_instance.get_domain_error_codes()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DomainErrorCodesApi->get_domain_error_codes: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DomainErrorCode]**](DomainErrorCode.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

