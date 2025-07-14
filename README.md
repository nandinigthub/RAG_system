# RAG_system
# PDF QA System with VQA Support

This project is a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to upload PDFs and ask questions about the content, including **text**, **tables**, and **images** using both **language** and **vision-language models**. It includes a FastAPI backend, a Streamlit frontend, and integrates with **Qdrant** as a vector store.

---

## Features Implemented

### 1. PDF Parsing & Extraction

* Extracts **raw text**, **tables**, and **images** from uploaded PDFs.
* Images are returned in **base64** format.
* Tables are returned as structured data.
* Endpoint: `POST /extract/pdf`

### 2. Vector Store Integration (Qdrant)

* Chunks the extracted text and tables.
* Embeds them using `sentence-transformers/all-mpnet-base-v2`.
* Stores vector embeddings in a local Qdrant instance.
* Enables similarity search to retrieve context for questions.

### 3. Visual Question Answering (VQA)

* Supports asking questions about **images extracted from the PDF**.
* Uses the **BLIP model** (`blip-vqa-base`) for VQA.
* Endpoint: `POST ask/vqa`

### 4. Frontend Integration (Streamlit)

* Upload a PDF and visualize extracted **text**, **tables**, and **images**.
* Ask questions on document content using **RAG**.
* Ask questions on **images** using **VQA**.

---

## Folder Structure

```
backend/
├── controller/
│   ├── pdf_chunker.py
│   ├── pdf_parser.py
│   ├── vqa.py
│   └── vector_db.py
├── schemas/
│   ├── qa.py
├── router/
│   ├── upload_pdf.py
│   ├── qa.py
└── main.py

frontend/
└── pages/
│   ├── main.py
```

---

##  How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/RAG_system
cd backend 
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Qdrant Locally

Make sure Docker is installed. Then run:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 4. Start the FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

### 5. Run the Streamlit Frontend

```bash
cd frontend
streamlit run pages/main.py
```

---

## Requirements

Add these to your `requirements.txt`:

```txt
fastapi
uvicorn
python-multipart
PyMuPDF
pandas
qdrant-client
sentence-transformers
streamlit
Pillow
transformers
torch
langchain
langchain-community
langchain-openai
```

---

## 🔗 Endpoints Summary

| Method | Endpoint       | Description                         |
| ------ | -------------- | ----------------------------------- |
| POST   | `/extract/pdf` | Upload and extract content from PDF |
| POST   | `ask/vqa`         | Visual question answering on images |
| POST   | `ask/qa`          | Ask questions on document content   |
