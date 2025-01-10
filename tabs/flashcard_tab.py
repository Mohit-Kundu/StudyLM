import streamlit as st
from utils.snowflake_manager import SnowflakeManager
from streamlit_card import card
import random

def generate_flashcards(document_content, num_cards=5):
    """Generate flashcards using Mistral AI"""
    snowflake = SnowflakeManager()
    
    prompt = f"""Based on the following content, generate {num_cards} flashcards. 
    Each flashcard should have a question on one side and the answer on the other side.
    Include a mix of:
    - Definitions
    - Fill in the blanks
    - Conceptual questions
    - True/False questions
    
    Format your response as a list of JSON objects like this:
    [
        {{"question": "What is X?", "answer": "X is Y"}},
        {{"question": "True or False: Z", "answer": "True, because..."}},
        ...
    ]
    
    Content: {document_content}
    """
    
    # Use Mistral to generate flashcards
    messages = [
        {"role": "system", "content": "You are a helpful assistant that creates educational flashcards."},
        {"role": "user", "content": prompt}
    ]
    
    response = snowflake.mistral_client.chat(
        model="mistral-large-2",
        messages=messages
    )
    
    # Parse the response to get flashcards
    import json
    try:
        flashcards = json.loads(response.choices[0].message.content)
        return flashcards
    except:
        st.error("Error generating flashcards. Please try again.")
        return []

def show():
    st.header("Flashcards")
    
    if not st.session_state.documents:
        st.warning("Please upload and process documents first in the Upload tab.")
        return
    
    # Initialize session state for flashcards
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = []
    if 'current_card' not in st.session_state:
        st.session_state.current_card = 0
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
        
    # Document selection
    selected_doc = st.selectbox(
        "Select a document to generate flashcards from:",
        options=[doc['name'] for doc in st.session_state.documents]
    )
    
    num_cards = st.slider("Number of flashcards to generate:", 5, 20, 10)
    
    # Generate button
    if st.button("Generate Flashcards"):
        with st.spinner("Generating flashcards..."):
            doc_content = next(
                doc['content'] for doc in st.session_state.documents 
                if doc['name'] == selected_doc
            )
            st.session_state.flashcards = generate_flashcards(doc_content, num_cards)
            st.session_state.current_card = 0
            st.session_state.show_answer = False
    
    # Display flashcards
    if st.session_state.flashcards:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("Previous Card") and st.session_state.current_card > 0:
                st.session_state.current_card -= 1
                st.session_state.show_answer = False
        
        with col3:
            if st.button("Next Card") and st.session_state.current_card < len(st.session_state.flashcards) - 1:
                st.session_state.current_card += 1
                st.session_state.show_answer = False
        
        current_flashcard = st.session_state.flashcards[st.session_state.current_card]
        
        # Display card counter
        st.write(f"Card {st.session_state.current_card + 1} of {len(st.session_state.flashcards)}")
        
        # Create clickable card
        card_clicked = card(
            title="",
            text=current_flashcard['question'] if not st.session_state.show_answer else current_flashcard['answer'],
            image="",
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "border-radius": "10px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.1)",
                    "cursor": "pointer",
                    "background-color": "#f0f2f6",
                    "transition": "transform 0.3s ease",
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "padding": "20px",
                    "text-align": "center"
                }
            }
        )
        
        # Toggle answer when card is clicked
        if card_clicked:
            st.session_state.show_answer = not st.session_state.show_answer
        
        # Show hint to click
        st.caption("Click the card to flip it!")
        
        # Shuffle button
        if st.button("Shuffle Cards"):
            random.shuffle(st.session_state.flashcards)
            st.session_state.current_card = 0
            st.session_state.show_answer = False 