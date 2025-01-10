import fitz  # PyMuPDF
import base64
import io

def highlight_text_in_pdf(pdf_content, text_snippets):
    """
    Highlights text snippets in a PDF and returns base64 encoded highlighted PDF
    """
    # Load PDF from bytes
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    
    # Process each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Search and highlight each text snippet
        for snippet in text_snippets:
            # Clean snippet for better matching
            clean_snippet = ' '.join(snippet.split())
            
            # Find text instances
            instances = page.search_for(clean_snippet)
            
            # Add highlight for each instance
            for inst in instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow highlight
                highlight.update()
    
    # Save the highlighted PDF to bytes
    output_buffer = io.BytesIO()
    pdf_document.save(output_buffer)
    pdf_document.close()
    
    # Convert to base64
    highlighted_pdf_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
    
    return highlighted_pdf_base64 