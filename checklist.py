"""Criterion 1 baseline: the 10-minute keyword checklist, frozen as written in criteria.md.
Written AFTER the model was trained (disclosed in README). Rules were not tuned on any test split."""
import json, re, sys
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SEEDS = [42, 7, 2024]
SHORT_WORDS = 8  # "very short" = fewer than 8 words, fixed before scoring

# a number/year, or a named product/brand
BRANDS = r"\b(nvidia|amd|intel|apple|samsung|rtx|gtx|radeon|ryzen|geforce|threadripper|epyc|arc|m[1-4]|ps[345]|xbox|switch|iphone|pixel|galaxy|windows|linux|macos|android|ios|steam|tsmc|nand|ddr[45]|nvme|zen\d?|core i[3579]|[a-z]*gpu|[a-z]*cpu)\b"
def checklist(text):
    t = str(text)
    if re.search(r"\d", t) or re.search(BRANDS, t, re.I):
        return "analysis"
    if "?" in t or len(t.split()) < SHORT_WORDS:
        return "reaction"
    return "hot_take"

def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    def _s(f):
        c = f["label"].value_counts()
        return f["label"] if c.min() >= 2 else None
    rest, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=_s(df))
    vs = val_size / (1 - test_size)
    train, val = train_test_split(rest, test_size=vs, random_state=seed, stratify=_s(rest))
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "labels.csv"
    df = pd.read_csv(path)
    model = {r["seed"]: r for r in json.load(open("results_three_seeds_before.json"))}
    out = []
    for s in SEEDS:
        test = split_dataset(df, s)[2]
        pred = test["text"].map(checklist)
        acc = accuracy_score(test["label"], pred)
        m = model[s]
        out.append({"seed": s, "n_test": len(test), "checklist_accuracy": round(acc, 3),
                    "model_accuracy": m["accuracy"], "gap": round(m["accuracy"] - acc, 3),
                    "passes": bool(m["accuracy"] - acc >= 0.10),
                    "test_label_counts": test["label"].value_counts().to_dict(),
                    "model_n_test": m["n_test"]})
        print(out[-1])
    json.dump(out, open("checklist_results.json", "w"), indent=2)
