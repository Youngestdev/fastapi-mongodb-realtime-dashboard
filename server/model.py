from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class OrderSchema(BaseModel):
    item: str = Field(..., example="FastAPI Course By TestDriven")
    customer: str = Field(..., example="Abdulazeez Abdulazeez Adeshina")
    status: Optional[str] = Field("pending", example="pending")
    created_at: datetime = datetime.now()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "item": "FastAPI Course By TestDriven",
                "customer": "Abdulazeez Abdulazeez Adeshina",
                "status": "pending"
            }
        }
    )

class UpdateOrderSchema(BaseModel):
    status: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "completed"
            }
        }
    )