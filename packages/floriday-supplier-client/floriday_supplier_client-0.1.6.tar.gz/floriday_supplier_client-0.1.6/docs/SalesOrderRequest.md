# SalesOrderRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sales_order_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**supply_line_id** | **str** |  | 
**number_of_pieces** | **int** |  | 
**price_per_piece** | [**AddPrice**](AddPrice.md) |  | 
**customer_order_id** | **str** |  | [optional] 
**created_by_user** | **str** | Used to associate an existing Floriday account with the created sales order. The user will be shown within the Floriday portal as the created user. | [optional] 
**packing_configuration** | [**SalesOrderPackingConfigurationCreate**](SalesOrderPackingConfigurationCreate.md) |  | 
**order_date_time** | **datetime** |  | 
**delivery** | [**AddSalesOrderDelivery**](AddSalesOrderDelivery.md) |  | 
**additional_services** | [**list[OrderAdditionalService]**](OrderAdditionalService.md) |  | [optional] 
**send_ekt** | **bool** |  | [optional] 
**payment_provider** | [**PaymentProviderCreate**](PaymentProviderCreate.md) |  | 
**delivery_remarks** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

