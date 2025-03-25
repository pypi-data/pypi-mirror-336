# SupplyRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_request_id** | **str** |  | 
**customer_organization_id** | **str** |  | 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**quantity_description** | **str** |  | [optional] 
**sales_channel** | **str** |  | 
**order_period** | [**TradePeriod**](TradePeriod.md) |  | 
**delivery_period** | [**TradePeriod**](TradePeriod.md) |  | 
**agreement_reference** | [**AgreementReference**](AgreementReference.md) |  | [optional] 
**expires_at_date_time** | **datetime** |  | 
**creation_date_time** | **datetime** |  | 
**last_modified_date_time** | **datetime** |  | 
**is_deleted** | **bool** |  | 
**sequence_number** | **int** |  | 
**commercial_services** | [**list[CommercialService]**](CommercialService.md) |  | 
**supply_request_lines** | [**list[SupplyRequestLine]**](SupplyRequestLine.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

