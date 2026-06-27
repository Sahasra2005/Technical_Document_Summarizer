from docx import Document
import fitz  # for PDFs
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text")
        return clean_text(text)

    elif ext in [".docx", ".doc"]:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            for run in para.runs:
                run_text = run.text.strip()
                if not run_text:
                    continue

                # ✅ Detect formatting importance
                if run.bold or run.underline:
                    run_text = f"[BOLD]{run_text}[/BOLD]"
                if run.font.highlight_color is not None:
                    run_text = f"[HIGHLIGHT]{run_text}[/HIGHLIGHT]"

                text += run_text + " "
            text += "\n"

        return clean_text(text)

    else:
        raise ValueError(f"Unsupported file type: {ext}")


def clean_text(text):
    return " ".join(text.split())
