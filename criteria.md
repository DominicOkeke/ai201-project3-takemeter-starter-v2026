# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

**Accuracy beats a simple checklist by at least 10 points.** Before training, I write a 10-minute rule-of-thumb checklist (a number, year or product name means `analysis`; a question or very short comment means `reaction`; everything else is `hot_take`) and score it on the same held-out set. TakeMeter's accuracy must be at least 0.10 higher than the checklist's, on all three seeds.

**Why this target:** My labels hinge on checkable specifics, so a keyword checklist is a real competitor. If a few lines of rules land within 10 points of the model, it isn't worth building. A checklist should stumble on my hard cases (numbers inside hypotheticals, jargon with no claim), which is where the model has to earn its gap.

---

## 2.

**When TakeMeter says `analysis`, it is right at least 75% of the time (precision ≥ 0.75), and it finds at least 60% of the real `analysis` comments (recall ≥ 0.60), on all three seeds.**

**Why this target:** Calling an opinion "evidence-backed" misleads a reader more than missing a good comment, so precision is held higher than recall. Recall is looser because `analysis` is my smallest label (65 of 292), so only about 13 land in a test split and its score will jump between seeds.

---

## 3.

**It works on a thread it has never seen.** Train on r/hardware and test on r/AskReddit, then the reverse. Accuracy must be at least 0.60 in both directions and no more than 10 points below its normal held-out accuracy.

**Why this target:** This checks that it learned what `analysis` looks like and not one forum's habits (r/hardware is technical; r/AskReddit is mostly short predictions). Each thread has few `analysis` examples (47 and 18), so this is a rough warning sign, not a precise score. Always guessing `hot_take` scores 0.55 on r/AskReddit, so 0.60 there is a floor, not a stretch.

---

## 4.

**I agree with myself.** When I relabel 40 random comments at least 3 days later without looking at my old labels, I give the same label on at least 34 of 40 (0.85), and Cohen's kappa is at least 0.70 (agreement after removing lucky matches). Stretch goal: a classmate using only my written decision rule agrees with me on at least 75% of the same 40.

**Why this target:** If I can't label the same comments the same way twice, I can't expect a model to. 21 of my 292 labels are flagged borderline, mostly `analysis` vs `hot_take`, so I expect most disagreements there. If I score under 0.85, I tighten the rule and relabel before judging the model.

---

## 5.

**When TakeMeter is at least 80% sure, it is right at least 85% of the time, and it is that sure on at least 25% of comments.** Below 50% sure, it shows "uncertain" instead of a label. Measured on predictions pooled across the three seeds.

**Why this target:** A confident answer should beat the average, and 85 is deliberately above 80 so that "80% sure" means something. The 25% coverage rule stops it passing by being confident only on easy cases like short `reaction` comments (95 of my 292). Predictions are pooled because a single test split leaves only about 15 comments in the top-confidence group.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
