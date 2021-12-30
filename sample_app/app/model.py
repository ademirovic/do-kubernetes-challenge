from datetime import datetime
from enum import Enum
from pydantic import BaseModel, conlist, conint
from uuid import UUID


class IceCreamType(str, Enum):
    banana = "banana"
    chocolate = "chocolate"
    lemon = "lemon"
    pistachio = "pistachio"
    raspberry = "raspberry"
    strawberry = "strawberry"
    vanilla = "vanilla"


class Scoop(BaseModel):
    type: IceCreamType
    quantity: conint(gt=0)
    price: conint(gt=0)

    class Config:
        use_enum_values = True


class Purchase(BaseModel):
    shop_id: UUID
    purchase_id: UUID
    timestamp: datetime
    scoops: conlist(Scoop, min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "shop_id": "9231c55f-b16c-45b8-b71e-731521495046",
                "purchase_id": "a430ef3a-86f3-4132-9474-a87c448fdb49",
                "timestamp": "2021-12-28 12:00:00+00",
                "scoops": [{"type": "chocolate", "quantity": 2, "price": 200}],
            }
        }
