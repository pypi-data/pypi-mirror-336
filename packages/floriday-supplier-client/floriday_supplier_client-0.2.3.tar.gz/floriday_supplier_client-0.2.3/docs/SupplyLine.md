# SupplyLine

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_line_id** | **str** |  | 
**status** | [**SupplyStatus**](SupplyStatus.md) |  | 
**trade_item_id** | **str** |  | 
**batch_id** | **str** |  | [optional] 
**price_per_piece** | [**Price**](Price.md) |  | 
**price_per_piece_last_modified** | **datetime** | This field is set when the price has been changed by the supplier. Catalog prices in a closed week can only be changed once per 24 hours. | [optional] 
**volume_prices** | [**list[VolumePrice]**](VolumePrice.md) |  | 
**number_of_pieces** | **int** |  | 
**packing_configurations** | [**list[SupplyLinePackingConfiguration]**](SupplyLinePackingConfiguration.md) |  | [optional] 
**order_period** | [**TradePeriod**](TradePeriod.md) |  | 
**delivery_period** | [**TradePeriod**](TradePeriod.md) |  | [optional] 
**included_services** | [**list[CommercialService]**](CommercialService.md) |  | [optional] 
**allowed_customer_organization_ids** | **list[str]** |  | [optional] 
**sequence_number** | **int** |  | 
**supply_type** | [**SupplyType**](SupplyType.md) |  | [optional] 
**agreement_reference** | [**AgreementReference**](AgreementReference.md) |  | [optional] 
**sales_unit** | [**SalesUnit**](SalesUnit.md) |  | [optional] 
**is_promo** | **bool** |  | [optional] 
**is_deleted** | **bool** |  | [optional] 
**price_group_name** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

