# floriday_supplier_client.OrganizationsApi

All URIs are relative to *https://api.staging.floriday.io/suppliers-api-2024v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization_by_company_gln**](OrganizationsApi.md#get_organization_by_company_gln) | **GET** /organizations | organization:read - Returns an organization by company GLN.
[**get_organization_by_id**](OrganizationsApi.md#get_organization_by_id) | **GET** /organizations/{organizationId} | organization:read - Returns an organization.
[**get_organizations_by_sequence_number**](OrganizationsApi.md#get_organizations_by_sequence_number) | **GET** /organizations/sync/{sequenceNumber} | organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 organizations starting from a specified sequence number.
[**get_organizations_max_sequence**](OrganizationsApi.md#get_organizations_max_sequence) | **GET** /organizations/current-max-sequence | organization:read - Returns the maximum sequence number found in organizations.

# **get_organization_by_company_gln**
> Organization get_organization_by_company_gln(company_gln)

organization:read - Returns an organization by company GLN.

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
api_instance = floriday_supplier_client.OrganizationsApi(floriday_supplier_client.ApiClient(configuration))
company_gln = 'company_gln_example' # str | 

try:
    # organization:read - Returns an organization by company GLN.
    api_response = api_instance.get_organization_by_company_gln(company_gln)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsApi->get_organization_by_company_gln: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **company_gln** | **str**|  | 

### Return type

[**Organization**](Organization.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_by_id**
> Organization get_organization_by_id(organization_id)

organization:read - Returns an organization.

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
api_instance = floriday_supplier_client.OrganizationsApi(floriday_supplier_client.ApiClient(configuration))
organization_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | 

try:
    # organization:read - Returns an organization.
    api_response = api_instance.get_organization_by_id(organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsApi->get_organization_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | [**str**](.md)|  | 

### Return type

[**Organization**](Organization.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organizations_by_sequence_number**
> SyncResultOfOrganization get_organizations_by_sequence_number(sequence_number, limit_result=limit_result)

organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 organizations starting from a specified sequence number.

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
api_instance = floriday_supplier_client.OrganizationsApi(floriday_supplier_client.ApiClient(configuration))
sequence_number = 789 # int | 
limit_result = 1000 # int |  (optional) (default to 1000)

try:
    # organization:read - rate limit: 2.0 per second - burst limit: 200 - Returns a list of max 1000 organizations starting from a specified sequence number.
    api_response = api_instance.get_organizations_by_sequence_number(sequence_number, limit_result=limit_result)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsApi->get_organizations_by_sequence_number: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sequence_number** | **int**|  | 
 **limit_result** | **int**|  | [optional] [default to 1000]

### Return type

[**SyncResultOfOrganization**](SyncResultOfOrganization.md)

### Authorization

[JWT Token](../README.md#JWT Token), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organizations_max_sequence**
> int get_organizations_max_sequence()

organization:read - Returns the maximum sequence number found in organizations.

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
api_instance = floriday_supplier_client.OrganizationsApi(floriday_supplier_client.ApiClient(configuration))

try:
    # organization:read - Returns the maximum sequence number found in organizations.
    api_response = api_instance.get_organizations_max_sequence()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsApi->get_organizations_max_sequence: %s\n" % e)
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

