
import json
import argparse
from parse_fields import extract_fields

TEMPLATE_QA = [
    ("What is the candidate's highest qualification?", lambda f: (", ".join(f.get("Education") or []) or "Not specified")),
    ("Which programming languages does the candidate mention?", lambda f: ", ".join(f.get("Skills") or []) or "Not specified"),
    ("What is the candidate's email address?", lambda f: f.get("Email") or "Not specified"),
    ("What is the candidate's phone number?", lambda f: f.get("Phone") or "Not specified"),
    ("Summarize the candidate's top skills.", lambda f: ", ".join((f.get("Skills") or [])[:5]) or "Not specified")
]

def generate_qna(text: str):
    fields = extract_fields(text)
    for q, ans_fn in TEMPLATE_QA:
        a = ans_fn(fields)
        yield {"question": q, "answer": a}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_file", required=True, help="Path to plain text resume")
    ap.add_argument("--out", required=True, help="Path to output JSONL (questions/answers)")
    args = ap.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        text = f.read()

    with open(args.out, "w", encoding="utf-8") as out:
        for item in generate_qna(text):
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
