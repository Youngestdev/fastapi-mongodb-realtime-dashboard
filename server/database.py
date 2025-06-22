from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(DATABASE_URL)
database = client.orders

orders = database.get_collection("orders")