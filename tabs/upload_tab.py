import streamlit as st
from utils.document_processor import process_document
from utils.snowflake_manager import SnowflakeManager
import tempfile

def show():
    st.header("Upload Your Documents")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload your documents (PDF, TXT, MP3, WAV)", 
        accept_multiple_files=True,
        type=['pdf', 'txt', 'mp3', 'wav']
    )
    
    if uploaded_files:
        if st.button("Process Documents"):
            with st.spinner("Processing documents and generating embeddings..."):
                snowflake = SnowflakeManager()
                
                for file in uploaded_files:
                    # Save temporary file
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Process document
                    processed_doc = process_document(tmp_path, file.name)
                    
                    # Store in Snowflake
                    snowflake.store_document(processed_doc)
                    
                    # Update session state
                    st.session_state.documents.append(processed_doc)
                
                st.success("Documents processed successfully!") 