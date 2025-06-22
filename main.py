import asyncio
from contextlib import asynccontextmanager
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from server.api import router
from server.database import orders

async def broadcast(data):
    text = json.dumps(data, default=str)
    for client in clients.copy():
        try:
            await client.send_text(text)
        except:
            clients.remove(client)

async def watch_order_changes():
    pipeline = [{"$match": {"operationType": {"$in": ["insert", "update", "replace", "delete"]}}}]
    async with orders.watch(
        pipeline,
        full_document="updateLookup",
        full_document_before_change="required"
    ) as stream:
        async for change in stream:
            doc_id = change["documentKey"]["_id"]
            before = change.get("fullDocumentBeforeChange", {})
            after = change.get("fullDocument", {})
            await broadcast({
                "event": change["operationType"],
                "document_id": str(doc_id),
                "before": before,
                "after": after
            })

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(watch_order_changes())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("static/index.html") as f:
        return f.read()
