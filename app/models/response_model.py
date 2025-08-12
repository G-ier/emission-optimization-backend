from pydantic import BaseModel, Field
from typing import Annotated

Weight = Annotated[float, Field(ge=0, description="Quantity in kilograms or grams")]
NullableEmissions = Annotated[float | None, Field(ge=0, description="Emissions value in kg CO2e")]
AccumContributions = Annotated[float, Field(ge=0, description="Accumulated contributions")]

class ProductModel(BaseModel):
    productId: str
    productName: str
    materialId: str
    plantId: str

class ProductContributorModel(BaseModel):
    purchaseId: str
    purchaseName: str
    materialId: str
    countryOfOriginId: str
    quantityInKg: Weight
    emissionsValue: NullableEmissions

class ProductDetailsModel(BaseModel):
    productId: str
    productName: str
    materialId: str
    plantId: str
    quantityInKg: AccumContributions
    emissionsValue: NullableEmissions




