# AdditionalService

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_service_id** | **str** |  | 
**commercial_service_type** | [**CommercialServiceType**](CommercialServiceType.md) |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**warehouse_ids** | **list[str]** |  | 
**price** | **AllOfAdditionalServicePrice** | The extra costs that will be billed when choosing this additional service | 
**unit** | [**AdditionalServiceUnit**](AdditionalServiceUnit.md) |  | 
**customer_organization_ids** | **list[str]** |  | [optional] 
**is_customer_specific** | **bool** | The additional service is customer-specific for one or more customers. | 
**sticker_information** | **AllOfAdditionalServiceStickerInformation** | Optional information related to stickers. | [optional] 
**is_available** | **bool** | Indicates if the additional service is currently available for use | 
**is_deleted** | **bool** |  | 
**sequence_number** | **int** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

