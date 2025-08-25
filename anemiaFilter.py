import pandas as pd
filename = "ehrshot.csv"
patients_with_hemo = set()
chunk_size = 25000
# for chunk in pd.read_csv(filename, chunksize = chunk_size):
#     matches = chunk[
#         (chunk['code'] == 'LOINC/718-7') &
#         (chunk['value'].notna()) &
#         (chunk['value'] != '')
#     ]
#     patients_with_hemo.update(matches['patient_id'].unique())
# print(len(patients_with_hemo))
# with open("hemoglobin_patients.txt", "w") as f:
#     for pid in patients_with_hemo:
#         f.write(str(pid) + "\n")
patient_ids = set(pd.read_csv("hemoglobin_patients.txt", header=None)[0].astype(str))
header = pd.read_csv(filename, nrows=0)
header.to_csv("all_info_hemoglobin_patients.csv", index=False)
print("Loaded", len(patient_ids), "patient IDs")
print("Sample:", list(patient_ids)[:5])
# Now write matching rows in chunks
for i, chunk in enumerate(pd.read_csv(filename, chunksize=chunk_size)):
    chunk['patient_id_str'] = chunk['patient_id'].astype(str)
    matches = chunk[chunk['patient_id_str'].isin(patient_ids)]
    print(f"Chunk {i}: {len(matches)} matches")
    if not matches.empty:
        matches.drop(columns=['patient_id_str']).to_csv(
            "all_info_hemoglobin_patients.csv", mode='a', header=False, index=False)
    del chunk
    del matches  # help garbage collector