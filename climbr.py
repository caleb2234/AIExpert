import femr.models.transformer
import torch
import femr.models.tokenizer
import femr.models.processor
import datetime

model_name = "StanfordShahLab/clmbr-t-base"

# Load tokenizer / batch loader
tokenizer = femr.models.tokenizer.FEMRTokenizer.from_pretrained(model_name)
batch_processor = femr.models.processor.FEMRBatchProcessor(tokenizer)

# Load model
model = femr.models.transformer.FEMRModel.from_pretrained(model_name)

# Create an example patient to run inference on
# This patient follows the MEDS schema: https://github.com/Medical-Event-Data-Standard
example_patient = {
    'patient_id': 30,
    'events': [{
        'time': datetime.datetime(2011, 5, 8),
        'measurements': [
            {'code': 'SNOMED/184099003'},
            {'code': 'Visit/IP'},
        ],
    },
    {
        'time': datetime.datetime(2012, 6, 9),
        'measurements': [
            {'code': 'Visit/OP'},
            {'code': 'SNOMED/3950001'}
        ],
    }]
}

raw_batch = batch_processor.convert_patient(example_patient, tensor_type="pt")
batch = batch_processor.collate([raw_batch])

# Run model
with torch.no_grad():
    _, result = model(**batch)
    print(result['timestamps'].cpu().numpy().astype('datetime64[s]'))
    print(result['patient_ids'])
    print(result['representations'])