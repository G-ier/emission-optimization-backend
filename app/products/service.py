from typing import Optional

from app.db.base import DBSession
from app.models.response_model import ProductModel, ProductContributorModel, ProductDetailsModel
from app.products.repository import product_list_repository, product_contributors_repository, product_details_repository

# Empty services -> only call repo
def product_list_service(db_session: DBSession, mat_id: Optional[str] = None, plant_id: Optional[str] = None) -> list[ProductModel]:
    
    return product_list_repository(db_session, mat_id, plant_id)

def product_contributors_service(db_session: DBSession, product_id: str) -> list[ProductContributorModel]:
    
    return product_contributors_repository(db_session, product_id)

def product_details_service(db_session: DBSession, product_id: str) -> list[ProductDetailsModel]:

    return product_details_repository(db_session, product_id)
