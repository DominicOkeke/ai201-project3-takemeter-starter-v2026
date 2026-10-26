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
- **Source Thread:** [Is the future of hardware just optimization? on r/hardware](https://www.reddit.com/r/hardware/comments/1pwxwx7/is_the_future_of_hardware_just_optimization/)
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

## Stress Test: Analysis vs. Hot_take

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
>
> *Could have been:*
>
> *I chose, because:*

**2.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**3.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

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
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

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
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



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
