# SupplyLineCreate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_line_id** | **str** |  | 
**batch_id** | **str** |  | 
**trade_item_id** | **str** |  | [optional] 
**price_per_piece** | [**Price**](Price.md) |  | 
**order_period** | [**TradePeriod**](TradePeriod.md) |  | 
**delivery_period** | [**TradePeriod**](TradePeriod.md) |  | 
**included_services** | [**list[CommercialService]**](CommercialService.md) |  | 
**allowed_customer_organization_ids** | **list[str]** |  | [optional] 
**packing_configurations** | [**list[SupplyLinePackingConfigurationCreate]**](SupplyLinePackingConfigurationCreate.md) |  | 
**agreement_reference** | [**AgreementReference**](AgreementReference.md) |  | [optional] 
**assigned_number_of_pieces** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

