# floriday_supplier_client.BatchesApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_batch**](BatchesApi.md#add_batch) | **POST** /batches | fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a batch.
[**combine_and_transform_batches**](BatchesApi.md#combine_and_transform_batches) | **POST** /batches/combine-and-transform | fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Merge and transform multiple existing batches into a single new batch with the given modifications.
[**edit_batch**](BatchesApi.md#edit_batch) | **PUT** /batches/{batchId}/quantity-corrections | fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Update the quantity of a batch.
[**get_batch_by_id**](BatchesApi.md#get_batch_by_id) | **GET** /batches/{batchId} | fulfillment:read - Returns a batch.
[**get_batch_mutations_by_sequence_number**](BatchesApi.md#get_batch_mutations_by_sequence_number) | **GET** /batches/mutations/sync/{sequenceNumber} | fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batch mutations starting from a specified sequence number.
[**get_batch_mutations_max_sequence**](BatchesApi.md#get_batch_mutations_max_sequence) | **GET** /batches/mutations/current-max-sequence | fulfillment:read - Returns the maximum sequence number found in batch mutations.
[**get_batches**](BatchesApi.md#get_batches) | **GET** /batches | fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns batches.
[**get_batches_by_sequence_number**](BatchesApi.md#get_batches_by_sequence_number) | **GET** /batches/sync/{sequenceNumber} | fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batches starting from a specified sequence number.
[**get_batches_max_sequence**](BatchesApi.md#get_batches_max_sequence) | **GET** /batches/current-max-sequence | fulfillment:read - Returns the maximum sequence number found in batches.
[**get_tray_labels_as_pdf_by_batch_ids**](BatchesApi.md#get_tray_labels_as_pdf_by_batch_ids) | **GET** /batches/stickers | fulfillment:read - Returns tray stickers as pdf for batches.
[**transform_batch**](BatchesApi.md#transform_batch) | **PUT** /batches/{batchId}/transform | fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Transform a batch into a new batch with the given modifications.

# **add_batch**
> add_batch(body)

fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a batch.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddBatch() # AddBatch | 

try:
    # fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Creates a batch.
    api_instance.add_batch(body)
except ApiException as e:
    print("Exception when calling BatchesApi->add_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddBatch**](AddBatch.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **combine_and_transform_batches**
> combine_and_transform_batches(body)

fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Merge and transform multiple existing batches into a single new batch with the given modifications.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.CombineAndTransformBatchesRequest() # CombineAndTransformBatchesRequest | 

try:
    # fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Merge and transform multiple existing batches into a single new batch with the given modifications.
    api_instance.combine_and_transform_batches(body)
except ApiException as e:
    print("Exception when calling BatchesApi->combine_and_transform_batches: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CombineAndTransformBatchesRequest**](CombineAndTransformBatchesRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_batch**
> edit_batch(body, batch_id)

fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Update the quantity of a batch.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.QuantityCorrection() # QuantityCorrection | 
batch_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Update the quantity of a batch.
    api_instance.edit_batch(body, batch_id)
except ApiException as e:
    print("Exception when calling BatchesApi->edit_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**QuantityCorrection**](QuantityCorrection.md)|  | 
 **batch_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_batch_by_id**
> Batch get_batch_by_id(batch_id)

fulfillment:read - Returns a batch.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
batch_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:read - Returns a batch.
    api_response = api_instance.get_batch_by_id(batch_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batch_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_id** | [**str**](.md)|  | 

### Return type

[**Batch**](Batch.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_batch_mutations_by_sequence_number**
> SyncResultOfBatchMutation get_batch_mutations_by_sequence_number(sequence_number, limit_result=limit_result)

fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batch mutations starting from a specified sequence number.

**Synchronization endpoint** Fetches the succeeding modified records based on `Limit` and the given `SequenceNumber`.  **Note** Your  data is up to date when your given `SequenceNumber` is equal to the received `MaximumSequenceNumber`.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batch mutations starting from a specified sequence number.
    api_response = api_instance.get_batch_mutations_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batch_mutations_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfBatchMutation**](SyncResultOfBatchMutation.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_batch_mutations_max_sequence**
> int get_batch_mutations_max_sequence()

fulfillment:read - Returns the maximum sequence number found in batch mutations.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # fulfillment:read - Returns the maximum sequence number found in batch mutations.
    api_response = api_instance.get_batch_mutations_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batch_mutations_max_sequence: %s\n" % e)
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

# **get_batches**
> list[Batch] get_batches(warehouse_id=warehouse_id, minimum_number_of_pieces=minimum_number_of_pieces, limit_result=limit_result)

fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns batches.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
warehouse_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str |  (optional)
minimum_number_of_pieces = 56 # int |  (optional)
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns batches.
    api_response = api_instance.get_batches(warehouse_id=warehouse_id, minimum_number_of_pieces=minimum_number_of_pieces, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batches: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **warehouse_id** | [**str**](.md)|  | [optional] 
 **minimum_number_of_pieces** | **int**|  | [optional] 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**list[Batch]**](Batch.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_batches_by_sequence_number**
> SyncResultOfBatch get_batches_by_sequence_number(sequence_number, limit_result=limit_result)

fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batches starting from a specified sequence number.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # fulfillment:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 batches starting from a specified sequence number.
    api_response = api_instance.get_batches_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batches_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfBatch**](SyncResultOfBatch.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_batches_max_sequence**
> int get_batches_max_sequence()

fulfillment:read - Returns the maximum sequence number found in batches.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))

try:
    # fulfillment:read - Returns the maximum sequence number found in batches.
    api_response = api_instance.get_batches_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_batches_max_sequence: %s\n" % e)
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

# **get_tray_labels_as_pdf_by_batch_ids**
> str get_tray_labels_as_pdf_by_batch_ids(batch_ids, single_sticker_per_batch=single_sticker_per_batch)

fulfillment:read - Returns tray stickers as pdf for batches.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
batch_ids = 'batch_ids_example' # str | 
single_sticker_per_batch = true # bool |  (optional)

try:
    # fulfillment:read - Returns tray stickers as pdf for batches.
    api_response = api_instance.get_tray_labels_as_pdf_by_batch_ids(batch_ids, single_sticker_per_batch=single_sticker_per_batch)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BatchesApi->get_tray_labels_as_pdf_by_batch_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_ids** | **str**|  | 
 **single_sticker_per_batch** | **bool**|  | [optional] 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transform_batch**
> transform_batch(body, batch_id)

fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Transform a batch into a new batch with the given modifications.

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
api_instance = floriday_supplier_client.BatchesApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.TransformBatchRequest() # TransformBatchRequest | 
batch_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # fulfillment:write - rate limit: 3.4 per second - burst limit: 1000 - Transform a batch into a new batch with the given modifications.
    api_instance.transform_batch(body, batch_id)
except ApiException as e:
    print("Exception when calling BatchesApi->transform_batch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TransformBatchRequest**](TransformBatchRequest.md)|  | 
 **batch_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

