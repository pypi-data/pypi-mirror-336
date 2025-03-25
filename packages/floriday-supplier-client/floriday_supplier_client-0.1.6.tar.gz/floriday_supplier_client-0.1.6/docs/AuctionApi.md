# floriday_supplier_client.AuctionApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_clock_presales_supply_line**](AuctionApi.md#add_clock_presales_supply_line) | **POST** /clock-presales-supply-lines | supply:write - Creates a new clock presales supply line.
[**add_clock_sales_from_nursery_supply_line**](AuctionApi.md#add_clock_sales_from_nursery_supply_line) | **POST** /clock-sales-from-nursery/supply-lines | supply:write - Creates a new clock sales from nursery supply line.
[**delete_clock_sales_from_nursery_supply_line**](AuctionApi.md#delete_clock_sales_from_nursery_supply_line) | **DELETE** /clock-sales-from-nursery/supply-lines/{clockSalesFromNurserySupplyLineId} | supply:write - Deletes a clock sales from nursery supply line.
[**edit_clock_presales_supply_line**](AuctionApi.md#edit_clock_presales_supply_line) | **PUT** /clock-presales-supply-lines/{clockPresalesSupplyLineId} | sales-order:write - Updates a clock presales supply line.
[**get_clock_presales_supply_line_by_id**](AuctionApi.md#get_clock_presales_supply_line_by_id) | **GET** /clock-presales-supply-lines/{clockPresalesSupplyLineId} | supply:read - Returns a clock presales supply line.
[**get_clock_presales_supply_lines_by_sequence_number**](AuctionApi.md#get_clock_presales_supply_lines_by_sequence_number) | **GET** /clock-presales-supply-lines/sync/{sequenceNumber} | supply:read - Returns a list of max 1000 clock presales supply lines starting from a specified sequence number.
[**get_clock_presales_supply_lines_max_sequence**](AuctionApi.md#get_clock_presales_supply_lines_max_sequence) | **GET** /clock-presales-supply-lines/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock presales supply lines.
[**get_clock_supply_line_by_id**](AuctionApi.md#get_clock_supply_line_by_id) | **GET** /clock-supply-lines/{supplyLineId} | supply:read - Returns a clock supply line.
[**get_clock_supply_lines_by_sequence_number**](AuctionApi.md#get_clock_supply_lines_by_sequence_number) | **GET** /clock-supply-lines/sync/{sequenceNumber} | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 clock supply lines starting from a specified sequence number.
[**get_clock_supply_lines_max_sequence**](AuctionApi.md#get_clock_supply_lines_max_sequence) | **GET** /clock-supply-lines/current-max-sequence | supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock supply lines.

# **add_clock_presales_supply_line**
> add_clock_presales_supply_line(body)

supply:write - Creates a new clock presales supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddClockPresalesSupplyLine() # AddClockPresalesSupplyLine | 

try:
    # supply:write - Creates a new clock presales supply line.
    api_instance.add_clock_presales_supply_line(body)
except ApiException as e:
    print("Exception when calling AuctionApi->add_clock_presales_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddClockPresalesSupplyLine**](AddClockPresalesSupplyLine.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_clock_sales_from_nursery_supply_line**
> add_clock_sales_from_nursery_supply_line(body)

supply:write - Creates a new clock sales from nursery supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddClockSalesFromNurserySupplyLine() # AddClockSalesFromNurserySupplyLine | 

try:
    # supply:write - Creates a new clock sales from nursery supply line.
    api_instance.add_clock_sales_from_nursery_supply_line(body)
except ApiException as e:
    print("Exception when calling AuctionApi->add_clock_sales_from_nursery_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddClockSalesFromNurserySupplyLine**](AddClockSalesFromNurserySupplyLine.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_clock_sales_from_nursery_supply_line**
> delete_clock_sales_from_nursery_supply_line(clock_sales_from_nursery_supply_line_id)

supply:write - Deletes a clock sales from nursery supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
clock_sales_from_nursery_supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:write - Deletes a clock sales from nursery supply line.
    api_instance.delete_clock_sales_from_nursery_supply_line(clock_sales_from_nursery_supply_line_id)
except ApiException as e:
    print("Exception when calling AuctionApi->delete_clock_sales_from_nursery_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **clock_sales_from_nursery_supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_clock_presales_supply_line**
> edit_clock_presales_supply_line(body, clock_presales_supply_line_id)

sales-order:write - Updates a clock presales supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditClockPresalesSupplyLine() # EditClockPresalesSupplyLine | 
clock_presales_supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # sales-order:write - Updates a clock presales supply line.
    api_instance.edit_clock_presales_supply_line(body, clock_presales_supply_line_id)
except ApiException as e:
    print("Exception when calling AuctionApi->edit_clock_presales_supply_line: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditClockPresalesSupplyLine**](EditClockPresalesSupplyLine.md)|  | 
 **clock_presales_supply_line_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_clock_presales_supply_line_by_id**
> ClockPresalesSupplyLine get_clock_presales_supply_line_by_id(clock_presales_supply_line_id)

supply:read - Returns a clock presales supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
clock_presales_supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a clock presales supply line.
    api_response = api_instance.get_clock_presales_supply_line_by_id(clock_presales_supply_line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_presales_supply_line_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **clock_presales_supply_line_id** | [**str**](.md)|  | 

### Return type

[**ClockPresalesSupplyLine**](ClockPresalesSupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_clock_presales_supply_lines_by_sequence_number**
> SyncResultOfClockPresalesSupplyLine get_clock_presales_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)

supply:read - Returns a list of max 1000 clock presales supply lines starting from a specified sequence number.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - Returns a list of max 1000 clock presales supply lines starting from a specified sequence number.
    api_response = api_instance.get_clock_presales_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_presales_supply_lines_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfClockPresalesSupplyLine**](SyncResultOfClockPresalesSupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_clock_presales_supply_lines_max_sequence**
> int get_clock_presales_supply_lines_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock presales supply lines.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock presales supply lines.
    api_response = api_instance.get_clock_presales_supply_lines_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_presales_supply_lines_max_sequence: %s\n" % e)
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

# **get_clock_supply_line_by_id**
> ClockSupplyLine get_clock_supply_line_by_id(supply_line_id)

supply:read - Returns a clock supply line.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
supply_line_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # supply:read - Returns a clock supply line.
    api_response = api_instance.get_clock_supply_line_by_id(supply_line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_supply_line_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_line_id** | [**str**](.md)|  | 

### Return type

[**ClockSupplyLine**](ClockSupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_clock_supply_lines_by_sequence_number**
> SyncResultOfClockSupplyLine get_clock_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 clock supply lines starting from a specified sequence number.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 1000 clock supply lines starting from a specified sequence number.
    api_response = api_instance.get_clock_supply_lines_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_supply_lines_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfClockSupplyLine**](SyncResultOfClockSupplyLine.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_clock_supply_lines_max_sequence**
> int get_clock_supply_lines_max_sequence()

supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock supply lines.

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
api_instance = floriday_supplier_client.AuctionApi(floriday_supplier_client.ApiClient(configuration))

try:
    # supply:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in clock supply lines.
    api_response = api_instance.get_clock_supply_lines_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuctionApi->get_clock_supply_lines_max_sequence: %s\n" % e)
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

