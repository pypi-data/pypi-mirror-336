# LoadCarrierConfigurationInbound

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**load_carrier_items** | [**list[LoadCarrierItemInbound]**](LoadCarrierItemInbound.md) |  | 
**load_carrier_type** | [**LoadCarrierType**](LoadCarrierType.md) |  | 
**number_of_additional_layers** | **int** |  | 
**document_reference** | **str** |  | [optional] 
**delivery_note_codes** | **list[str]** |  | 
**sort_index** | **int** | Used to determine the position of the load carrier within the shipment. Duplicate numbers will yield indeterministic sequencing. | 
**load_carrier_reference** | **str** | When present, uniquely references a load carrier within a collection of load carrier configurations; Appears on a PAB. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

