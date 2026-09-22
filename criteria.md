# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Four of my five questions are answered in a single document with distinctive
wording — "credit hours", "$1.75", "fifteen days", "$30" — so retrieval should
find them. The CS 210 question is the one I expect to be hard: the corpus has
three CS 210 documents (the base post, the exams post and the workload post)
that share most of their vocabulary, so the chunk that wins may be the wrong one
of the three. 4 of 5 leaves room for exactly that, and not more.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
All five and not four because this is enforced twice over, not left to luck.
The relevance gate refuses before the model ever runs when nothing retrieved is
close enough, so the model is never handed thin material and asked to be honest
about it. And `GROUNDING_INSTRUCTION` in `generate.py` tells it explicitly to
name the file. For this to come out at 4 of 5, the model would have to ignore a
direct instruction on a question where retrieval worked — which would be a
finding worth having rather than a target I should have set lower.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I measured both groups in Milestone 4 before setting this. My five in-corpus
questions land between 0.1729 and 0.3799; the five in `OUT_OF_SCOPE` land
between 0.8246 and 0.9340. Nothing falls in between — a gap of 0.44 with my
cutoff of 0.6 sitting in the middle of it. On that evidence all five of the
out-of-corpus questions are refused, so 4 of 5 is a target I expect to beat.
I am leaving it at 4 rather than raising it to 5 because the five questions
`run_eval.py` puts through the gate in unit 2 are not the only questions a
person could ask, and my gap was measured on exactly five. One refusal failing
on a question I haven't thought of yet is a margin I want.

---

## 4. Chunks stand on their own

All 5 of 5 chunks I sample read as a complete thought — something I could
answer a question from without reading what came before or after it.

**Why this target:**
5 of 5 and not 4 of 5 because I already hit 5 of 5 once. I sampled five chunks
after swapping in my own chunker and every one of them stood alone, so allowing
myself a failure I've already shown doesn't happen would make this unmissable.
My chunker cuts on paragraph breaks and prepends each document's title line, and
`MIN_CHUNK_CHARS = 100` merges anything shorter into its neighbour — the index
reports a shortest chunk of 117 characters, so there are no fragments anywhere
in the corpus. If that design is doing what I think it is, five of five should
hold on a different sample too. If it doesn't, the sample that breaks it tells
me something real about a document I haven't read.

---

## 5. The source named is the right one

For at least 4 of my 5 test questions, the source document named in the answer
is the file the answer actually came from — not merely some file.

**Why this target:**
Criterion 2 only asks that an answer names *a* source, which the grounding
instruction more or less guarantees. Nobody has checked whether it names the
*correct* one, and my corpus makes that a real risk: 20 of the 88 documents open
with one of three stock phrases, and all of the `*_noise.txt` and
`*_workload.txt` files are near-templates of each other. My CS 210 question has
three documents competing for it — the base post, the exams post and the
workload post — which share vocabulary heavily. I set 4 of 5 rather than 5 of 5
to allow exactly one of those near-duplicate collisions, and rather than 3 of 5
because two wrong attributions out of five is not a system I'd trust.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
