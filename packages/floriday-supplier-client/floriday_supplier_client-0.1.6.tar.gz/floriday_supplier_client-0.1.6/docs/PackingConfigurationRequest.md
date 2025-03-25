# PackingConfigurationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packing_configuration_request_id** | **str** |  | 
**supplier_organization_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**trade_item_id** | **str** |  | 
**status** | [**RequestStatus**](RequestStatus.md) |  | 
**sequence_number** | **int** |  | 
**remark** | **str** |  | [optional] 
**expires_at_date_time** | **datetime** |  | 
**creation_date_time** | **datetime** |  | 
**last_modified_date_time** | **datetime** |  | 
**pieces_per_package** | **int** |  | 
**package** | [**Package**](Package.md) |  | 
**packages_per_layer** | **int** |  | 
**layers_per_load_carrier** | **int** |  | 
**load_carrier** | [**SupplyLoadCarrierType**](SupplyLoadCarrierType.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

