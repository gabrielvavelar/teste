import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
import uuid
from pathlib import Path

load_dotenv()

cloudinary.config( 
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Cria a pasta storage se não existir

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


def save_image_locally(img: bytes) -> str:
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = STORAGE_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(img)

    return str(file_path)


def create_img_url(file_path: str) -> str:
    # Cloudinary precisa do caminho completo do arquivo
    result = cloudinary.uploader.upload(
        file_path,
        resource_type="image"
    )

    return result["secure_url"]
