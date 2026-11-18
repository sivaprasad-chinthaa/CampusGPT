from pathlib import Path

MAX_QUESTION_CHARS = 1500
MAX_FILE_MB = 10

def validate_question(question: str):
    q = (question or "").strip()
    if not q:
        return False, "Please enter a question."
    if len(q) > MAX_QUESTION_CHARS:
        return False, f"Please keep the question below {MAX_QUESTION_CHARS} characters."
    return True, ""

def validate_pdf(uploaded_file):
    if uploaded_file is None:
        return False, "No file selected."
    if not uploaded_file.name.lower().endswith('.pdf'):
        return False, "CampusGPT currently accepts PDF files only."
    size = getattr(uploaded_file, 'size', 0) or 0
    if size > MAX_FILE_MB * 1024 * 1024:
        return False, f"Please upload PDFs smaller than {MAX_FILE_MB} MB."
    return True, ""
