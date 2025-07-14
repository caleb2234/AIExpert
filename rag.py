import torch
import torch.nn.functional as F

from torch import Tensor
from transformers import AutoTokenizer, AutoModel

import os


def last_token_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]


def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery:{query}'

task = 'Given a query, retrieve relevant medical chapter related to query'

queries = [
    get_detailed_instruct(task, 'The patient has dyspnea and respiratory distress?')
]
documents = []

current_directory = os.getcwd()

directory_in_str = current_directory + "/outputs"
directory = os.fsencode(directory_in_str)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith("3-s2.0-B9780323761741000043.pdf.txt"): 
        with open(directory_in_str + "/" + filename, 'r', encoding = "utf-8") as file:
            content = file.read()
            documents.append(content)
        continue
    else:
        continue
chunked_documents = []
document_map = [] 
for doc_idx, doc_content in enumerate(documents):
    lines = doc_content.splitlines()
    for line_idx, line in enumerate(lines):
        if line.strip(): 
            chunked_documents.append(line)
            document_map.append({'document_idx': doc_idx, 'line_idx': line_idx, 'content': line})
input_texts = queries + chunked_documents
print("Chunking successful:")
print(input_texts)
tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3-Embedding-0.6B', padding_side='left')
model = AutoModel.from_pretrained('Qwen/Qwen3-Embedding-0.6B')
print("Loaded models")

max_length = 8192

print("Tokenizing input texts...")
batch_dict = tokenizer(
    input_texts,
    padding=True,
    truncation=True,
    max_length=max_length,
    return_tensors="pt",
)
print(f"Tokenization complete. Batch dictionary keys: {batch_dict.keys()}")
print(f"Input IDs shape: {batch_dict['input_ids'].shape}")

batch_dict.to(model.device)
outputs = model(**batch_dict)
embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])


embeddings = F.normalize(embeddings, p=2, dim=1)
scores = (embeddings[:1] @ embeddings[1:].T)
print("Scores:")
print(scores.tolist())
sorted_scores, sorted_indices = torch.sort(scores, descending=True)

print(queries[0])
print("\nTop matching chunks:")
for i in range(len(sorted_indices[0])):
    chunk_index = sorted_indices[0][i].item()
    score = sorted_scores[0][i].item()
    original_doc_info = document_map[chunk_index]
    print(f"Chunk {i+1} (Score: {score:.4f})")
    print(f"Content: {original_doc_info['content']}")