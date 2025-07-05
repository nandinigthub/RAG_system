import streamlit as st
import requests
import base64
import pandas as pd

st.title("📄 RAG PDF QA System")

with st.form("upload-form"):
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    submit = st.form_submit_button("Upload and Process")

if uploaded and submit:
    # Call FastAPI backend
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": uploaded}
    )

    if response.status_code != 200:
        st.error("Failed to process PDF")
    else:
        result = response.json()
        st.success("PDF uploaded and processed!")

        # TEXT 
        st.subheader("Extracted Text")
        st.text_area("Text Preview", result["text"][:2000], height=300)

        # TABLES 
        if "tables" in result and result["tables"]:
            st.subheader("Extracted Tables")
            for idx, table in enumerate(result["tables"]):
                st.markdown(f"**Table {idx+1} (Page {table['page']})**")
                df = pd.DataFrame(table["data"])
                st.dataframe(df)
        else:
            st.info("No tables detected.")

        # IMAGES 
        if "images" in result and result["images"]:
            st.subheader("Extracted Images")
            for img in result["images"]:
                image_bytes = base64.b64decode(img["base64"])
                st.image(image_bytes, caption=f"Page {img['page']} - Image {img['index']}", use_container_width =True)
        else:
            st.info("No images found.")
