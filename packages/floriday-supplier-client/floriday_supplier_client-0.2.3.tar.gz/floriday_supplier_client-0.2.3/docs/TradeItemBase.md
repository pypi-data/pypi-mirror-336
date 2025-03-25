# TradeItemBase

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_item_id** | **str** |  | 
**supplier_article_code** | **str** | Supplier article code cannot contain leading, trailing or duplicate whitespaces. | 
**article_gtin** | **str** |  | [optional] 
**vbn_product_code** | **int** |  | 
**trade_item_name** | **AllOfTradeItemBaseTradeItemName** | Trade item name cannot contain leading, trailing or duplicate whitespaces. | 
**characteristics** | [**list[Characteristic]**](Characteristic.md) |  | 
**customer_organization_ids** | **list[str]** |  | [optional] 
**seasonal_periods** | [**list[SeasonalPeriod]**](SeasonalPeriod.md) |  | [optional] 
**photos** | [**list[Photo]**](Photo.md) |  | 
**packing_configurations** | [**list[PackingConfiguration]**](PackingConfiguration.md) |  | 
**botanical_names** | **list[str]** |  | [optional] 
**country_of_origin_iso_codes** | **list[str]** |  | [optional] 
**is_hidden_in_catalog** | **bool** |  | 
**trade_item_components** | [**list[TradeItemComponent]**](TradeItemComponent.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

