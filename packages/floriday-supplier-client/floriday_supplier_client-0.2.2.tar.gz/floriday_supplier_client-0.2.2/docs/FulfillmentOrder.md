# FulfillmentOrder

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_order_id** | **str** |  | 
**latest_delivery_date_time** | **datetime** |  | 
**despatch_warehouse_id** | **str** |  | 
**fulfilling_organization_id** | **str** |  | 
**supplier_organization_id** | **str** |  | 
**carrier_organization_id** | **str** |  | [optional] 
**destination** | [**Destination**](Destination.md) |  | 
**logistic_hub** | [**LogisticHub**](LogisticHub.md) |  | [optional] 
**load_carriers** | [**list[LoadCarrierConfiguration]**](LoadCarrierConfiguration.md) |  | 
**delivery_note_codes** | **list[str]** |  | 
**type** | [**FulfillmentType**](FulfillmentType.md) |  | 
**one_label_only** | **bool** |  | 
**status** | [**FulfillmentStatus**](FulfillmentStatus.md) |  | 
**submission_error** | **str** |  | [optional] 
**sequence_number** | **int** |  | 
**creation_date_time** | **datetime** |  | 
**last_modified_date_time** | **datetime** |  | 
**fulfillment_order_corrections** | [**list[FulfillmentOrderCorrection]**](FulfillmentOrderCorrection.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

