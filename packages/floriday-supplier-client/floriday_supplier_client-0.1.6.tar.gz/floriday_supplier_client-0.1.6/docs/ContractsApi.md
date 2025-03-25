# floriday_supplier_client.ContractsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_contract**](ContractsApi.md#add_contract) | **POST** /contracts | contract:write - Creates a draft contract
[**add_new_contract_version**](ContractsApi.md#add_new_contract_version) | **POST** /contracts/reference/{contractReference} | contract:write - Creates a new version for an existing contract
[**approve_contract**](ContractsApi.md#approve_contract) | **PATCH** /contracts/{contractId}/approve | contract:write - Sets the state of the contract to &#x27;APPROVED&#x27; if already finalized by the customer.
[**approve_contract_by_reference**](ContractsApi.md#approve_contract_by_reference) | **PATCH** /contracts/reference/{contractReference}/approve-contract | contract:write - Sets the state of the contract to &#x27;APPROVED&#x27; if already finalized by the customer.
[**approve_delete_contract**](ContractsApi.md#approve_delete_contract) | **DELETE** /contracts/reference/{contractReference}/approve | contract:write - Approves contract delete request created by customer
[**decline_contract**](ContractsApi.md#decline_contract) | **PATCH** /contracts/{contractId}/decline | contract:write - Sets the state of the contract to &#x27;DECLINED&#x27; if already finalized by the customer.
[**decline_contract2**](ContractsApi.md#decline_contract2) | **PATCH** /contracts/reference/{contractReference}/decline-contract | contract:write - Sets the state of the contract to &#x27;DECLINED&#x27; if already finalized by the customer.
[**decline_delete_contract**](ContractsApi.md#decline_delete_contract) | **DELETE** /contracts/reference/{contractReference}/decline-delete | contract:write - Declines contract delete request created by customer
[**edit_contract**](ContractsApi.md#edit_contract) | **PUT** /contracts/{contractId} | contract:write - Updates a draft contract
[**edit_contract_by_reference**](ContractsApi.md#edit_contract_by_reference) | **PUT** /contracts/reference/{contractReference} | contract:write - Updates a draft contract
[**finalize_contract**](ContractsApi.md#finalize_contract) | **PATCH** /contracts/{contractId}/finalize | contract:write - Sets the contract status to &#x27;FINALIZED&#x27; and offers the contract to the customer for approval.
[**finalize_contract_by_reference**](ContractsApi.md#finalize_contract_by_reference) | **PATCH** /contracts/reference/{contractReference}/finalize-contract | contract:write - Sets the contract status to &#x27;FINALIZED&#x27; and offers the contract to the customer for approval.
[**get_contract_attachment_by_id**](ContractsApi.md#get_contract_attachment_by_id) | **GET** /contracts/attachments/{attachmentId} | contract:read - Returns a contract attachment.
[**get_contract_by_id**](ContractsApi.md#get_contract_by_id) | **GET** /contracts/{contractId} | contract:read - Returns a contract.
[**get_contracts_by_sequence_number**](ContractsApi.md#get_contracts_by_sequence_number) | **GET** /contracts/sync/{sequenceNumber} | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 contracts starting from a specified sequence number.
[**get_contracts_max_sequence**](ContractsApi.md#get_contracts_max_sequence) | **GET** /contracts/current-max-sequence | contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contracts.
[**request_delete_contract**](ContractsApi.md#request_delete_contract) | **DELETE** /contracts/reference/{contractReference}/request | contract:write - Deletes contract if contract is not yet approved. Requests delete by customer if already approved

# **add_contract**
> add_contract(body)

contract:write - Creates a draft contract

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddContract() # AddContract | 

try:
    # contract:write - Creates a draft contract
    api_instance.add_contract(body)
except ApiException as e:
    print("Exception when calling ContractsApi->add_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddContract**](AddContract.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_new_contract_version**
> add_new_contract_version(body, contract_reference)

contract:write - Creates a new version for an existing contract

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.AddContractVersion() # AddContractVersion | 
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Creates a new version for an existing contract
    api_instance.add_new_contract_version(body, contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->add_new_contract_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddContractVersion**](AddContractVersion.md)|  | 
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **approve_contract**
> approve_contract(contract_id)

contract:write - Sets the state of the contract to 'APPROVED' if already finalized by the customer.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Sets the state of the contract to 'APPROVED' if already finalized by the customer.
    api_instance.approve_contract(contract_id)
except ApiException as e:
    print("Exception when calling ContractsApi->approve_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **approve_contract_by_reference**
> approve_contract_by_reference(contract_reference)

contract:write - Sets the state of the contract to 'APPROVED' if already finalized by the customer.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Sets the state of the contract to 'APPROVED' if already finalized by the customer.
    api_instance.approve_contract_by_reference(contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->approve_contract_by_reference: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **approve_delete_contract**
> approve_delete_contract(contract_reference)

contract:write - Approves contract delete request created by customer

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Approves contract delete request created by customer
    api_instance.approve_delete_contract(contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->approve_delete_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **decline_contract**
> decline_contract(body, contract_id)

contract:write - Sets the state of the contract to 'DECLINED' if already finalized by the customer.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.DeclineContract() # DeclineContract | 
contract_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Sets the state of the contract to 'DECLINED' if already finalized by the customer.
    api_instance.decline_contract(body, contract_id)
except ApiException as e:
    print("Exception when calling ContractsApi->decline_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeclineContract**](DeclineContract.md)|  | 
 **contract_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **decline_contract2**
> decline_contract2(body, contract_reference)

contract:write - Sets the state of the contract to 'DECLINED' if already finalized by the customer.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.DeclineContract() # DeclineContract | 
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Sets the state of the contract to 'DECLINED' if already finalized by the customer.
    api_instance.decline_contract2(body, contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->decline_contract2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeclineContract**](DeclineContract.md)|  | 
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **decline_delete_contract**
> decline_delete_contract(contract_reference)

contract:write - Declines contract delete request created by customer

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Declines contract delete request created by customer
    api_instance.decline_delete_contract(contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->decline_delete_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_contract**
> edit_contract(body, contract_id)

contract:write - Updates a draft contract

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditContract() # EditContract | 
contract_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Updates a draft contract
    api_instance.edit_contract(body, contract_id)
except ApiException as e:
    print("Exception when calling ContractsApi->edit_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditContract**](EditContract.md)|  | 
 **contract_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_contract_by_reference**
> edit_contract_by_reference(body, contract_reference)

contract:write - Updates a draft contract

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
body = floriday_supplier_client.EditContract() # EditContract | 
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Updates a draft contract
    api_instance.edit_contract_by_reference(body, contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->edit_contract_by_reference: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EditContract**](EditContract.md)|  | 
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json-patch+json, application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finalize_contract**
> finalize_contract(contract_id)

contract:write - Sets the contract status to 'FINALIZED' and offers the contract to the customer for approval.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:write - Sets the contract status to 'FINALIZED' and offers the contract to the customer for approval.
    api_instance.finalize_contract(contract_id)
except ApiException as e:
    print("Exception when calling ContractsApi->finalize_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | [**str**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finalize_contract_by_reference**
> finalize_contract_by_reference(contract_reference)

contract:write - Sets the contract status to 'FINALIZED' and offers the contract to the customer for approval.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Sets the contract status to 'FINALIZED' and offers the contract to the customer for approval.
    api_instance.finalize_contract_by_reference(contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->finalize_contract_by_reference: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract_attachment_by_id**
> str get_contract_attachment_by_id(attachment_id)

contract:read - Returns a contract attachment.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
attachment_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:read - Returns a contract attachment.
    api_response = api_instance.get_contract_attachment_by_id(attachment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractsApi->get_contract_attachment_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **attachment_id** | [**str**](.md)|  | 

### Return type

**str**

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract_by_id**
> Contract get_contract_by_id(contract_id)

contract:read - Returns a contract.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # contract:read - Returns a contract.
    api_response = api_instance.get_contract_by_id(contract_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractsApi->get_contract_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | [**str**](.md)|  | 

### Return type

[**Contract**](Contract.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contracts_by_sequence_number**
> SyncResultOfContract get_contracts_by_sequence_number(sequence_number, limit_result=limit_result)

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 contracts starting from a specified sequence number.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 100 # int |  (optional) (default to 100)

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns a list of max 100 contracts starting from a specified sequence number.
    api_response = api_instance.get_contracts_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractsApi->get_contracts_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 100]

### Return type

[**SyncResultOfContract**](SyncResultOfContract.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contracts_max_sequence**
> int get_contracts_max_sequence()

contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contracts.

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # contract:read - rate limit: 3.4 per second - burst limit: 1000 - Returns the maximum sequence number found in contracts.
    api_response = api_instance.get_contracts_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContractsApi->get_contracts_max_sequence: %s\n" % e)
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

# **request_delete_contract**
> request_delete_contract(contract_reference)

contract:write - Deletes contract if contract is not yet approved. Requests delete by customer if already approved

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
api_instance = floriday_supplier_client.ContractsApi(floriday_supplier_client.ApiClient(configuration))
contract_reference = 'contract_reference_example' # str | 

try:
    # contract:write - Deletes contract if contract is not yet approved. Requests delete by customer if already approved
    api_instance.request_delete_contract(contract_reference)
except ApiException as e:
    print("Exception when calling ContractsApi->request_delete_contract: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_reference** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

