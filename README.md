# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** 400 characters, as a ceiling rather than a window
**Overlap:** 0

I chunk on paragraph boundaries, and I prepend the document's title line to
every chunk. `CHUNK_SIZE` only fires on a paragraph longer than 400 characters,
which in this corpus is rare; `MIN_CHUNK_CHARS = 100` merges anything shorter
than that into its neighbour.

**Why not a character window.** `campus_life` is 88 posts averaging 317
characters. The starter's 800-character window never cut anything, so one post
was one chunk — including posts holding two unrelated thoughts.
`health_center.txt` is walk-in hours in its first paragraph and counselling
intake in its second. `dining_kestrel_commons.txt` is wait times, then opening
hours and prices. Asking about counselling waits returned a chunk that was half
about something else. Paragraph breaks in these posts are topic breaks, so
that's where I cut.

**Why the title rides along.** Splitting on paragraphs alone creates orphans.
Paragraph two of `housing_aldridge_hall_laundry.txt` reads "Best time to do
laundry here is Tuesday or Wednesday morning" — "here" names nothing once it's
separated from the title. Sample Chunk 3 below has the same problem with "It's
front-loaded". Prepending the title fixes both, and it's why splitting on
paragraphs didn't just trade a noise problem for a fragment problem.

**Why zero overlap.** Overlap repairs thoughts cut in half by an arbitrary
boundary. A blank line isn't arbitrary, and the title header already carries
the context overlap would have supplied.

**What changed, in numbers.**

| | Chunks | Average | Shortest | Longest |
|---|---|---|---|---|
| Starter (`fallback_split`, 800/120) | 88 | ~317 | — | — |
| Mine (`split_documents`, 400/0) | 135 | 217 | 117 | 409 |

Two things in that row are worth naming. The shortest chunk is 117 characters,
above the 100-character floor, so the corpus contains no fragments. The longest
is 409, which is over my stated ceiling — the ceiling applies to the paragraph
and the title is prepended afterwards, adding about 25 characters. That's the
rule working as written, not a chunk that escaped it.

**What I got wrong on the first pass.** I set the 100-character floor expecting
it to catch stray fragments. It mostly did something else: it merged short
paragraphs back into posts where both paragraphs were about the same topic —
`housing_aldridge_hall_noise.txt` has an 89-character opening that merged
forward, and the laundry post's short second paragraph merged back. Both pairs
belonged together. The rule was right for a reason I hadn't predicted.

**A property of this corpus that will matter later.** 20 of the 88 documents
open with one of three stock phrases — "I'm a junior and I've done this twice
now", "Asked about this a lot so writing it down", "People keep asking so". All
of the `*_noise.txt` and `*_workload.txt` files are near-templates of each
other. Twenty chunks sharing an opening sentence look more alike to the embedder
than their content warrants, which should narrow the gap between my in-corpus
and out-of-corpus distances in Milestone 4.

## Sample Chunks

All five produced by `chunker.py::split_documents`.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

Answers "when can I add a course", "how late can I drop", and "does dropping
show on my transcript" without any surrounding text.

**Chunk 2** — source: `course_cs_340.txt#0` — produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus
a project that runs the whole term. Assessment: one midterm and a final, both
open-book. Lightly curved, usually two or three points.
```

Answers how CS 340 is assessed and whether exams are open-book. A third of it
is the stock opening sentence, which carries no information.

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time,
not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```

Answers "how many hours a week is PHYS 130". Note "It's front-loaded" — "it"
only resolves because the title is prepended. Without that, this chunk breaks.

**Chunk 4** — source: `health_center.txt#1` — produced by: `chunker.py::split_documents`

```
The health centre

Counselling is separate, in the same building, and has its own intake process
with a shorter wait than people expect — usually three or four days for a first
session.
```

Answers "how long is the wait for counselling". This chunk did not exist under
the starter's chunker — it was the second half of a document whose first half
is about walk-in hours, so a counselling question retrieved both.

**Chunk 5** — source: `housing_morrow_house_noise.txt#0` — produced by: `chunker.py::split_documents`

```
Noise levels in Morrow House

Asked about this a lot so writing it down. Loud until about 1am on weekends, no
enforced quiet hours.
```

Answers "are there quiet hours in Morrow House". Shortest of the five, and the
first sentence is the stock opening, but the answer survives.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
