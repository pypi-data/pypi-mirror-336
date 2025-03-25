# SalesOrderVersion

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sales_order_id** | **str** |  | 
**sales_channel_order_id** | **str** |  | [optional] 
**customer_order_id** | **str** |  | [optional] 
**supplier_organization_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**supply_line_id** | **str** |  | [optional] 
**trade_item_id** | **str** |  | 
**sales_channel** | [**SalesChannel**](SalesChannel.md) |  | 
**number_of_pieces** | **int** |  | 
**trade_instrument** | [**TradeInstrument**](TradeInstrument.md) |  | 
**packing_configuration** | [**SalesOrderPackingConfiguration**](SalesOrderPackingConfiguration.md) |  | 
**order_date_time** | **datetime** |  | 
**price_per_piece** | [**Price**](Price.md) |  | 
**delivery** | [**SalesOrderDelivery**](SalesOrderDelivery.md) |  | 
**additional_services** | [**list[OrderedAdditionalService]**](OrderedAdditionalService.md) |  | [optional] 
**cancellation_deadline** | **datetime** |  | [optional] 
**status** | [**SalesOrderStatus**](SalesOrderStatus.md) |  | [optional] 
**credit_claim_status** | [**CreditClaimStatus**](CreditClaimStatus.md) |  | [optional] 
**credit_claim_expiration_date_time** | **datetime** |  | [optional] 
**sequence_number** | **int** |  | 
**trade_item_version** | **int** |  | [optional] 
**version** | **int** |  | [optional] 
**contract_id** | **str** |  | [optional] 
**blanket_order_line_id** | **str** |  | [optional] 
**calculated_fields** | [**SalesOrderCalculatedFields**](SalesOrderCalculatedFields.md) |  | [optional] 
**payment_provider** | [**PaymentProvider**](PaymentProvider.md) |  | [optional] 
**delivery_remarks** | **str** |  | [optional] 
**delivery_price_per_piece** | [**Price**](Price.md) |  | [optional] 
**despatch_warehouse_id** | **str** |  | [optional] 
**creation_date_time** | **datetime** |  | [optional] 
**last_modified_date_time** | **datetime** |  | [optional] 
**created_by_supplier** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

