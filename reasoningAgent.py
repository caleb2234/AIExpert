from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import torch
import data

model_id = "google/medgemma-4b-it"

model = AutoModelForImageTextToText.from_pretrained(
    model_id,
    torch_dtype = torch.float16,
    device_map = "auto"
)

reasoning_agent = AutoProcessor.from_pretrained(model_id, use_fast = True)

messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text" : """
        You are an experienced general practitioner tasked to guide a student.
Use all available information to fill out a JSON on the current state of the case and on the student's progress in the case. You must pinpoint
three things:
(1) Which node the student currently is on in the flow chart given their input
(2) Which node the student currently is on in the flow chart based on the patient conversation history
(3) List all the skipped nodes that start with Q on the flow chart from ONLY the direct path from patientConversationHistoryNode to the studentInputNode.
Reply in the following JSON format:
studentProgress = {
"studentInputNode" : str # This is for the node given the input
"patientConversationHistoryNode" : str # This is for the node given the patient conversation history
"skippedNodes": list[str] # This is for the skipped nodes
                     }
=== Flowchart ===
Refer to the following flowchart:
        """ + data.flowchart}]
    },
    {"role": "user", "content": [{"type":"text", "text":f"""
                                  
=== Student Input ===
{data.student_input2}

=== Patient Conversation History ===
{data.patient_conversation_history2}

"""}]},
]
inputs = reasoning_agent.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_dict = True, return_tensors = 'pt').to(model.device, dtype=torch.float16)
input_len = inputs["input_ids"].shape[-1]
with torch.inference_mode():
    generation = model.generate(**inputs, max_new_tokens=1000, do_sample=False)
    generation = generation[0][input_len:]
decoded = reasoning_agent.decode(generation, skip_special_tokens=True)
print(decoded)