from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router.upload_pdf import router as upload
from backend.router.visual_qa import router as vqa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload, prefix="/extract")
app.include_router(vqa, prefix="/ask")
