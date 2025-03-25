# FulfillmentOrderCreate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_order_id** | **str** |  | 
**carrier_organization_id** | **str** |  | [optional] 
**logistic_hub** | [**LogisticHub**](LogisticHub.md) |  | [optional] 
**one_label_only** | **bool** | If true, only one logistic label pdf will be provided | 
**load_carriers** | [**list[AddLoadCarrierConfiguration]**](AddLoadCarrierConfiguration.md) |  | 
**delivery_location_gln** | **str** | Optional property to set a different delivery location from the delivery location known in the fulfillment requests. The location must be in the same country as the original delivery location. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

