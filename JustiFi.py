import os
from PyPDF2 import PdfReader
import streamlit as st
from model import query_gemma2_model  # Import the function from model.py

# --------- STEP 1: Load and Process Legal Documents ---------
def load_documents(pdf_folder):
    documents = []
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file_name)
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            documents.append({"content": text, "title": file_name})
    return documents


def split_text_into_chunks(text, chunk_size=512, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks


# --------- STEP 3: Streamlit UI ---------
def main():
    st.title("JustiFi")
    st.sidebar.header("Upload Legal Documents")

    # Upload and process PDFs
    pdf_folder = "legal_documents"
    os.makedirs(pdf_folder, exist_ok=True)
    uploaded_files = st.sidebar.file_uploader("Upload Legal PDFs", accept_multiple_files=True, type=["pdf"])
    for uploaded_file in uploaded_files:
        with open(os.path.join(pdf_folder, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

    # Load PDFs and split text into chunks
    documents = load_documents(pdf_folder)
    all_chunks = []
    for doc in documents:
        chunks = split_text_into_chunks(doc["content"])
        all_chunks.extend(chunks)

    # User Query
    query = st.text_input("Ask your legal question:")
    if query:
        st.write("Processing your query...")
        
        # Use top chunks as context (optional)
        context = " ".join(all_chunks[:5])
        prompt = f"Context: {context}\n\nQuery: {query}\n\nResponse:"

        # Query the model
        response = query_gemma2_model(prompt)
        
        st.subheader("Chatbot Response:")
        st.write(response)


if __name__ == "__main__":
    main()

