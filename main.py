import os

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# 獲取 MongoDB 連接字符串
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.test_database  # 這是你要使用的資料庫
collection = db.test_collection  # 這是你要使用的集合


class Item(BaseModel):
    name: str
    description: str


@app.get('/')
def home():
    return "Hello, Test App!"


@app.delete("/del_item/{item_name}")
def delete_item(item_name: str):
    result = collection.delete_one({"name": item_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Deleted {item_name} from database"}


@app.put("/add_item/")
def add_item(item: Item):
    collection.update_one(
        {"name": item.name},
        {"$set": item.dict()},
        upsert=True  # 存在則更新，不存在則插入
    )
    return {"message": "Item name: {} added or updated!".format(item.name),
            "item": item}


@app.get("/get_items/")
def get_items():
    try:
        items = list(collection.find({}, {"_id": 0}))
        return {"data": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving items: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
