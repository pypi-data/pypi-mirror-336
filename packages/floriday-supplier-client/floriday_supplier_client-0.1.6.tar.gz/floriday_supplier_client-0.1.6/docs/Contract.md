# Contract

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contract_id** | **str** |  | 
**reference** | **str** | The reference of a contract remains the same between the different versions. | 
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**start_date_time** | **datetime** |  | 
**end_date_time** | **datetime** |  | 
**customer_organization_id** | **str** |  | 
**supplier_organization_id** | **str** |  | 
**sub_supplier_organization_ids** | **list[str]** |  | [optional] 
**contract_period_kind** | [**ContractPeriodKind**](ContractPeriodKind.md) |  | 
**is_initiated_by_supplier** | **bool** |  | 
**allow_trade_item_variants** | **bool** | Allow the use of variants from the chosen trade item when creating a blanket order. | 
**allow_automatic_blanket_order_approval** | **bool** |  | 
**version** | [**ContractVersion**](ContractVersion.md) |  | 
**status** | [**ContractStatus**](ContractStatus.md) |  | 
**delivery** | [**ContractDelivery**](ContractDelivery.md) |  | 
**currency** | [**Currency**](Currency.md) |  | 
**payment_provider** | [**PaymentProvider**](PaymentProvider.md) |  | 
**creation_date_time** | **datetime** |  | 
**last_modified_date_time** | **datetime** |  | 
**contract_lines** | [**list[ContractLine]**](ContractLine.md) |  | 
**attachment_details** | [**list[AttachmentDetail]**](AttachmentDetail.md) |  | [optional] 
**sequence_number** | **int** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

