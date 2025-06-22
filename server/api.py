from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from typing import Dict

from server.database import orders
from server.model import OrderSchema, UpdateOrderSchema

router = APIRouter()

@router.post("/api/orders",)
async def create_order(payload: OrderSchema) -> Dict[str, str]:
    order = payload.model_dump()
    result = await orders.insert_one(order)
    return {"id": str(result.inserted_id)}

@router.put("/api/orders/{id}")
async def update_order(id: str, payload: UpdateOrderSchema) -> Dict[str, str]:
    if not await orders.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404, detail="Order not found")
    await orders.update_one({"_id": ObjectId(id)}, {"$set": payload.model_dump(exclude_unset=True)})
    return {"updated": str(id)}

@router.delete("/api/orders/{id}")
async def delete_order(id: str) -> Dict[str, str]:
    result = await orders.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"deleted": str(id)}

