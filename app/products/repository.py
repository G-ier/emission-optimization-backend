from typing import Optional
from sqlalchemy import case, func

from app.db.base import DBSession
from app.models.response_model import ProductModel, ProductContributorModel, ProductDetailsModel
from app.db.tables import Product, Contribution, Purchase, PurchaseEmissions

def product_list_repository(db_session: DBSession, mat_id: Optional[str] = None, plant_id: Optional[str] = None) -> list[ProductModel]:


    query = db_session.query(
        Product.product_id.label("productId"),
        Product.product_name.label("productName"),
        Product.material_id.label("materialId"),
        Product.plant_id.label("plantId"),
    )

    if mat_id is not None:
        query = query.filter(Product.material_id == mat_id)

    if plant_id is not None:
        query = query.filter(Product.plant_id == plant_id)

    rows = query.all()


    return [
        {
            "productId": row.productId,
            "productName": row.productName,
            "materialId": row.materialId,
            "plantId": row.plantId,
        }
        for row in rows
    ]

def product_contributors_repository(db_session: DBSession, product_id: str) -> list[ProductContributorModel]:
    # TODO: Check if product exists
    if db_session.query(Product).filter(Product.product_id == product_id).first() is None:
        return None

    query = (
        db_session.query(
            Purchase.purchase_id.label("purchaseId"),
            Purchase.purchase_name.label("purchaseName"),
            Purchase.material_id.label("materialId"),
            Purchase.country_of_origin_id.label("countryOfOriginId"),
            case(
                (Purchase.quantity_unit == 'kg', Purchase.quantity * Contribution.contribution_factor),
                (Purchase.quantity_unit == 'g',  (Purchase.quantity / 1000.0) * Contribution.contribution_factor),
            ).label("quantityInKg"),
            PurchaseEmissions.emissions_value.label("emissionsValue")
        )
        .join(Contribution, Contribution.purchase_id == Purchase.purchase_id)
        .outerjoin(PurchaseEmissions, PurchaseEmissions.purchase_id == Purchase.purchase_id)
        .filter(Contribution.product_id == product_id)
        .order_by(Purchase.purchase_id)
    )

    rows = query.all()


    return [
        {
            "purchaseId": row.purchaseId,
            "purchaseName": row.purchaseName,
            "materialId": row.materialId,
            "countryOfOriginId": row.countryOfOriginId,
            "quantityInKg": float(row.quantityInKg or 0.0),
            "emissionsValue": None if row.emissionsValue is None else float(row.emissionsValue),
        }
        for row in rows
    ]

def product_details_repository(db_session: DBSession, product_id: str) -> list[ProductDetailsModel]:

    # quantity contributed from each purchase -> in kg
    qty_kg = case(
        (Purchase.quantity_unit == 'kg', Purchase.quantity * Contribution.contribution_factor),
        (Purchase.quantity_unit == 'g',  (Purchase.quantity / 1000.0) * Contribution.contribution_factor),
        else_=0.0,
    )

    total_qty_kg = func.coalesce(func.sum(qty_kg), 0.0)

    # sum(emission * weight) / sum(weight over rows with emission)
    weighted_sum = func.coalesce(func.sum(
        case(
            (PurchaseEmissions.emissions_value.isnot(None),
             PurchaseEmissions.emissions_value * qty_kg),
            else_=0.0,
        )
    ), 0.0)

    weight_with_emissions = func.coalesce(func.sum(
        case(
            (PurchaseEmissions.emissions_value.isnot(None), qty_kg),
            else_=0.0,
        )
    ), 0.0)

    emissions_weighted_avg = weighted_sum / func.nullif(weight_with_emissions, 0.0)

    row = (
        db_session.query(
            Product.product_id.label("productId"),
            Product.product_name.label("productName"),
            Product.material_id.label("materialId"),
            Product.plant_id.label("plantId"),
            total_qty_kg.label("quantityInKg"),
            emissions_weighted_avg.label("emissionsValue"),
        )
        .filter(Product.product_id == product_id)
        .outerjoin(Contribution, Contribution.product_id == Product.product_id)
        .outerjoin(Purchase, Purchase.purchase_id == Contribution.purchase_id)
        .outerjoin(PurchaseEmissions, PurchaseEmissions.purchase_id == Purchase.purchase_id)
        .group_by(Product.product_id, Product.product_name, Product.material_id, Product.plant_id)
        .one_or_none()
    )

    if row is None:
        return None

    # return singleton
    return {
        "productId": row.productId,
        "productName": row.productName,
        "materialId": row.materialId,
        "plantId": row.plantId,
        "quantityInKg": float(row.quantityInKg or 0.0),
        "emissionsValue": None if row.emissionsValue is None else float(row.emissionsValue),
    }

