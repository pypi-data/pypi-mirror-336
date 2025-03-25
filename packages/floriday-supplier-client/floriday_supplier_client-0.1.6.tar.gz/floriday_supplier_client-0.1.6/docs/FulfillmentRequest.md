# FulfillmentRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_request_id** | **str** |  | 
**batch_id** | **str** |  | 
**number_of_packages** | **int** |  | 
**initial_number_of_packages** | **int** |  | 
**sales_order_id** | **str** |  | [optional] 
**clock_pre_sales_price** | **float** |  | [optional] 
**clock_minimum_price** | **float** |  | [optional] 
**additional_service_ids** | **list[str]** |  | [optional] 
**package** | [**Package**](Package.md) |  | [optional] 
**pieces_per_package** | **int** |  | [optional] 
**load_carrier** | [**LoadCarrierType**](LoadCarrierType.md) |  | [optional] 
**service_code** | **int** |  | [optional] 
**packing_agent_organization_id** | **str** |  | [optional] 
**next_leg_identifier** | **str** |  | [optional] 
**delivery_remarks** | **str** |  | [optional] 
**number_of_pieces_picked** | **int** |  | 
**fulfillment_order_claims** | [**list[FulfillmentOrderClaim]**](FulfillmentOrderClaim.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

