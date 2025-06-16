from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import torch
import data
from google import genai
from google.genai import types

model_id = "google/medgemma-4b-it"

model = AutoModelForImageTextToText.from_pretrained(
    model_id,
    torch_dtype = torch.bfloat16,
    device_map = "auto"
)

reasoning_agent = AutoProcessor.from_pretrained(model_id, use_fast = True)

messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text" : """
        You are an experienced general practitioner tasked to guide a student.
Use all available information to generate a report on the current state of the case and on the student's progress in the case.
You must find the correct diagnosis, create recommendations, provide student's strengths and weaknesses based on previous performance and what
the student has asked so far, the student's progress in the case, and important information the student has not yet asked the patient yet.
=== Response format ===
ONLY answer by filling in the following JSON schema:
        """ + data.reasoning_json_schema}]
    },
    {"role": "user", "content": [{"type":"text", "text":f"""

=== Expert Conversation History ===
{data.expert_conversation_history}

=== Student Historical Performance ===
{data.student_record_performance}

=== Patient Conversation History ===
{data.patient_conversation_history}

=== Patient Information ===
{data.patient_info}

=== Your Task ===
Based on all the above sections generate a report on what the student doesn't know based on what the student has previously asked,
the student's weaknesses based on historical performance, the correct procedure, and the correct diagnosis.
"""}]},
]
inputs = reasoning_agent.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_dict = True, return_tensors = 'pt').to(model.device, dtype=torch.bfloat16)
input_len = inputs["input_ids"].shape[-1]
with torch.inference_mode():
    generation = model.generate(**inputs, max_new_tokens=1000, do_sample=False)
    generation = generation[0][input_len:]
decoded = reasoning_agent.decode(generation, skip_special_tokens=True)
print(decoded)
client = genai.Client(api_key="AIzaSyCIqhlxRg9n578xvFXVmKdrRWKHmCOD8fk")
response = client.models.generate_content(
    model="learnlm-2.0-flash-experimental", 
    config = types.GenerateContentConfig(system_instruction="""You are an experienced general practitioner whose main goal is to help the student learn and develop
        an intuition on how to diagnose patients. You will only be speaking to the student, who is currently talking with a patient in an OSCE examination setting. 
        Guide the student through the following clinical reasoning steps:
        - (1) Interpretive summary
        - (2) Differential diagnosis
        - (3) Explanation of lead diagnosis
        - (4) Explanation of alternative diagnoses
        - (5) Reflection on potential diagnostic errors and bias
        - (6) Evaluation and management plan
        and make sure you do not repeat any of the steps given past dialogue with the student.
        Past dialogue with expert: """ + data.expert_conversation_history + """
        
        You must also:
        - Be a friendly, supportive tutor 
        - Ask guiding questions to help your students take incremental steps toward the correct diagnosis and procedure
        - Don't reveal the correct diagnosis
        - Identify and address misconceptions
        - Adapt to the student's level
        Use the following context of the current case, the student's weaknesses,
        what the student doesn't know and hasn't asked yet, and the correct procedure to respond to the student:""" + decoded),
    contents= data.student_input
)
print(response.text)
