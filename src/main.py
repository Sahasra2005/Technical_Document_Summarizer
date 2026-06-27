import os
import time
from datetime import datetime
from extractor import extract_text, clean_text
from summarizer import summarize_text
from report import generate_pdf

# Paths
INPUT_FILE = "C:/Users/geetasai/Downloads/doc_summarizer/doc_summarizer/input/story.docx"
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "..", "output", "summary_story.pdf")


def main():
    run_times = []  
    total_runs = 5

    print("===== Document Summarization Benchmark =====\n")

    for i in range(total_runs):
        print(f"\n----- Run {i + 1} of {total_runs} -----")
        start_time = time.time()
        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Start time: {start_timestamp}")

        # Step 1: Extract text
        print("Extracting text...")
        text = extract_text(INPUT_FILE)
        text = clean_text(text) if text else ""

        print(f"Extracted text length: {len(text)} characters")

        # Step 2: Summarize
        print("Summarizing text...")
        summary = summarize_text(text)

        print(f"Generated {len(summary)} summary sections")

        # Step 3: Preview part of summary in console
        for idx, (title, s) in enumerate(summary, 1):
            print(f"\n--- {title} ---")
            print(s[:200] + "..." if len(s) > 200 else s)
        
        # Step 4: Generate PDF
        print("Generating PDF report...")
        generate_pdf(summary, OUTPUT_PDF)

        end_time = time.time()
        elapsed = end_time - start_time
        run_times.append(elapsed)

        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"End time: {end_timestamp}")
        print(f"Run {i + 1} execution time: {elapsed:.2f} seconds")

    # Final results
    avg_time = sum(run_times) / len(run_times)
    print("\n===== Benchmark Complete =====")
    for idx, t in enumerate(run_times, 1):
        print(f"Run {idx}: {t:.2f} seconds")
    print(f"\nAverage execution time: {avg_time:.2f} seconds")
    print(f"\nPDF saved to: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
