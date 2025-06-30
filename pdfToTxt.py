import pymupdf
import os

current_directory = os.getcwd()

directory_in_str = current_directory + "/medbook"
directory = os.fsencode(directory_in_str)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".pdf"): 
        doc = pymupdf.open(directory_in_str + f"/{filename}")
        out = open(current_directory + f"/outputs/{filename}.txt", "wb")
        for page in doc: 
            text = page.get_text().encode("utf8")
            out.write(text)
            out.write(bytes((12,)))
        out.close()
        continue
    else:
        continue