from fastapi import FastAPI, Body, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from tabulate import tabulate

app = FastAPI()

client = AsyncIOMotorClient("localhost", 27017)
db = client.collector
collections = {"users": db.users, "knives": db.knives, "availability": db.availability}

@app.post("/{collection}/")
async def create(collection: str, name: str = Body(None), surname: str = Body(None), city: str = Body(None),
                      manufacturer: str = Body(None), grip: str = Body(None), steel: str = Body(None), form: str = Body(None),
                      id_product: int = Body(None), address: str = Body(None), available: str = Body(None)):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")

    coll = collections[collection]

    n = await coll.count_documents({})
    document = {"i": n+1}
    if name:
        document.update({"Name": name})
    if surname:
        document.update({"Surname": surname})
    if city:
        document.update({"City": city})
    if manufacturer:
        document.update({"Manufacturer": manufacturer})
    if grip:
        document.update({"Grip": grip})
    if steel:
        document.update({"Steel": steel})
    if form:
        document.update({"Form": form})
    if id_product:
        document.update({"id_product": id_product})
    if address:
        document.update({"address": address})
    if available:
        document.update({"available": available})
    result = await coll.insert_one(document)
    return {"message": f"Документ с id {n+1} создан"}

@app.get("/{collection}/")
async def read(collection: str, id: int):
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")

    coll = collections[collection]

    result = await coll.find_one({"i": id}, {"_id": 0, "i": 0})
    if result:
        return {"user_info": result}
    else:
        return {"message": "Документ не существует"}

@app.put("/{collection}/")
async def update(collection: str, id: int, name: str = Body(None), surname: str = Body(None), city: str = Body(None),
                      manufacturer: str = Body(None), grip: str = Body(None), steel: str = Body(None), form: str = Body(None),
                      id_product: str = Body(None), address: str = Body(None), available: str = Body(None)):
    keys = ["Name", "Surname", "City", "Manufacturer", "Grip", "Steel", "Form", "id_product", "address", "available"]
    if collection not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")

    coll = collections[collection]

    document = {"i": id}
    result = await coll.find_one({"i": {"$lt": id}})
    keys_res = list(result.keys())
    params = []

    for i in keys:
        if i in keys_res:
            params.append(1)
        else:
            params.append(0)

    if name == None and params[0] == 1:
        name = result.get("Name")
    if surname == None and params[1] == 1:
        surname = result.get("Surname")
    if city == None and params[2] == 1:
        city = result.get("City")
    if manufacturer == None and params[3] == 1:
        manufacturer = result.get("Manufacturer")
    if grip == None and params[4] == 1:
        grip = result.get("Grip")
    if steel == None and params[5] == 1:
        steel = result.get("Steel")
    if form == None and params[6] == 1:
        form = result.get("Form")
    if id_product == None and params[7] == 1:
        id_product = result.get("id_product")
    if address == None and params[8] == 1:
        address = result.get("address")
    if available == None and params[9] == 1:
        available = result.get("available")
    if name:
        document.update({"Name": name})
    if surname:
        document.update({"Surname": surname})
    if city:
        document.update({"City": city})
    if manufacturer:
        document.update({"Manufacturer": manufacturer})
    if grip:
        document.update({"Grip": grip})
    if steel:
        document.update({"Steel": steel})
    if form:
        document.update({"Form": form})
    if id_product:
        document.update({"id_product": id_product})
    if address:
        document.update({"address": address})
    if available:
        document.update({"available": available})
    await coll.update_one({"i": id}, {"$set": document})
    return {"message": f"Документ с id {id} обновлён"}

@app.delete("/{collection}/")
async def delete(collection: str, id: int):
    if collection == "users":
        coll = db.users
    elif collection == "knives":
        coll = db.knives
    else:
        coll = db.availability

    n = await coll.count_documents({})
    await coll.delete_one({"i": id})
    new_count = await coll.count_documents({})
    return {"message": f"Документ с id {id} удалён из {collection}"}
