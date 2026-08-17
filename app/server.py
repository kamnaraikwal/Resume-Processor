from bson import ObjectId
from fastapi import FastAPI, UploadFile, Path
from uuid import uuid4
from .utils.file import save_to_disk
from .db.collections.files import files_collection, FileSchema
from .queue.q import q
from .queue.workers import process_file


app = FastAPI()

@app.get("/")
async def test():
    return {"Status": "Healthy"}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile):
    db_file = await files_collection.insert_one(
        document=FileSchema(
            name=file.filename,
            status="saving"
        )
    )

    file_path = f"/mnt/uploads/{str(db_file.inserted_id)}/{file.filename}"

    await save_to_disk(file=await file.read(), path=file_path)

    # Push to Queue
    q.enqueue(process_file, str(db_file.inserted_id), file_path)

    # MongoDB Save
    await files_collection.update_one({"_id": db_file.inserted_id}, {
        "$set": {
            "status": "queued"
        }
    })

    return {"file_id": str(db_file.inserted_id)}

@app.get("/{id}")
async def get_file_by_id(id: str = Path(..., description="ID of the file")):
    db_file = await files_collection.find_one({"_id": ObjectId(id)})

    print(db_file)

    return {
        "_id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "result": db_file["result"] if "result" in db_file else None,
    }