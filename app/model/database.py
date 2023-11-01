import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:mongo@localhost:27017/text")
db = client.text
text_collection = db.get_collection("text")

