from fastapi import UploadFile, File, Form, APIRouter
from backend.controller.vqa import answer_image_question
from backend.controller.vector_db import search_similar
from backend.schemas.qa import QuestionRequest

router = APIRouter()

@router.post("/vqa")
async def vqa_endpoint(
    image: UploadFile = File(...),
    question: str = Form(...)
):
    img_bytes = await image.read()
    answer = answer_image_question(img_bytes, question)
    return {"answer": answer}


@router.post("/qa")
def ask_question(request:QuestionRequest):
    results = search_similar(request.query)
    print(results)
    
    ans =  {
        "matches": [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
            } for hit in results
        ]
    }
    print(ans)
    return ans
