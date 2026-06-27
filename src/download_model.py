from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

LOCAL_MODEL_PATH = r"C:/Users/geetasai/Downloads/bart-large-cnn"

tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL_PATH)

print("Loaded model locally!")
