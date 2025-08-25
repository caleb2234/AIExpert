import pandas as pd
from collections import Counter, defaultdict

filename = "all_info_hemoglobin_patients.csv"  # Already filtered for patients with anemia labs
chunk_size = 100_000

# Symptom code mapping (all SNOMED)
symptom_codes = {
    'fatigue':       ['SNOMED/84229001'],
    'syncope':       ['SNOMED/271594007'],
    'menorrhagia':   ['SNOMED/386692008'],
    'dizziness':     ['SNOMED/404640003'],
    'bloody_stool':  ['SNOMED/405729008'],
}
anemia_code = 'LOINC/718-7'

# 1. Store each patient's minimum anemia lab
anemia_labs = {}
# 2. Store which patients have which symptom
symptom_patients = defaultdict(set)

for chunk in pd.read_csv(filename, chunksize=chunk_size):
    # Anemia labs: convert value to numeric safely
    labs = chunk[(chunk['code'] == anemia_code)].copy()
    labs['value'] = pd.to_numeric(labs['value'], errors='coerce')
    labs = labs[labs['value'].notna()]
    for row in labs.itertuples(index=False):
        pid = str(row.patient_id)
        val = float(row.value) * 10  # g/dL to g/L
        anemia_labs.setdefault(pid, []).append(val)

    # Symptom flags
    for symptom, codes in symptom_codes.items():
        mask = chunk['code'].isin(codes)
        for pid in chunk.loc[mask, 'patient_id']:
            symptom_patients[symptom].add(str(pid))

# Classify anemia severity
def classify_anemia(vals):
    v = min(vals)  # worst anemia
    if v >= 120: return 'normal'
    elif v >= 110: return 'mild'
    elif v >= 70:  return 'moderate'
    else:          return 'severe'

anemia_by_patient = {pid: classify_anemia(vals) for pid, vals in anemia_labs.items()}

# Count for each symptom and anemia severity
result = defaultdict(Counter)
for symptom, pids in symptom_patients.items():
    for pid in pids:
        if pid in anemia_by_patient:
            result[symptom][anemia_by_patient[pid]] += 1
for symptom, symptom_pids in symptom_patients.items():
    print(f"Not {symptom.capitalize()}:")
    # Patients with anemia lab but NOT this symptom
    not_symptom_pids = set(anemia_by_patient.keys()) - symptom_pids
    not_symptom_counts = Counter()
    for pid in not_symptom_pids:
        not_symptom_counts[anemia_by_patient[pid]] += 1
    for cat in ['normal', 'mild', 'moderate', 'severe']:
        print(f"  {cat}: {not_symptom_counts[cat]}")
    print()
# Print results
for symptom, counts in result.items():
    print(f"{symptom.capitalize()}:")
    for cat in ['normal', 'mild', 'moderate', 'severe']:
        print(f"  {cat}: {counts[cat]}")
    print()