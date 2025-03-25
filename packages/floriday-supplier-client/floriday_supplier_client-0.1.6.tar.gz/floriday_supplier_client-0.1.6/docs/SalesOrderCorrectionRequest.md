# SalesOrderCorrectionRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sales_order_correction_request_id** | **str** |  | 
**sales_order_id** | **str** |  | 
**status** | [**CorrectionRequestStatus**](CorrectionRequestStatus.md) |  | 
**is_sales_order_created_by_supplier** | **bool** |  | 
**initiated_by** | [**OrganizationType**](OrganizationType.md) |  | 
**expires_at_date_time** | **datetime** |  | 
**creation_date_time** | **datetime** |  | 
**last_modified_date_time** | **datetime** |  | 
**sequence_number** | **int** |  | 
**customer_organization_id** | **str** |  | 
**price_per_piece** | [**Price**](Price.md) |  | [optional] 
**package** | [**Package**](Package.md) |  | [optional] 
**number_of_pieces** | **int** |  | [optional] 
**pieces_per_package** | **int** |  | [optional] 
**incoterm** | [**Incoterm**](Incoterm.md) |  | [optional] 
**reason** | **str** |  | [optional] 
**is_cancel_request** | **bool** |  | 
**sales_order_version_after_correction** | **int** |  | [optional] 
**created_by_user_name** | **str** | Name of the contact person responsible for the sales order correction request | [optional] 
**stock_application** | [**SalesOrderCorrectionStockApplication**](SalesOrderCorrectionStockApplication.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

