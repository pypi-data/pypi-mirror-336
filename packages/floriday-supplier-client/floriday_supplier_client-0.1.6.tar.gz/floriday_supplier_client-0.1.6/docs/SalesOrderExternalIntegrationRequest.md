# SalesOrderExternalIntegrationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sales_order_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**trade_item_id** | **str** |  | 
**despatch_warehouse_id** | **str** |  | 
**number_of_pieces** | **int** |  | 
**price_per_piece** | [**AddPrice**](AddPrice.md) |  | 
**customer_order_id** | **str** |  | [optional] 
**created_by_user** | **str** | Used to associate an existing Floriday account with the created sales order. The user will be shown within the Floriday portal as the created user. | [optional] 
**packing_configuration** | [**SalesOrderPackingConfigurationCreate**](SalesOrderPackingConfigurationCreate.md) |  | 
**delivery** | [**AddSalesOrderDelivery**](AddSalesOrderDelivery.md) |  | 
**additional_services** | [**list[OrderAdditionalService]**](OrderAdditionalService.md) |  | [optional] 
**send_ekt** | **bool** |  | [optional] 
**payment_provider** | [**PaymentProviderCreate**](PaymentProviderCreate.md) |  | 
**delivery_remarks** | **str** |  | [optional] 
**included_services** | [**list[CommercialService]**](CommercialService.md) | Does not support the commercial service type &#x27;DELIVERY&#x27; | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

