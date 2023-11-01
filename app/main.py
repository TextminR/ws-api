import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, HTTPException, status
from app.model.models import *
import uvicorn
from fastapi.responses import Response

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:mongo@localhost:27017/")
db = client.text
text_collection = db.get_collection("text")


@app.get("/findAllTexts", response_model=TextMetadataCollection)
async def findAllTexts():
    projection = {"_id": 1, "autor": 1, "titel": 1, "year": 1}
    return TextMetadataCollection(textdata=await text_collection.find({}, projection).to_list(1000))


@app.get("/texts/{textid}", response_model=TextModel)
async def findTextById(textid):
    if (
            text := await text_collection.find_one({"_id": ObjectId(textid)})
    ) is not None:
        return text

    raise HTTPException(status_code=404, detail=f"Text {textid} not found.")


@app.post("/getTitelBetweenYears/", response_model=List[str])
async def getTitelBetweenYears(minYear: int, maxYear: int):
    result = []
    async for doc in text_collection.find({"year": {'$lt': maxYear, '$gte': minYear}}, {"_id": 0, "titel": 1}):
        result.append(doc["titel"])
    return result


@app.post("/getTitelByYear/", response_model=List[str])
async def getTitelByYear(year: int):
    result = []
    async for doc in text_collection.find({"year": year}, {"_id": 0, "titel": 1}):
        result.append(doc["titel"])
    return result


@app.post("/createText/", response_model=TextModel)
async def create_text(text: TextModel):
    new_text = await text_collection.insert_one(text.model_dump(by_alias=True, exclude=["id"]))
    created_text = await text_collection.find_one({"_id": new_text.inserted_id})
    return created_text


@app.post("/getTitleByAuthor/", response_model=List[str])
async def getTitleByAuthor(author: str):
    result = []
    async for doc in text_collection.find({"autor": author}, {"_id": 0, "titel": 1}):
        result.append(doc["titel"])
    return result


@app.post("/getTextByTitle/", response_model=TextCollection)
async def getTextByTitle(titel: str):
    return TextCollection(texts=await text_collection.find({"titel": titel}).to_list(1000))


@app.post("/getTextByAuthor/", response_model=TextCollection)
async def getTextByAuthor(autor: str):
    return TextCollection(texts=await text_collection.find({"autor": autor}).to_list(1000))


@app.post("/getTextByYear/", response_model=TextCollection)
async def getTextByYear(year: int):
    return TextCollection(texts=await text_collection.find({"year": year}).to_list(1000))


@app.post("/getBirthplaceOfAuthor/", response_model=str)
def getBirthplaceOfAuthor(authorname: str):
    return "Warwickshire"


@app.post("/getTextBetweenYears/", response_model=TextCollection)
async def getTextByYearBetween(minYear: int, maxYear: int):
    return TextCollection(texts=await text_collection.find({"year": {'$lt': maxYear, '$gte': minYear}}).to_list(1000))


@app.delete("/deleteText/{textid}")
async def deleteText(textid):
    delete_result = await text_collection.delete_one({"_id": ObjectId(textid)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Text {textid} not found")


@app.get("/")
async def hello():
    return "hi"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
