from dotenv import load_dotenv
from ..db.collections.files import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
import base64
from google import genai
from google.genai import types
import io

load_dotenv()
client = genai.Client()

async def process_file(id: str, file_path: str):
    await files_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": {"status": "processing"}}
    )

    # convert PDF pages into PIL Image objects
    pages = convert_from_path(file_path)

    image_parts = []
    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')

        # Convert in-memory PIL image directly to raw bytes
        img_byte_arr = io.BytesIO()
        page.save(img_byte_arr, format='JPEG')
        
        image_parts.append(
            types.Part.from_bytes(
                data=img_byte_arr.getvalue(),
                mime_type="image/jpeg"
            )
        )

    result = await client.aio.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "Based on the resume below, roast this resume:",
            *image_parts,
        ],
    )

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "processed",
            "result": result.text
        }
    })
