from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import google.genai as genai
from PIL import Image as PILImage
import io
from utils import *

mcp = FastMCP("Neuron MCP")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

image_model = "gemini-2.5-flash-image"

@mcp.tool()
async def create_image(input: str) -> str:
    """
    Gera imagem e retorna URL
    
    """
    try:
        response = client.models.generate_content(
            model=image_model,
            contents=input
        )

        for part in getattr(response, "parts", []):
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                img = inline_data.data

                file_path = save_image_locally(data)

                image_url = create_img_url(file_path)
                
                return image_url

    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

    return None

STORAGE_DIR = r"C:\Users\https\Desktop\trabalho_sd"

@mcp.tool()
async def list_files() -> dict:
    """
    Lista arquivos com metadados.
    """
    import time
    files = []
    for name in os.listdir(STORAGE_DIR):
        path = os.path.join(STORAGE_DIR, name)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": name,
                "size": stat.st_size,
                "modified": time.ctime(stat.st_mtime)
            })
    return {"files": files}

@mcp.tool()
async def search_in_files(query: str) -> dict:
    """
    Procura texto em todos os arquivos legíveis.
    """
    matches = []

    for name in os.listdir(STORAGE_DIR):
        path = os.path.join(STORAGE_DIR, name)
        if not os.path.isfile(path):
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if query.lower() in line.lower():
                        matches.append({
                            "file": name,
                            "line": i + 1,
                            "text": line.strip()
                        })
        except:
            # ignora arquivos binários
            continue

    return {"results": matches}

@mcp.tool()
async def read_file_chunk(name: str, offset: int = 0, length: int = 2048) -> dict:
    """
    Lê uma parte do arquivo, útil para arquivos grandes.
    """
    safe = os.path.basename(name)
    path = os.path.join(STORAGE_DIR, safe)

    if not os.path.exists(path):
        return {"error": "file not found"}

    with open(path, "rb") as f:
        f.seek(offset)
        data = f.read(length)

    return {
        "name": safe,
        "offset": offset,
        "length": len(data),
        "content_b64": data.decode("latin1")  # ou base64
    }

if __name__ == "__main__":
    mcp.run()
