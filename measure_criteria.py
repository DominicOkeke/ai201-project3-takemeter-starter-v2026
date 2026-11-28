"""
Unit 6, Milestone 4 — measures criteria 3, 4 and 5 (criteria.md).

    python measure_criteria.py cross          # criterion 3: train on one thread, test on the other
    python measure_criteria.py confidence     # criterion 5: per-prediction confidence, 3 seeds, pooled
    python measure_criteria.py relabel-make   # criterion 4: writes relabel_blind.csv (no labels shown)
    python measure_criteria.py relabel-score  # criterion 4: scores the filled-in relabel_blind.csv

`cross` and `confidence` train DistilBERT with the notebook's exact settings
(3 epochs, lr 2e-5, batch 16, max length 128) and the notebook's split_dataset.
They never touch results_three_seeds_before.json.
"""
import json, re, sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score
from sklearn.model_selection import train_test_split

LABELS = ["analysis", "hot_take", "reaction"]
SEEDS = [42, 7, 2024]
BASE_MODEL, EPOCHS, LR, BATCH, MAX_LENGTH = "distilbert-base-uncased", 3, 2e-5, 16, 128


def norm(t):
    return re.sub(r"\s+", " ", str(t)).strip()


def load_labels():
    df = pd.read_csv("labels.csv")
    tm = pd.read_csv("thread_map.csv")
    lookup = {norm(t): th for t, th in zip(tm["text"], tm["thread"])}
    df["thread"] = df["text"].map(lambda t: lookup[norm(t)])
    return df


def split_dataset(df, seed, test_size=0.15, val_size=0.15):  # identical to the notebook
    def _s(f):
        c = f["label"].value_counts()
        return f["label"] if c.min() >= 2 else None
    rest, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=_s(df))
    vs = val_size / (1 - test_size)
    train, val = train_test_split(rest, test_size=vs, random_state=seed, stratify=_s(rest))
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)


