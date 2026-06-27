from transformers import pipeline, AutoTokenizer
import torch

# Use your local cached folder path here (change if needed)
MODEL_PATH = r"C:/Users/geetasai/Downloads/bart-large-cnn"

REAL_MODEL_MAX_TOKENS = 1024   
SAFE_MAX_TOKENS = 1000         
MAX_LENGTH = 400
MIN_LENGTH = 100

print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and summarization pipeline from local folder
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=True)
summarizer = pipeline("summarization", model=MODEL_PATH, tokenizer=tokenizer, device=-1)

def chunk_text(text, max_words=600):
    words = text.split()
    chunks, current_chunk = [], []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print(f"DEBUG: Prepared {len(chunks)} chunks for summarization (word-based).")
    return chunks

def split_into_windows(chunk_text):
    tokens = tokenizer.encode(chunk_text, truncation=False)
    windows = []

    for i in range(0, len(tokens), SAFE_MAX_TOKENS - 100):
        window_tokens = tokens[i:i + SAFE_MAX_TOKENS]
        window_text = tokenizer.decode(window_tokens, skip_special_tokens=True)
        windows.append(window_text)

    print(f"⚠️ Chunk too long ({len(tokens)} tokens). Split into {len(windows)} windows.")
    return windows

def summarize_chunk(chunk_text):
    try:
        tokens = tokenizer.encode(chunk_text, truncation=False)
        token_count = len(tokens)
        print(f"Chunk tokens: {token_count}")

        if token_count <= SAFE_MAX_TOKENS:
            result = summarizer(chunk_text, max_length=MAX_LENGTH, min_length=MIN_LENGTH, do_sample=False)
            return result[0]["summary_text"]
        else:
            windows = split_into_windows(chunk_text)
            window_summaries = []

            for i, window in enumerate(windows):
                print(f"  Summarizing window {i+1}/{len(windows)}...")
                try:
                    result = summarizer(window, max_length=MAX_LENGTH, min_length=MIN_LENGTH, do_sample=False)
                    window_summaries.append(result[0]["summary_text"])
                except Exception as e:
                    print(f"  ⚠️ Error in window {i+1}: {type(e).__name__}: {e}")
                    continue

            return " ".join(window_summaries).strip() if window_summaries else ""

    except Exception as e:
        print(f"⚠️ Error summarizing chunk: {type(e).__name__}: {e}")
        return ""

def summarize_text(text):
    print("Summarizing text...")
    chunks = chunk_text(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}: chars={len(chunk):,}, words={len(chunk.split()):,}")
        summary_text = summarize_chunk(chunk)

        if summary_text.strip():
            summaries.append((f"Section {i+1}", summary_text))
        else:
            print(f"⚠️ Summary failed for chunk {i+1}, including raw text instead.")
            summaries.append((f"Section {i+1}", chunk[:1500] + ("..." if len(chunk) > 1500 else "")))

    print(f"Generated {len(summaries)} summary sections\n")
    return summaries

# Example usage:
if __name__ == "__main__":
    sample_text = "Your long text goes here..."
    results = summarize_text(sample_text)
    for section, summary in results:
        print(f"{section}:\n{summary}\n")
