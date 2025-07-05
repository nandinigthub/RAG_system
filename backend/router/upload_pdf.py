from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from backend.controllers.pdf_parser import parse_pdf
import base64

router = APIRouter()

@router.post("/pdf")
async def extract_pdf(file: UploadFile = File(...)):
    content, tables, images = parse_pdf(file)
    
    base64_images = []

    for img_info in images:
        img_bytes = img_info["image"]
        encoded = base64.b64encode(img_bytes).decode("utf-8")
        base64_images.append({
            "page": img_info["page"],
            "index": img_info["index"],
            "base64": encoded
        })

    return JSONResponse({
        "message": "PDF processed",
        "text": content,
        "num_images": len(base64_images),
        "images": base64_images,
        "tables":tables
    })
