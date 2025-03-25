# OrderRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_request_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**supply_line_id** | **str** |  | [optional] 
**trade_item_id** | **str** |  | 
**number_of_pieces** | **int** |  | 
**price_per_piece** | [**Price**](Price.md) |  | 
**packing_configuration** | [**PackingConfigurationBase**](PackingConfigurationBase.md) |  | 
**delivery** | [**OrderRequestDelivery**](OrderRequestDelivery.md) |  | 
**delivery_remarks** | **str** |  | [optional] 
**reference** | **str** |  | [optional] 
**additional_service_ids** | **list[str]** |  | 
**added** | **datetime** |  | 
**status** | [**OrderRequestStatus**](OrderRequestStatus.md) |  | 
**declined_reason** | **str** |  | [optional] 
**payment_provider** | [**PaymentProvider**](PaymentProvider.md) |  | [optional] 
**sequence_number** | **int** |  | 
**is_deleted** | **bool** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

