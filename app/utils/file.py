import os
import aiofiles

async def save_to_disk(path: str, file: bytes) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        async with aiofiles.open(path,"wb") as f:
            await f.write(file)
        return True
    except Exception as e:
        print(f"Error saving file to disk: {e}")
        return False