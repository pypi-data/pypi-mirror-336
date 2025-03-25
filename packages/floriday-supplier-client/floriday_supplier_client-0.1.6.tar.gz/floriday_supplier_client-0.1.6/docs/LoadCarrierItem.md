# LoadCarrierItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_request_id** | **str** |  | 
**sales_order_id** | **str** |  | [optional] 
**number_of_packages** | **int** |  | 
**service_code** | **int** |  | [optional] 
**packing_agent_organization_id** | **str** |  | [optional] 
**batch_id** | **str** |  | 
**trade_item_id** | **str** |  | 
**batch_reference** | **str** |  | [optional] 
**delivery_note_code** | **str** |  | [optional] 
**delivery_note_letter** | **str** |  | [optional] 
**commercial_invoice_reference** | **str** |  | [optional] 
**sort_index** | **int** | The index related to the item&#x27;s position on the loadcarrier | [optional] 
**delivery_remarks** | **str** | The delivery remarks will be printed on the connect EAB document. A &#x60;NULL&#x60; value indicates the use of the default delivery remarks found in the FulfillmentRequest or will ignore the value in an update. | [optional] 
**status_of_received_item** | [**ReceivedLoadCarrierConfigurationItemStatus**](ReceivedLoadCarrierConfigurationItemStatus.md) |  | [optional] 
**status_of_received_item_reason** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

