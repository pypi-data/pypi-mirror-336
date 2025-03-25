# CustomerTradeSettings

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_organization_id** | **str** |  | 
**accepts_direct_orders** | **AllOfCustomerTradeSettingsAcceptsDirectOrders** | As a customer, you set whether suppliers are allowed to create orders manually. | 
**automatically_accepts_correction_requests_on_direct_orders** | **AllOfCustomerTradeSettingsAutomaticallyAcceptsCorrectionRequestsOnDirectOrders** | With this you set that corrections requested by suppliers on orders that the supplier has created are automatically accepted. | 
**automatically_accepts_correction_requests_on_supply_orders** | **AllOfCustomerTradeSettingsAutomaticallyAcceptsCorrectionRequestsOnSupplyOrders** | With this you set that corrections requested by suppliers on orders placed by you as a customer are automatically accepted. | 
**allow_suppliers_to_manage_selected_trade_item_assortment** | **AllOfCustomerTradeSettingsAllowSuppliersToManageSelectedTradeItemAssortment** | Determine whether suppliers may add trade items to my selected assortment. | 
**accepts_supply_of_type_purchase_tip** | **AllOfCustomerTradeSettingsAcceptsSupplyOfTypePurchaseTip** | Organization works with purchase tips. | 
**uses_contracts** | **AllOfCustomerTradeSettingsUsesContracts** | Organization works with contracts. | 
**accepts_transport_cost** | **AllOfCustomerTradeSettingsAcceptsTransportCost** | Organization works with transport costs. Please note: when deactivating this setting, orders can only be placed on supply where transport costs are included in the price. | 
**sequence_number** | **int** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

