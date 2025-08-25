from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

ner = pipeline("token-classification",
               model="Charangan/MedBERT",
               tokenizer="Charangan/MedBERT",
               aggregation_strategy="simple")

text = open("melissa_bishop_note.txt","r",encoding="utf-8").read()
entities = ner(text)

# crude ranking of likely diagnoses by entity frequency
from collections import Counter
diseases = [e["word"] for e in entities if "DISEASE" in e["entity_group"].upper()]
print(Counter(diseases).most_common(10))