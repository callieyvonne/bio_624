import json
import glob
import pandas as pd
import os

# Directory containing your fastp JSON files
qc_dir = r"C:\Users\calli\OneDrive - North Carolina State University\Documents\bio_624_project\qc_json_results"

# Directory where you want the summary CSV to be written
output_dir = r"C:\Users\calli\OneDrive - North Carolina State University\Documents\bio_624_project"

records = []

for json_file in glob.glob(os.path.join(qc_dir, "*_fastp.json")):
    sample = os.path.basename(json_file).replace("_fastp.json", "")
    
    with open(json_file) as f:
        data = json.load(f)
    
    before = data["summary"]["before_filtering"]
    after = data["summary"]["after_filtering"]
    dup = data.get("duplication", {})
    adapter = data.get("adapter_cutting", {})
    
    records.append({
        "sample": sample,
        "raw_reads": before["total_reads"],
        "filtered_reads": after["total_reads"],
        "reads_retained_pct": round(after["total_reads"] / before["total_reads"] * 100, 2),
        "raw_bases": before["total_bases"],
        "filtered_bases": after["total_bases"],
        "duplication_rate": dup.get("rate", None),
        "adapter_trimmed_reads": adapter.get("adapter_trimmed_reads", None)
    })

df = pd.DataFrame(records)

# Write the summary CSV to your project directory
output_path = os.path.join(output_dir, "fastp_qc_summary.csv")
df.to_csv(output_path, index=False)

print(f"Wrote fastp_qc_summary.csv to: {output_path}")

