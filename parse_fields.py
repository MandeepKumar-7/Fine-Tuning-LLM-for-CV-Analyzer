
import re
import json
import argparse

DEFAULT_SKILLS = [
    "Python","Java","C++","SQL","Machine Learning","Deep Learning","Data Analysis","Pandas",
    "NumPy","TensorFlow","PyTorch","NLP","Computer Vision","AWS","Docker","Kubernetes","Git",
    "Tableau","Power BI","Spark","Hadoop","JavaScript","React"
]

DEGREE_PAT = r'(B\.?Tech|B\.?E|M\.?Tech|BSc|MSc|B\.A\.|M\.A\.|MBA|Ph\.?D|BCA|MCA)'

def extract_fields(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    fields = {}

    # Name heuristic: first non-trivial line
    fields["Name"] = lines[0] if lines else None

    # Email
    m = re.search(r'[\w\.-]+@[\w\.-]+', text)
    fields["Email"] = m.group(0) if m else None

    # Phone (loose, international-friendly)
    m = re.search(r'(\+?\d[\d\-\s]{8,}\d)', text)
    fields["Phone"] = m.group(0) if m else None

    # Degrees mentioned
    degrees = re.findall(DEGREE_PAT, text, flags=re.IGNORECASE)
    fields["Education"] = sorted(set(d.title() for d in degrees))

    # Skills present
    found_skills = [s for s in DEFAULT_SKILLS if s.lower() in text.lower()]
    fields["Skills"] = sorted(set(found_skills))

    return fields

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_file", required=True, help="Path to plain text resume")
    ap.add_argument("--out", required=False, help="Path to JSON output for fields")
    args = ap.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        text = f.read()

    out = extract_fields(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
