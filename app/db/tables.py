from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AppBase(DeclarativeBase):
    pass


class Product(AppBase):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    material_id: Mapped[str]
    plant_id: Mapped[str]


class Purchase(AppBase):
    __tablename__ = "purchases"

    purchase_id: Mapped[str] = mapped_column(primary_key=True)
    purchase_name: Mapped[str | None]
    material_id: Mapped[str]
    country_of_origin_id: Mapped[str]
    quantity: Mapped[float]
    quantity_unit: Mapped[str]


class Contribution(AppBase):
    __tablename__ = "contribution"

    purchase_id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(primary_key=True)
    contribution_factor: Mapped[float]


class PurchaseEmissions(AppBase):
    __tablename__ = "purchase_emissions"

    purchase_id: Mapped[str] = mapped_column(primary_key=True)
    emissions_value: Mapped[float]
