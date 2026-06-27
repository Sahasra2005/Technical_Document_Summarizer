# import streamlit as st
# from io import BytesIO
# from PyPDF2 import PdfReader
# from transformers import pipeline
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4

# # Load summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # 🔹 Extract text from uploaded PDF
# def extract_text_from_pdf(uploaded_file):
#     reader = PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text
#     return text

# # 🔹 Split text into chunks for summarization
# def chunk_text(text, max_chunk_size=1000):
#     chunks = []
#     while len(text) > max_chunk_size:
#         split_at = text[:max_chunk_size].rfind(".")
#         if split_at == -1:
#             split_at = max_chunk_size
#         chunks.append(text[:split_at+1])
#         text = text[split_at+1:]
#     if text:
#         chunks.append(text)
#     return chunks

# # 🔹 Summarize each chunk using BART
# def summarize_chunks(chunks):
#     summaries = []
#     for chunk in chunks:
#         summary = summarizer(chunk, max_length=300, min_length=100, do_sample=False)[0]['summary_text']
#         summaries.append(summary)
#     return summaries

# # 🔹 Generate PDF from summaries
# def generate_pdf(summaries):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     story = []
#     for i, summary in enumerate(summaries):
#         story.append(Paragraph(f"Section {i+1}", styles["Heading2"]))
#         story.append(Spacer(1, 12))
#         story.append(Paragraph(summary, styles["BodyText"]))
#         story.append(Spacer(1, 24))
#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # 🔹 Streamlit UI
# st.set_page_config(page_title="Document Summarizer", layout="centered")
# st.title("📄 Document Summarizer")

# uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# if uploaded_file:
#     st.success("File uploaded successfully!")
#     if st.button("Summarize Document"):
#         with st.spinner("Extracting and summarizing..."):
#             raw_text = extract_text_from_pdf(uploaded_file)
#             chunks = chunk_text(raw_text)
#             summaries = summarize_chunks(chunks)
#             pdf_output = generate_pdf(summaries)
#         st.success("Summary generated!")
#         st.download_button("Download Summary PDF", data=pdf_output, file_name="summary.pdf", mime="application/pdf")