def train_and_predict(train_df, val_df, test_df, seed):
    """Same training recipe as the notebook. Returns (gold ids, softmax probs)."""
    from datasets import Dataset
    from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                              TrainingArguments, Trainer, set_seed)
    set_seed(seed)
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL, num_labels=3,
        id2label=dict(enumerate(LABELS)), label2id={l: i for i, l in enumerate(LABELS)})
    lk = {l: i for i, l in enumerate(LABELS)}

    def ds(f):
        d = pd.DataFrame({"text": f["text"], "labels": f["label"].str.strip().map(lk)})
        return Dataset.from_pandas(d).map(
            lambda b: tok(b["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH),
            batched=True)

    args = TrainingArguments(output_dir="./takemeter_out_c345", num_train_epochs=EPOCHS,
                             learning_rate=LR, per_device_train_batch_size=BATCH,
                             per_device_eval_batch_size=BATCH, eval_strategy="epoch",
                             save_strategy="no", logging_steps=10, seed=seed,
                             report_to="none", disable_tqdm=True)
    trainer = Trainer(model=model, args=args, train_dataset=ds(train_df), eval_dataset=ds(val_df))
    trainer.train()
    out = trainer.predict(ds(test_df))
    s = out.predictions
    e = np.exp(s - s.max(axis=-1, keepdims=True))
    return np.array(out.label_ids), e / e.sum(axis=-1, keepdims=True)


def cmd_cross():
    df = load_labels()
    before = {r["seed"]: r["accuracy"] for r in json.load(open("results_three_seeds_before.json"))}
    normal = float(np.mean(list(before.values())))
    rows = []
    for seed in SEEDS:
        for train_t, test_t in (("r/hardware", "r/AskReddit"), ("r/AskReddit", "r/hardware")):
            tr, te = df[df.thread == train_t], df[df.thread == test_t].reset_index(drop=True)
            tr_df, val_df = train_test_split(tr, test_size=0.15, random_state=seed, stratify=tr["label"])
            gold, probs = train_and_predict(tr_df.reset_index(drop=True), val_df.reset_index(drop=True), te, seed)
            acc = float(accuracy_score(gold, probs.argmax(1)))
            rows.append({"seed": seed, "train": train_t, "test": test_t, "n_test": len(te),
                         "accuracy": round(acc, 3),
                         "majority_rate_test": round(float(te["label"].value_counts(normalize=True).max()), 3),
                         "predicted_counts": {LABELS[i]: int((probs.argmax(1) == i).sum()) for i in range(3)}})
            print(rows[-1], flush=True)
    for r in rows:
        r["meets_floor_0.60"] = r["accuracy"] >= 0.60
        r["within_0.10_of_normal"] = r["accuracy"] >= round(before[r["seed"]], 3) - 0.10
    json.dump({"normal_accuracy_by_seed": before, "rows": rows,
               "all_pass": all(r["meets_floor_0.60"] and r["within_0.10_of_normal"] for r in rows)},
              open("cross_thread_results.json", "w"), indent=2)
    print("\nWrote cross_thread_results.json. all_pass =",
          all(r["meets_floor_0.60"] and r["within_0.10_of_normal"] for r in rows))


def cmd_confidence():
    df = load_labels()
    before = {r["seed"]: r for r in json.load(open("results_three_seeds_before.json"))}
    preds, per_seed = [], []
    for seed in SEEDS:
        _, _, test = split_dataset(df, seed)
        gold, probs = train_and_predict(*split_dataset(df, seed), seed)
        acc = float(accuracy_score(gold, probs.argmax(1)))
        per_seed.append({"seed": seed, "accuracy_now": round(acc, 3),
                         "accuracy_saved_run": round(before[seed]["accuracy"], 3)})
        print(per_seed[-1], flush=True)
        for g, p, t in zip(gold, probs, test["text"]):
            preds.append({"seed": seed, "text": t, "gold": LABELS[g], "pred": LABELS[int(p.argmax())],
                          "confidence": float(p.max())})
    p = pd.DataFrame(preds)
    right = p.gold == p.pred
    hi = p.confidence >= 0.80
    unsure = p.confidence < 0.50
    res = {"n_pooled": len(p), "n_high_conf": int(hi.sum()), "coverage_high_conf": round(float(hi.mean()), 3),
           "accuracy_high_conf": round(float(right[hi].mean()), 3) if hi.any() else None,
           "share_uncertain_below_0.50": round(float(unsure.mean()), 3),
           "mean_confidence": round(float(p.confidence.mean()), 3),
           "max_confidence": round(float(p.confidence.max()), 3),
           "per_seed_check_vs_saved_run": per_seed,
           "passes": bool(hi.any() and right[hi].mean() >= 0.85 and hi.mean() >= 0.25)}
    json.dump({"summary": res, "predictions": preds}, open("confidence_predictions_before.json", "w"), indent=2)
    print(json.dumps(res, indent=2))


def cmd_relabel_make():
    df = pd.read_csv("labels.csv")
    s = df.sample(n=40, random_state=2026)
    s[["text"]].assign(label="").to_csv("relabel_blind.csv", index=False)
    print("Wrote relabel_blind.csv (40 comments, no labels, no notes). Fill the `label` column "
          "WITHOUT opening labels.csv, using only your written decision rule.")


def cmd_relabel_score():
    old = pd.read_csv("labels.csv")
    new = pd.read_csv("relabel_blind.csv")
    new["label"] = new["label"].astype(str).str.strip()
    if (~new["label"].isin(LABELS)).any():
        sys.exit("relabel_blind.csv still has empty or misspelt labels.")
    om = {norm(t): l for t, l in zip(old["text"], old["label"])}
    new["old"] = new["text"].map(lambda t: om[norm(t)])
    agree = int((new.old == new.label).sum())
    kappa = float(cohen_kappa_score(new.old, new.label, labels=LABELS))
    dis = new[new.old != new.label][["text", "old", "label"]].rename(columns={"label": "new"})
    res = {"n": len(new), "agreed": agree, "agreement": round(agree / len(new), 3),
           "kappa": round(kappa, 3), "passes": bool(agree >= 34 and kappa >= 0.70),
           "disagreements": dis.to_dict("records")}
    json.dump(res, open("self_agreement_results.json", "w"), indent=2)
    print({k: v for k, v in res.items() if k != "disagreements"})
    for r in res["disagreements"]:
        print(f"  old={r['old']:9} new={r['new']:9} {norm(r['text'])[:80]}")


if __name__ == "__main__":
    cmds = {"cross": cmd_cross, "confidence": cmd_confidence,
            "relabel-make": cmd_relabel_make, "relabel-score": cmd_relabel_score}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]]()
