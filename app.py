import streamlit as st
from dotenv import load_dotenv
import os
from tabs import upload_tab, qa_tab, flashcard_tab

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="Document Learning Assistant", layout="wide")
    
    # Initialize session state for storing documents and embeddings
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = None
        
    st.title("Document Learning Assistant")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "📁 Upload Documents", 
        "❓ Ask Questions", 
        "🔄 Flashcards"
    ])
    
    with tab1:
        upload_tab.show()
    
    with tab2:
        qa_tab.show()
        
    with tab3:
        flashcard_tab.show()

if __name__ == "__main__":
    main() 