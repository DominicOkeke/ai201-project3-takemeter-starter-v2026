# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This project builds TakeMeter, a text classifier trained to categorize discussions from the hardware community on Reddit (r/hardware). It sorts community posts and comments into distinct structural types—specifically distinguishing between factual technical analysis, unsupported hot_take claims, and quick reaction remarks. By automating this sorting process, the classifier helps filter through community noise to surface substantive architectural debates and hardware insights.

## Data Source
- **Source Thread:** [Is the future of hardware just optimization? on r/hardware](https://www.reddit.com/r/hardware/comments/1pwxwx7/is_the_future_of_hardware_just_optimization/ and https://www.reddit.com/r/AskReddit/comments/1hi1r3p/what_is_computer_hardware_likely_to_be_like_in/)
---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `label_one`: Analysis

**Definition:**
 Makes an argument backed by a specific, checkable fact (such as an IRDS roadmap, transistor gate metrics, or manufacturing process nodes)

**Example 1:**
>"You can look up IRDS's most recent More Moore roadmap if you're curious. There are significant improvements in compute and efficiency yet to come from CMOS..."

**Example 2:**
>"As the industry moves to GAA-FETs, backside power delivery, and High NA-EUV, the low hanging fruit will be picked..."

### `label_two`: hot_take

**Definition:**
A confident, broad claim or sweeping prediction with no technical support or architectural data offered.

**Example 1:**
>"In 10 years we will be right here. 10 years ago was 2015. Internet is the same, phones are the same, PCs and servers are the same."

**Example 2:**
>"The future of hardware just optimization? ... Barring the switch to quantum or light based computers I think most improvements to the computer world are going to come from optimisations."


### `label_three`: Reactions

**Definition:** An immediate emotional response, personal anecdote, or brief conversational reply rather than a structured technical argument.

**Example 1:** 
> "Very interesting 🤔".

**Example 2:** 
> "Yeah. In 2005 if you had 4GB of RAM you were cool."

---

### The hardest boundary

**Which two labels:**
Analysis vs. Hot_take

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

 If a post makes a predictive claim about future hardware limits or slowdowns but accompanies it with specific engineering terms, architectural paradigms (e.g., GAA-FETs, CNTFETs), or explicit roadmap references, it is **`analysis`**. If it states the same prediction purely as an opinion or personal belief without referencing underlying physical or industrial data points, it is a **`hot_take`**.

 If the post names a specific checkable architectural metric or hardware specification (such as core counts, VRAM capacity, or bus widths), it is **`analysis`**, even if the tone is cynical or heated.

---

## Borderline Case Analysis
The Two Labels Involved: analysis and hot_take

## The Borderline Post Example:

"Nvidia could have sold us a 5080 that had 50% more cores, 50% more VRAM at the same price, and made a healthy margin besides.. they didn't, bc they don't have to."

Why it's ambiguous: It reads like an opinionated, cynical rant about corporate greed (which leans toward a hot_take), but it relies on specific, quantifiable hardware metrics and product specifications (50% more cores, 50% more VRAM) to drive its point home.

## Your Decision Rule
If the post names a specific checkable architectural metric or hardware specification (such as core counts, VRAM capacity, or bus widths), it is analysis, even if the tone is cynical or heated.

## How I Updated the Decision Rule

**Stress Test:** Analysis vs. Hot_take

I selected eight real comments from the r/hardware thread ("Is the future of hardware just optimization?") that sit near the analysis/hot_take boundary and labeled each one under my original rule, then under a tightened rule.

### The eight boundary comments

| # | Commenter | Excerpt | Original rule | Problem found | Final label |
|---|---|---|---|---|---|
| 1 | greggm2000 | "Nvidia could have sold us a 5080 that had 50% more cores, 50% more VRAM..." | analysis | Figures are counterfactual. Right label, wrong reason. | analysis (thin) |
| 2 | reddit_equals_censor | 3060 vs. 4060 die sizes, bus widths, prices | analysis | None. Heated tone doesn't matter. | analysis |
| 3 | dudemanguy301 | "tail end of the useful lifespan of regular EUV, front side power delivery, and Fin-FETs" | analysis | Excerpt alone is jargon plus a prediction. | analysis |
| 4 | lord_lableigh | "You can lookup the IEEE conference on chip roadmap..." | analysis | None, but thin. | analysis (thin) |
| 5 | Federal_Patience2422 | "Tsmc itself states that it's keeping track with moores law" | hot_take | Appeal to a source with no locatable document. | hot_take |
| 6 | [deleted] | "25% improvement in 20 years... flat from N4 to N3" | ambiguous | Specific but unsourced figures; no ruling existed. | analysis (thin) |
| 7 | noiserr | "ARM is efficient at light workloads... x86 is more efficient at heavy workloads" | conflict | Engineering-paradigm trigger said analysis, no-data trigger said hot_take. | hot_take |
| 8 | Fr0stCy | "SRAM doesn't shrink nearly as much as logic... Apple's unified memory and AMD's X3D cache" | analysis | None. | analysis |

Four of eight (#1, 5, 6, 7) did not classify cleanly under the original rule.

### What the test exposed

1. **Unit of labeling was undefined** (#1, 3). Comments mix claims, so the label must come from the whole comment's main claim.
2. **The two analysis triggers disagreed** (#3, 7). Engineering terms and checkable metrics gave different answers, and terms alone are cheap.
3. **Source attribution was inconsistent** (#4 vs. 5). "Look up the IEEE roadmap" counted, but "TSMC states..." did not, and the rule couldn't say why.
4. **Unsourced numbers had no ruling** (#6).
5. **hot_take required a "sweeping prediction"** (#7). A confident technical claim with no data and no prediction fit neither label.
6. **The borderline example was anchored on the wrong sentence** (#1). The 5080 line is a hypothetical.

### Updated decision rule

**Label the whole comment by its main claim.** Tone, hedging, whether the claim is true, and whether the conclusion overreaches never change the label.

- **`analysis`:** The main claim rests on at least one checkable specific that bears on the conclusion: a locatable document or roadmap (IMEC, IRDS, IEEE), a number or date, a named product or component spec, or a documented fact about how a named technology scales or changes.
- **`hot_take`:** A confident claim, predictive or not, whose support is absent, generic, hypothetical, or attributed to a source no one could locate.

**Does not count as support:**
- Jargon lists with no claim attached (GAA-FET, CNTFET)
- General mechanisms ("quantum effects get weird")
- Numbers inside hypotheticals or counterfactuals
- Unlocatable attributions ("TSMC says...")

**Thin analysis is still analysis.**

### Revised borderline example

> "Nvidia could have sold us a 5080 that had 50% more cores, 50% more VRAM at the same price, and made a healthy margin besides.. they didn't, bc they don't have to."

The 5080 sentence alone is a counterfactual and would be `hot_take`. The full comment is `analysis` because it also makes checkable GPU-generation comparisons (1080 Ti → 3080 → 4090, 9800X3D vs. 1600X). The label comes from those claims, not from the core and VRAM figures.

### Remaining judgment call

#4 (counts) vs. #5 (doesn't): a locatable roadmap series counts, but a named entity "stating" something does not. If this is ever relaxed so "named entity states X" counts as analysis, flip #5 and apply it everywhere.

### Taxonomy fixes carried forward

- **Analysis Example 2:** use the full dudemanguy301 comment, since the excerpt alone fails the new rule.
- **Hot_take Example 2:** the "Barring the switch to quantum..." quote is from the original post, not a comment. Decide whether the OP post is in the 200+ items.

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**
- **Source Thread:** [Is the future of hardware just optimization? on r/hardware](https://www.reddit.com/r/hardware/comments/1pwxwx7/is_the_future_of_hardware_just_optimization/ and https://www.reddit.com/r/AskReddit/comments/1hi1r3p/what_is_computer_hardware_likely_to_be_like_in/)
---
**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
| **Total** |  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
>The post: greggm2000: "From the 1080 Ti to the 3080 to the 4090, we see a doubling in performance each time... Nvidia could have sold us a 5080 that had 50% more cores, 50% more VRAM at the same price... they didn't, bc they don't have to."

> *Could have been:*
>analysis or hot_take

> *I chose, because:*
>I chose: analysis, because the 5080 line is a counterfactual and would be a hot_take on its own, but the same comment also makes checkable GPU-generation comparisons (1080 Ti → 3080 → 4090, 9800X3D vs 1600X). I label the whole comment by its main claim, and those comparisons carry it.


**2.**
> *The post:*
>The post: Federal_Patience2422: "No it's not? Tsmc itself states that it's keeping track with moores law." Compared with rimantass: "But the tsmc road map clearly shows it slowing down."

> *Could have been:*
>analysis or hot_take (both comments)

> *I chose, because:*
>I chose: hot_take for "Tsmc itself states..." and analysis (thin) for "the tsmc road map clearly shows...", because the first points at no document anyone could locate, while the second names a specific roadmap. It's the closest call in the file, and it's also the pair most likely to be labeled inconsistently.

**3.**
> *The post:*
>The post: Strazdas1: "Moores law has been dead for at least a decade and even then it lasted a lot longer than anyone expected it to. Moore himself said it will stop being applicable in 1986."

> *Could have been:*
>analysis or hot_take

> *I chose, because:*
>I chose: hot_take, because the checkable fact (Moore and 1986) supports a side point about how long it lasted. Take it out and the main claim ("dead for at least a decade") stands exactly as strongly, so the specific doesn't carry the conclusion.

**4.**
> *The post:*
The post: theQuandary: "https://en.wikipedia.org/wiki/Amdahl's_law"

> *Could have been:*
> analysis or reaction

> *I chose, because:*
>I chose: analysis (thin), because it points at a named, locatable law and bears on the comment it replies to, the same way "look up the IEEE roadmap" does. But it states no claim of its own, so a reasonable labeler could call it a reaction.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**
>distilbert-base-uncased (default starter model)

**Settings:** <!-- epochs, learning rate, batch size, seed -->
>Epochs: 3, Learning rate: 2e-5, Batch size: 16, Seed: 42.

**Anything I changed from the defaults, and why:**
>None. Kept all training hyperparameters at their default values to establish a clean, standard baseline.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
>Train / Val / Test split counts: 200 / 44 / 44 (based on a standard 70/15/15 split of 288 total examples).

>Per-label counts in the test split (approximate distribution based on your dataset balance):

- analysis: ~18

- hot_take: ~16

- reaction: ~10 (Note: If any label falls near or below 8 examples in the test split, it can cause its individual F1 metric to jump around in the next unit).

*Device Used for the Test*
device: cpu  (CPU)
torch:  2.14.1+cpu

⚠️  WRITE THIS DOWN. Your results depend on it.

Two people running this notebook on the same data with the same seed can
get different numbers, because different hardware does the arithmetic in
a slightly different order. That is not a bug and it is not one of you
being wrong — it is a real property of the thing you are building, and
unit 6 asks you to report it alongside your three seeds.

**Results**:

[39/39 01:31, Epoch 3/3]
Epoch	Training Loss	Validation Loss	Accuracy	F1 Macro
1	1.062800	1.007794	0.454545	0.208333
2	1.015000	0.965759	0.454545	0.208333
3	0.909900	0.947674	0.454545	0.208333

Map: 100%|██████████| 44/44 [00:00<00:00, 3704.40 examples/s]
c:\Users\dokek\Downloads\ai201-project3-takemeter-starter-v2026-main\.venv-1\Lib\site-packages\torch\utils\data\dataloader.py:759: UserWarning: 'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used.
  super().__init__(loader)
accuracy  0.500
macro F1  0.318

  analysis         F1 0.167   (n=11)
  hot_take         F1 0.645   (n=20)
  reaction         F1 0.143   (n=13)

confidence   most-sure third 0.714   ·   least-sure third 0.429

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* 
>I asked an AI tool to review my label definitions for `analysis` and `hot_take` alongside a tricky borderline post from r/hardware to help generate a hard-boundary decision rule.
- *What came back:* 
>The model provided a structured breakdown of why the post could fit either category due to its cynical tone masking underlying hardware specifications.
- *What I changed:* 
>I refined its suggestion into a definitive, checkable rule: "If the post names a specific checkable architectural metric or hardware specification (such as core counts or VRAM capacity), it is analysis, even if the tone is cynical."

**Moment 2**

- *What I asked for:*
>Eight comments from the thread that sit on the analysis/hot_take boundary, to stress-test my labels.
- *What came back:*
>Eight invented posts written in the style of the thread, with labels.
- *What I changed:*
>I rejected them and required real comments. The second attempt found that my rule’s two triggers disagreed (engineering terms vs checkable metrics). I tightened it to label the whole comment by its main claim, and I moved my borderline example’s reasoning off the 5080 counterfactual sentence.

**Pre-labelling disclosure:**

Claude AI was used to label 271 rows from my decision rule and I reviewed them. 

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

Before I look at your trained model:

> The trained model will outperform the baseline on nuanced 'analysis' posts because fine-tuning helps capture subtle technical citations and architectural metrics that zero-shot general prompts misinterpret

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->


Device set to use cpu
accuracy  0.341               
macro F1  0.325

  analysis         F1 0.391   (n=11)
  hot_take         F1 0.250   (n=20)
  reaction         F1 0.333   (n=13)


| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |


| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.341 | 0.500 | +0.159 |
| Macro F1 | 0.325 | 0.318 | -0.007 |
| F1 — `analysis` | 0.391 | 0.167 | -0.225 |
| F1 — `hot_take` | 0.250 | 0.645 | +0.395 |
| F1 — `reaction` | 0.333 | 0.143 | -0.190 |






**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Accuracy vs. checklist (+0.10 all 3 seeds) | ≥ +0.10 over checklist (all 3 seeds) | acc 0.500 vs. checklist 0.477 (+0.023) | acc 0.455 vs. checklist 0.545 (−0.091) | acc 0.477 vs. checklist 0.386 (+0.091) | MISSED |
| 2. `analysis` precision & recall (all 3 seeds) | P ≥ 0.75 and R ≥ 0.60 (all 3 seeds) | P 1.000 (1 prediction) / R 0.091 | P 0.000 (never predicted) / R 0.000 | P 0.000 (never predicted) / R 0.000 | MISSED |
| 3. Cross-thread accuracy (`r/hardware` ↔ `r/AskReddit`) | ≥ 0.60 & within 0.10 of held-out | H→A 0.255, A→H 0.309 | H→A 0.170, A→H 0.309 | H→A 0.364, A→H 0.309 | MISSED |
| 4. Self-agreement & Cohen's κ | ≥ 0.85 (34/40), κ ≥ 0.70 | 25/40 = 0.625, κ 0.421 | (one relabel, not per seed) | (one relabel, not per seed) | MISSED |
| 5. High-conf. (≥ 0.80) acc & coverage (pooled) | Acc ≥ 0.85, cov ≥ 0.25 (pooled) | 0 of 132 pooled predictions ≥ 0.80 (coverage 0.000, accuracy undefined) | (pooled across seeds) | (pooled across seeds) | MISSED |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **analysis** | 1 | 10 | 0 |
| **hot_take** | 0 | 20 | 0 |
| **reaction** | 0 | 12 | 1 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

>The model misclassified 12 true `reaction` posts as `hot_take` while calling 0 true `hot_take` posts `reaction` (and also sent 10 true `analysis` posts to `hot_take` with 0 in reverse), showing a lopsided bias toward predicting `hot_take` across boundaries.


*Section 6 three-seed run summary (device: `cpu` / `CPU`, `torch` `2.14.1+cpu`):*
- **Overall accuracy:** `0.500` (Seed 42), `0.455` (Seed 7), `0.477` (Seed 2024) — spread `0.045` (within ~10-point stability window).
- **Macro F1:** `0.318` (Seed 42), `0.208` (Seed 7), `0.291` (Seed 2024) — spread `0.110`.
- **Per-label F1:** `analysis` (`0.167`, `0.000`, `0.000`), `hot_take` (`0.645`, `0.625`, `0.623`), `reaction` (`0.143`, `0.000`, `0.250`).

### Criterion 1 — the keyword checklist

The checklist from `criteria.md`, in `checklist.py` (results in `checklist_results.json`). It rebuilds each seed's test split with the notebook's `split_dataset` (stratified 70/15/15, seeds 42 / 7 / 2024; 44 test comments each: 11 `analysis`, 20 `hot_take`, 13 `reaction`) and scores the rules on it:

1. If the comment contains a digit (number or year) or a named product/brand, predict `analysis`.
2. Otherwise, if it contains a `?` or has fewer than 8 words, predict `reaction`.
3. Otherwise, predict `hot_take`.

| Seed | Checklist accuracy | TakeMeter accuracy | Gap (needs ≥ +0.10) | Met? |
|---|---|---|---|---|
| 42 | 0.477 | 0.500 | +0.023 | No |
| 7 | 0.545 | 0.455 | −0.091 | No |
| 2024 | 0.386 | 0.477 | +0.091 | No |

**Disclosure:** I wrote the checklist after training, not before as `criteria.md` planned. I took the rules straight from the criterion and fixed them once, including the 8-word "very short" cutoff and the brand list, before scoring. I did not tune them against any test split and ran no threshold sensitivity check. The test counts per label match the confusion-matrix row totals from the training run, which confirms the splits are the same ones the model was scored on.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Accuracy beats the keyword checklist by ≥ 0.10 (all 3 seeds) | ≥ +0.10 over checklist on all 3 seeds | MISSED | The gaps were +0.023 / −0.091 / +0.091, so no seed reached +0.10, and on seed 7 the checklist beat the model outright. Closest was seed 2024, 0.009 short. The model's accuracy is just the `hot_take` majority rate (it predicts `hot_take` for almost everything), while the checklist's accuracy swings with each split. The checklist was written after training (see below). |
| 2 | `analysis` precision and recall (all 3 seeds) | P ≥ 0.75 and R ≥ 0.60 on all 3 seeds | MISSED | Recall was 0.091 / 0.000 / 0.000 against 0.60, so the target fails on every seed whatever the precision was. Precision was 1.000 on seed 42 but from a single `analysis` prediction, and 0.000 on seeds 7 and 2024 because the model never predicted `analysis` (all 11 real `analysis` posts in each test split were called `hot_take` or, on seed 42, 1 was caught and 10 went to `hot_take`). |
| 3 | Cross-thread accuracy (`r/hardware` ↔ `r/AskReddit`) | ≥ 0.60 in both directions and within 0.10 of normal held-out accuracy | MISSED | All six runs (3 seeds × 2 directions) fell below the 0.60 floor: hardware→AskReddit 0.255 / 0.170 / 0.364, AskReddit→hardware 0.309 / 0.309 / 0.309. They also fell more than 0.10 below normal accuracy (0.500 / 0.455 / 0.477). On AskReddit the model scored below the 0.552 you get by always guessing `hot_take`. |
| 4 | Self-agreement and Cohen's κ | ≥ 34 of 40 (0.85) and κ ≥ 0.70 | MISSED | On the 40-comment blind relabel I gave the same label on 25 of 40 (0.625) with κ = 0.421, against 34 and 0.70 needed. The relabel was done about a day or two after the original labels, not the 3+ days the criterion asks for, so the gap would likely be at least as large with more time. |
| 5 | High-confidence accuracy and coverage (pooled across 3 seeds) | ≥ 80% sure → right ≥ 85% of the time, and that sure on ≥ 25% of comments | MISSED | Of 132 pooled test predictions, none reached 0.80 confidence (the maximum was 0.612, the mean 0.477), so coverage was 0.000 against 0.25 and there was no high-confidence accuracy to score. 63.6% of predictions fell below 0.50 and would have shown "uncertain". |

**The opposite verdict, argued (criterion 1, seed 2024).** The case for MET: on seed 2024 the model got 21 of 44 right and the checklist 17 of 44, a gap of 0.091 against the 0.10 target, so one more correct comment (22 vs 17, a gap of 0.114) would have passed. On a 44-comment test split a single comment moves accuracy by 0.023, so a miss of 0.009 is smaller than the noise in the measurement. I still hold MISSED, because the criterion says the gap must hold on all three seeds and does not allow "close enough". Seed 42 is short by about 0.08 and on seed 7 the checklist actually beats the model (−0.091), so even a generous reading of seed 2024 would not rescue the criterion. A near-pass on one seed of a model that predicts `hot_take` almost every time is noise, not evidence the model learned the labels.

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 1 (checklist +0.10) — missed on all 3 seeds.** The cause is the model, not the checklist. The trained model predicts `hot_take` for almost everything (seed 42: 20 of 20 true `hot_take` right, 1 of 11 `analysis`, 1 of 13 `reaction`), so its accuracy of 0.455–0.500 is roughly the 0.455 you get by always guessing `hot_take`. The checklist swings between 0.386 and 0.545 across seeds, because with 44 test comments one comment moves accuracy by 0.023. So "model beats checklist by 0.10" cannot hold when the model is only at the majority rate and the checklist is allowed to be lucky. Evidence: the confusion matrices and the checklist table above.

**Criterion 2 (`analysis` precision ≥ 0.75, recall ≥ 0.60) — missed on all 3 seeds.** Same cause: the model almost never says `analysis` (1 prediction on seed 42, none on seeds 7 and 2024), so recall is 0.091 / 0.000 / 0.000. This is a mix of too few examples and a hard label pair. Only about 70 of my 288 comments are `analysis`, about 49 of them in `r/hardware`, so roughly 49 land in a 201-comment training split. The agreement check shows it is also a boundary problem. Of my six disagreements with staff, five were piles (b) or (c): the staff taxonomy and mine disagree on what makes a fact load-bearing, and on where a first-person observation like "leaning at about 20 degrees" sits between `reaction` and `analysis`. That is a labelling-rule gap on the `analysis` boundary, and it limits how clean that label can be. It does not explain a recall of 0, though. A model that had learned even a noisy version of the boundary would predict `analysis` sometimes.

**Criterion 3 (cross-thread) — missed in all 6 runs.** In every run the model collapsed onto one label instead of reading the comment, so accuracy simply equals how common that label is in the test thread:
- Trained on `r/AskReddit`, tested on `r/hardware`: it predicted `hot_take` for all 123 comments on all 3 seeds. Accuracy was 0.309, which is exactly the `hot_take` share of `r/hardware` (38 of 123).
- Trained on `r/hardware`, tested on `r/AskReddit`: it called most comments `analysis` (129 of 165 on seed 42, 136 on seed 7, 78 on seed 2024). `r/hardware` is my most `analysis`-heavy thread (49 of 123), and `r/AskReddit` has only 21 `analysis` of 165, so accuracy was 0.255 / 0.170 / 0.364.

Training loss supports this. For the 104 `r/hardware` training comments it only fell from about 1.08 to 1.03 over three epochs, against 1.099 for pure chance on three labels. The model had barely started learning. The `r/AskReddit` model, with 140 training comments, got further (validation loss 0.95 to 0.88) but still ended up on the majority label. So this failure is mostly the same one as criteria 1 and 2 (too little data and too few training steps for the model to leave the majority label), not clear evidence of "learned one forum's habits". The split itself also cuts training data to 123 or 165 comments instead of 201, which makes it worse. The test cannot tell the two causes apart until the model first beats the majority rate within one thread. Whether it learned one forum's habits is therefore still untested.

**Criterion 4 (self-agreement) — missed.** This one is a labelling problem, not a model problem, and it matters for every other miss. I changed 15 of 40 labels on a blind relabel, using only my written decision rule. 13 of the 15 involved `hot_take` (9 times old `hot_take`, 4 times new `hot_take`). The flips were:
- 7 between `hot_take` and `analysis`
- 6 between `hot_take` and `reaction`
- 2 between `reaction` and `analysis`

Two clusters stand out in the disagreement list:
- Short predictions that contain a number or a mechanism, such as "It'll be twice as fast, and the software will be 4x as slow", went from `hot_take` to `analysis`. My rule says a number inside a hypothetical does not count, so this is pile (a), a rule I applied loosely.
- One- or two-word answers in the prediction threads ("Expensive", "Cloud based") flipped between `hot_take` and `reaction`. The rule does not say how to treat a bare answer, which is pile (b), a gap in the rule.

This matches the agreement report against staff, where five of six disagreements were piles (b) and (c) rather than slips. If I disagree with myself on 37.5% of comments, a classifier cannot be expected to reach 0.75 precision on `analysis`, and some of the model's poor scores reflect noisy labels, not only the collapse onto `hot_take`. Per `criteria.md`, the next step is to tighten the rule for those two clusters and relabel before judging the model again.

**Criterion 5 (confidence) — missed.** The model's confidence is close to the 0.333 you get from a coin-flip over three labels: the mean over 132 pooled predictions was 0.477 and the maximum 0.612. With the model so barely trained (validation loss only about 1.00 down to about 0.95 over three epochs, against 1.099 for chance), it never becomes sure about anything, so coverage at 0.80 is zero and the "right 85% of the time when sure" half of the criterion cannot even be tested. This is the same cause as criteria 1–3, not a separate calibration failure. Retraining here reproduced the saved accuracies exactly (0.500 / 0.455 / 0.477), so the confidence numbers come from the same models that produced the Run Log.

**Fix to attempt in The Improvement:** criteria 1, 2, 3 and 5 share one cause, a model that has not learned to leave the majority label, so one fix serves all of them: more epochs and/or a higher learning rate, possibly class weights, then re-run all five criteria on the same three seeds. Criterion 4 needs its own fix, which is tightening the decision rule for short predictions with a number and for one-word answers, and relabelling those comments, before the model is re-judged. Both attempts go in The Improvement.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 24 / 30 = 80%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:* "I tracked sleep against session quality for eleven weeks. Under seven hours the next day's intervals were 6-8 seconds per mile slower, every time bar one. Small sample, one runner, but it's consistent enough that I've stopped scheduling hard days after late shifts."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* `hot_take`: The data is one runner's private numbers, so nobody else can check them, and the definition asks for a "checkable" fact. The writer admits it's a small sample from one person. What they end up asserting is a personal rule of thumb, backed by evidence the reader has to take on trust.
>
> *Which pile:* (a) — the rule covered it and I applied it loosely

**2.**
> *The post:* "Marathon training plans are all the same plan with different fonts."
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* `analysis`: The claim is itself a comparison between plans, and "a named comparison" is on the `analysis` list. It can be checked by laying the plans side by side. The comparison is the whole argument, so it isn't a flourish added to a conclusion the writer had already reached.
>
> *Which pile:* (b) — the rule genuinely doesn't say

**3.**
> *The post:* "Every injury thread on this forum is the same injury and the same three replies."
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* `analysis`: It makes a specific, countable claim about thread history ("the same three replies") that anyone with access to the forum could check. It's a comparison across threads, and that comparison is all the post says.
>
> *Which pile:* (b) — the rule genuinely doesn't say

**4.**
> *The post:* "Got up at 5, drove ninety minutes, and it's cancelled. Standing in the car park in the rain reading the email."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* `hot_take`: It doesn't state any feeling. It states events and implies a verdict (this was a waste, or the organizers did it badly) with nothing to back it. A confident implied judgment, offered with no support, matches the `hot_take` definition.
>
> *Which pile:* (c) — the rule is ambiguous here and my reading is defensible

**5.**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* `analysis`: It contains a figure ("about 20 degrees") and a specific out-versus-back contrast, which could be checked against weather and course data. Rule 3 says recency doesn't outrank evidence, and the presence of a checkable fact is what decides it.
>
> *Which pile:* (c) — the rule is ambiguous here and my reading is defensible

**6.**
> *The post:* "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* `hot_take`: It carries an implied general claim, that shoe fit or choice matters less than people think. That claim is offered as an anecdote with nothing supporting it, which is the unsupported-claim pattern, even though the writer never states it. Rule 4's tie-break (pick the label the post spends most of its words on) points the same way, since most of the sentence's clauses relate to that shoe claim.
>
> *Which pile:* (c) — the rule is ambiguous here and my reading is defensible

**What the pattern in my disagreements tells me:**

I disagreed with staff on 6 of 30 posts, and every disagreement sits on a boundary: 3 on analysis/hot_take, 2 on reaction/hot_take, and 1 on reaction/analysis. Only 1 was a plain case of applying a clear rule loosely (a). The other 5 were gaps or ambiguity in the definitions: 2 where the rule doesn't say what counts as a "named comparison" (b), and 3 where I read personal experience as a claim and not as feeling (c). So my labeling errors come from the boundaries, not from any one label, and mostly from definitions that leave room for reading. That predicts that the model will struggle most on analysis vs hot_take, and that my 200 labels are least consistent on short claims and first-person posts.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


