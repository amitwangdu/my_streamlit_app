import streamlit as st
from chroma_helper import ChromaHelper

# Initialize the Chroma helper with a specific collection name
chroma_helper = ChromaHelper("my_file_collection")

st.title("File Upload and Search with ChromaDB")

# Upload File Section
st.header("Upload a File")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "md"])

# Section to show all existing file names in the database
st.header("Files Currently in the Database")
existing_files = chroma_helper.get_all_file_names()
if existing_files:
    st.write("The following files are already stored in the database:")
    st.write(existing_files)
else:
    st.write("No files found in the database.")

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    doc_id = uploaded_file.name

    # Check for exact matches before uploading
    similar_docs = chroma_helper.get_similar_documents(file_content)
    if similar_docs:
        st.warning(f"This file is identical to existing files in the database: {', '.join(similar_docs)}")
    else:
        chroma_helper.upsert_document(doc_id, file_content)
        st.success(f"File '{doc_id}' uploaded and stored in the database.")
