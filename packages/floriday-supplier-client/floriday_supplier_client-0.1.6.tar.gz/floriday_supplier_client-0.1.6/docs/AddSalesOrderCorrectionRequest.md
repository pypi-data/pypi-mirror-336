# AddSalesOrderCorrectionRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sales_order_correction_request_id** | **str** |  | 
**sales_order_id** | **str** |  | 
**price_per_piece** | [**Price**](Price.md) |  | [optional] 
**package** | [**Package**](Package.md) |  | [optional] 
**number_of_pieces** | **int** |  | [optional] 
**pieces_per_package** | **int** |  | [optional] 
**incoterm** | [**Incoterm**](Incoterm.md) |  | [optional] 
**reason** | **str** |  | [optional] 
**created_by_user** | **str** | Used to associate an existing Floriday account with the created correction request. The user will be shown within the Floriday portal as the created user. | [optional] 
**intended_for_customer_user** | **str** | Used to associate an existing Floriday account with the created correction request. The user will be shown within the Floriday portal as the customer user. | [optional] 
**is_cancel_request** | **bool** |  | 
**created_by_user_name** | **str** | Name of the contact person responsible for the sales order correction request | [optional] 
**stock_application** | [**SalesOrderCorrectionStockApplication**](SalesOrderCorrectionStockApplication.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

