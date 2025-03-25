# floriday_supplier_client.BundledOffersApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_bundled_offer**](BundledOffersApi.md#add_bundled_offer) | **POST** /bundled-offers | supply:write - creates a bundled offer.
[**delete_bundled_offer**](BundledOffersApi.md#delete_bundled_offer) | **DELETE** /bundled-offers/{bundledOfferId} | supply:write - delete a bundled offer
[**edit_bundled_offer**](BundledOffersApi.md#edit_bundled_offer) | **PUT** /bundled-offers/{bundledOfferId} | supply:write - update a bundled offer
[**get_bundled_offer_by_bundled_offer_line_id**](BundledOffersApi.md#get_bundled_offer_by_bundled_offer_line_id) | **GET** /bundled-offers/by-bundled-offer-line-id | supply:read - Returns a bundled offer.
[**get_bundled_offer_by_id**](BundledOffersApi.md#get_bundled_offer_by_id) | **GET** /bundled-offers/{bundledOfferId} | supply:read - Returns a bundled offer.
[**get_bundled_offers_by_sequence_number**](BundledOffersApi.md#get_bundled_offers_by_sequence_number) | **GET** /bundled-offers/sync/{sequenceNumber} | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 Bundled offers starting from a specified sequence number.
[**get_bundled_offers_max_sequence**](BundledOffersApi.md#get_bundled_offers_max_sequence) | **GET** /bundled-offers/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in bundled offers.

# **add_bundled_offer**
> add_bundled_offer(body)

supply:write - creates a bundled offer.

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddBundledOffer() # AddBundledOffer | 

try:
    # supply:write - creates a bundled offer.
    api_instance.add_bundled_offer(body)
except ApiException as e:
    print("Exception when calling BundledOffersApi->add_bundled_offer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddBundledOffer**](AddBundledOffer.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_bundled_offer**
> delete_bundled_offer(bundled_offer_id)

supply:write - delete a bundled offer

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
bundled_offer_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - delete a bundled offer
    api_instance.delete_bundled_offer(bundled_offer_id)
except ApiException as e:
    print("Exception when calling BundledOffersApi->delete_bundled_offer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bundled_offer_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_bundled_offer**
> edit_bundled_offer(body, bundled_offer_id)

supply:write - update a bundled offer

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditBundledOffer() # EditBundledOffer | 
bundled_offer_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - update a bundled offer
    api_instance.edit_bundled_offer(body, bundled_offer_id)
except ApiException as e:
    print("Exception when calling BundledOffersApi->edit_bundled_offer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditBundledOffer**](EditBundledOffer.md)|  | 
 **bundled_offer_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_bundled_offer_by_bundled_offer_line_id**
> BundledOffer get_bundled_offer_by_bundled_offer_line_id(bundled_offer_line_id)

supply:read - Returns a bundled offer.

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
bundled_offer_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a bundled offer.
    api_response = api_instance.get_bundled_offer_by_bundled_offer_line_id(bundled_offer_line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BundledOffersApi->get_bundled_offer_by_bundled_offer_line_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bundled_offer_line_id** | [**str**](.md)|  | 

### Return type

[**BundledOffer**](BundledOffer.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_bundled_offer_by_id**
> BundledOffer get_bundled_offer_by_id(bundled_offer_id)

supply:read - Returns a bundled offer.

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
bundled_offer_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a bundled offer.
    api_response = api_instance.get_bundled_offer_by_id(bundled_offer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BundledOffersApi->get_bundled_offer_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bundled_offer_id** | [**str**](.md)|  | 

### Return type

[**BundledOffer**](BundledOffer.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_bundled_offers_by_sequence_number**
> SyncResultOfBundledOffer get_bundled_offers_by_sequence_number(sequence_number, limit_result=limit_result)

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 Bundled offers starting from a specified sequence number.

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 Bundled offers starting from a specified sequence number.
    api_response = api_instance.get_bundled_offers_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BundledOffersApi->get_bundled_offers_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfBundledOffer**](SyncResultOfBundledOffer.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_bundled_offers_max_sequence**
> int get_bundled_offers_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in bundled offers.

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
api_instance = floriday_supplier_client.BundledOffersApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in bundled offers.
    api_response = api_instance.get_bundled_offers_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BundledOffersApi->get_bundled_offers_max_sequence: %s\n" % e)
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

