from typing import Optional

from fastapi import APIRouter, HTTPException

from app.db.base import DBSession
from app.models.response_model import ProductModel, ProductContributorModel, ProductDetailsModel
from app.products.service import product_list_service, product_contributors_service, product_details_service

products_router = APIRouter(prefix="/products", tags=["Products"])


def _normalize_query_param(value: Optional[str]) -> Optional[str]:
    """Treat empty or whitespace-only strings as None."""
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


@products_router.get("")
def get_product_list(db_session: DBSession, mat_id: Optional[str] = None, plant_id: Optional[str] = None) -> list[ProductModel]:
    # Normalize empty/whitespace-only strings to None so filters are applied only when provided
    mat_id = _normalize_query_param(mat_id)
    plant_id = _normalize_query_param(plant_id)

    products = product_list_service(db_session, mat_id, plant_id)
    
    if products is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return products

@products_router.get("/{product_id}/contributors")
def get_product_contributors(db_session: DBSession, product_id: str) -> list[ProductContributorModel]:

    contributors = product_contributors_service(db_session, product_id)

    if contributors is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return contributors

@products_router.get("/{product_id}/details")
def get_product_contributors(db_session: DBSession, product_id: str) -> ProductDetailsModel:

    details = product_details_service(db_session, product_id)

    if details is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return details