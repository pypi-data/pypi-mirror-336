# DeliveryOrderAuction

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auction_date** | **date** |  | 
**auction_group_code** | **int** |  | 
**batch_fulfillment_requests** | [**list[FulfillmentRequestCreateAuction]**](FulfillmentRequestCreateAuction.md) | AddClockDeliveryOrder only supports batch or trade item fulfillment requests, not a combination. | [optional] 
**trade_item_fulfillment_requests** | [**list[FulfillmentRequestCreateAuctionTradeItem]**](FulfillmentRequestCreateAuctionTradeItem.md) | AddClockDeliveryOrder only supports batch or trade item fulfillment requests, not a combination. | [optional] 
**delivery_date_time** | **datetime** |  | 
**destination_warehouse_id** | **str** |  | 
**despatch_warehouse_id** | **str** |  | 
**carrier_organization_id** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

