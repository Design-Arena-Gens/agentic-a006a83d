from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    name: str
    sku: str
    quantity: int
    reorder_level: int
    unit_cost: float
    notes: str | None = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None
    reorder_level: int | None = None
    unit_cost: float | None = None
    notes: str | None = None


class InventoryRead(InventoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
