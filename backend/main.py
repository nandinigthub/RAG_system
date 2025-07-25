from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router.upload_pdf import router as upload
from backend.router.qa import router as vqa
from backend.controller.vector_db import init_qdrant

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    init_qdrant()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload, prefix="/extract")
app.include_router(vqa, prefix="/ask")
