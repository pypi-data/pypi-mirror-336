# floriday_supplier_client.DeliveryLocationsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_delivery_location_max_sequence**](DeliveryLocationsApi.md#get_delivery_location_max_sequence) | **GET** /delivery-locations/current-max-sequence | organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.
[**get_delivery_locations_by_sequence_number**](DeliveryLocationsApi.md#get_delivery_locations_by_sequence_number) | **GET** /delivery-locations/sync/{sequenceNumber} | organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 customer delivery locations starting from a specified sequence number.

# **get_delivery_location_max_sequence**
> int get_delivery_location_max_sequence()

organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.

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
api_instance = floriday_supplier_client.DeliveryLocationsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns the maximum sequence number found in warehouses.
    api_response = api_instance.get_delivery_location_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryLocationsApi->get_delivery_location_max_sequence: %s\n" % e)
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

# **get_delivery_locations_by_sequence_number**
> SyncResultOfDeliveryLocation get_delivery_locations_by_sequence_number(sequence_number, limit_result=limit_result)

organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 customer delivery locations starting from a specified sequence number.

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
api_instance = floriday_supplier_client.DeliveryLocationsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 customer delivery locations starting from a specified sequence number.
    api_response = api_instance.get_delivery_locations_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryLocationsApi->get_delivery_locations_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfDeliveryLocation**](SyncResultOfDeliveryLocation.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

