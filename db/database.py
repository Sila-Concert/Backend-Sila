# driver for mongodb
import motor.motor_asyncio
from models.PyObjectId import PyObjectId

MONGODB_URL = "mongodb://testuser:test123@localhost:27017"
DATABASE_NAME = "online_shop_db"


class Database():
    def __init__(self) -> None:
        self.connected = False
        self.mongodb_client = None

    async def db_connection(self):
        if self.connected == False:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
            self.connected = True
        db = self.client[DATABASE_NAME]
        return db


database = Database()

# Add a new product into the database


async def add_product(product_data: dict):
    db = await database.db_connection()
    product = await db.product.insert_one(product_data)
    new_product = await db.product.find_one({"_id": product.inserted_id})
    return to_product(new_product)


# Retrieve a product by id
async def read_product(id: str):
    db = await database.db_connection()
    product = await db.product.find_one({"_id": PyObjectId(id)})
    if product:
        return to_product(product)
    return None


# Update a product by id
async def update_product(id: str, product_data: dict):
    if len(product_data) < 1:
        return False
    db = await database.db_connection()
    product = await db.product.find_one({"_id": PyObjectId(id)})
    if product:
        product["name"] = product_data.get("name")
        product["price"] = product_data.get("price")
        product["updated_by"] = product_data.get("updated_by")
        updated_product = await db.product.update_one({"_id": PyObjectId(id)}, {"$set": product})
        return updated_product.acknowledged
    return False

# Delete a product from the database


async def delete_product(id: str):
    db = await database.db_connection()
    product = await db.product.find_one({"_id": PyObjectId(id)})
    if product:
        await db.product.delete_one({"_id": PyObjectId(id)})
        return True
    else:
        return False


def to_product(item) -> dict:
    return {
        "id": str(item.get("_id")),
        "name": item.get("name"),
        "price": item.get("price"),
        "created_at": item.get("created_at"),
        "created_by": item.get("created_by"),
        "updated_at": item.get("updated_at"),
        "updated_by": item.get("updated_by")
    }

def to_product_list(items) -> list:
    return [to_product(item) for item in items]