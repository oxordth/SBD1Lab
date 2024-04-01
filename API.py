import pymongo
from fastapi import FastAPI, Body, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

app = FastAPI()

class Repository:
    def __init__(self, db):
        self.db = db

    async def create_document(self, collection_name: str, document: dict):
        coll = self.db[collection_name]
        result = await coll.insert_one(document)
        return {"message": f"Document with id {result.inserted_id} created"}

    async def get_document(self, collection_name: str, document_id: int):
        coll = self.db[collection_name]
        document = await coll.find_one({"i": document_id}, {"_id": 0, "i": 0})
        return document

    async def update_document(self, collection_name: str, document_id: int, update_data: dict):
        coll = self.db[collection_name]
        await coll.update_one({"i": document_id}, {"$set": update_data})
        return {"message": f"Document with id {document_id} updated"}

    async def delete_document(self, collection_name: str, document_id: int):
        coll = self.db[collection_name]
        await coll.delete_one({"i": document_id})
        return {"message": f"Document with id {document_id} deleted from {collection_name}"}

client = AsyncIOMotorClient("localhost", 27017)
db = client.collector
collections = {"users": db.users, "knives": db.knives, "availability": db.availability}

db.users.create_index([("City", pymongo.DESCENDING)])
db.knives.create_index([("Form", pymongo.DESCENDING)])
db.availability.create_index([("address", pymongo.DESCENDING)])

repos = Repository(db)

@app.post("/{collection}/")
async def create_document(collection: str, data: dict = Body(...)):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    return await repos.create_document(collection, data)

@app.get("/{collection}/")
async def get_document(collection: str, id: int):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    document = await repos.get_document(collection, id)
    if document:
        return {"user_info": document}
    else:
        return {"message": "Document does not exist"}

@app.put("/{collection}/")
async def update_document(collection: str, id: int, data: dict = Body(...)):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    return await repos.update_document(collection, id, data)

@app.delete("/{collection}/")
async def delete_document(collection: str, id: int):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    return await repos.delete_document(collection, id)
