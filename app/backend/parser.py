import pdfplumber
from docx import Document
import io

def extract_text_from_pdf(file_bytes):
    """Extract all text from a PDF file (given as bytes)."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_bytes):
    """Extract all text from a DOCX file (given as bytes)."""
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_bytes, file_type):
    """
    Main function to extract text from a resume file.
    file_type must be a MIME type:
      - 'application/pdf'
      - 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    """
    if file_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")