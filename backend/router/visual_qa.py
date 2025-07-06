from fastapi import UploadFile, File, Form, APIRouter
from backend.controllers.vqa import answer_image_question

router = APIRouter()

@router.post("/vqa")
async def vqa_endpoint(
    image: UploadFile = File(...),
    question: str = Form(...)
):
    img_bytes = await image.read()
    answer = answer_image_question(img_bytes, question)
    return {"answer": answer}
