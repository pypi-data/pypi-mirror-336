# EditContract

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**start_date_time** | **datetime** |  | 
**end_date_time** | **datetime** |  | 
**sub_supplier_organization_ids** | **list[str]** |  | [optional] 
**allow_trade_item_variants** | **bool** | Allow the use of variants from the chosen trade item when creating a blanket order. | 
**allow_automatic_blanket_order_approval** | **bool** |  | 
**delivery** | [**EditContractDelivery**](EditContractDelivery.md) |  | 
**currency** | [**Currency**](Currency.md) |  | 
**payment_provider** | [**PaymentProvider**](PaymentProvider.md) |  | 
**contract_lines** | [**list[EditContractLine]**](EditContractLine.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

