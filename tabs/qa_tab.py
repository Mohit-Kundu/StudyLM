import streamlit as st
from utils.snowflake_manager import SnowflakeManager
from utils.pdf_highlighter import highlight_text_in_pdf
import streamlit.components.v1 as components

def show():
    st.header("Ask Questions About Your Documents")
    
    if not st.session_state.documents:
        st.warning("Please upload and process documents first in the Upload tab.")
        return
    
    # Question input
    question = st.text_input("Ask a question about your documents:")
    
    if question:
        with st.spinner("Searching for answer..."):
            snowflake = SnowflakeManager()
            
            # Get answer and relevant contexts
            answer, contexts = snowflake.query_documents(question)
            
            # Display answer
            st.subheader("Answer:")
            st.write(answer)
            
            # Display relevant document sections
            st.subheader("Relevant Document Sections:")
            
            # Create two columns for the layout
            doc_col, highlight_col = st.columns([1, 1])
            
            with doc_col:
                for ctx in contexts:
                    with st.expander(f"From: {ctx['document_name']}"):
                        st.write(ctx['text'])
            
            with highlight_col:
                if any(doc.endswith('.pdf') for doc in [ctx['document_name'] for ctx in contexts]):
                    # Get the PDF document
                    pdf_docs = [doc for doc in st.session_state.documents if doc['name'].endswith('.pdf')]
                    
                    if pdf_docs:
                        selected_pdf = st.selectbox(
                            "Select PDF to view highlights:",
                            options=[doc['name'] for doc in pdf_docs]
                        )
                        
                        # Get relevant text snippets for highlighting
                        highlights = [ctx['text'] for ctx in contexts 
                                   if ctx['document_name'] == selected_pdf]
                        
                        # Display highlighted PDF
                        highlighted_pdf = highlight_text_in_pdf(
                            next(doc for doc in pdf_docs if doc['name'] == selected_pdf)['content'],
                            highlights
                        )
                        
                        # Display PDF viewer with highlights
                        components.html(
                            f'''
                            <iframe 
                                src="data:application/pdf;base64,{highlighted_pdf}"
                                width="100%"
                                height="800px"
                                type="application/pdf"
                            ></iframe>
                            ''',
                            height=800,
                        ) 