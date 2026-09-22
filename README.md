# The Unofficial Guide

Cottons Kaka · corpus: `campus_life`

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

This is a question-answering system over `campus_life`: 88 short posts written
by students about a university — dining halls, dorms, courses, and the
administrative rules nobody explains properly. You ask a plain question like
"is the housing lottery actually random?" and it answers from those documents
and names the file it used, rather than from anything the model happens to
know. It handles specific questions with a real answer in the corpus — laundry
prices in a named building, how long you have to file a grade appeal, whether a
course's exams come from the lectures or the textbook. Ask it something the
documents don't cover and it checks how close the nearest chunk actually was
and refuses instead of guessing.

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

I picked this question deliberately: it's the one most likely to be attributed
wrongly. Five chunks come back and two of them quote the same $1.75 from a
different building.

**Question:** How much does a wash and dry cost in Aldridge Hall?

**Answer:**

```
(best distance 0.258, cutoff 0.6)

A wash costs $1.75 and a dryer costs $1.50 in Aldridge Hall
(housing_aldridge_hall.txt and housing_aldridge_hall_laundry.txt).

Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt,
housing_calder_annexe.txt, housing_innisfree_hall.txt,
housing_innisfree_hall_laundry.txt

1 model calls this session, 538 tokens (495 in, 43 out)
```

Three of the five retrieved chunks are about other buildings, and
`housing_innisfree_hall_laundry.txt` quotes the same price. The answer named
neither. Both files it did name genuinely carry the fact —
`housing_aldridge_hall.txt` mentions laundry costs alongside everything else
about the building, and `housing_aldridge_hall_laundry.txt` is the dedicated
post — so naming two sources here is accurate rather than hedging.

**On the grounding instruction.** I read `GROUNDING_INSTRUCTION` in
`generate.py` and decided not to change it. It tells the model to use only the
documents provided, to refuse when they don't cover the question, and to name
the file. What it does not do is say anything about what to do when several
documents say nearly the same thing, which is the shape of my corpus — so I
tested it on the worst case rather than guessing, and it held. Tightening it on
speculation would have made it harder to tell, in unit 2, whether a change I
made was the thing that helped.

**My relevance cutoff:** 0.6

I measured rather than inherited it. Ten questions through `python app.py
retrieve` — my five, then the five in `OUT_OF_SCOPE`:

| Question | In corpus? | Best distance |
|---|---|---|
| How long do I have to file a grade appeal? | Yes | 0.1729 |
| Is the housing lottery actually random? | Yes | 0.2483 |
| How much does a wash and dry cost in Aldridge Hall? | Yes | 0.2582 |
| How much printing does each student get per semester? | Yes | 0.2749 |
| Are CS 210 exams based on the textbook or the lectures? | Yes | 0.3799 |
| What is the capital of Mongolia? | No | 0.8246 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8477 |
| How do I write a for loop in Rust? | No | 0.8768 |
| Who won the 1994 World Cup? | No | 0.8859 |
| How do I change the oil in a diesel engine? | No | 0.9340 |

**The two groups.** In-corpus runs 0.1729 to 0.3799. Out-of-corpus runs 0.8246
to 0.9340. Nothing lands between 0.38 and 0.82 — a gap of 0.44 with no overlap
at all. The midpoint is 0.602, so the starter's 0.6 turns out to sit almost
exactly in the middle of my gap. I kept it, but it's now a number I can defend:
it clears my worst in-corpus question by 0.22 and my closest out-of-corpus
question by 0.22. Moving it anywhere between roughly 0.45 and 0.80 would change
nothing about these ten questions, which is what a gap that wide means.

**What I expected and didn't get.** 20 of my 88 documents open with one of three
stock phrases, so I expected the two groups to be squeezed closer together than
this. They weren't. The templates do show up — `course_hist_118_exams.txt` is
the top hit for the Mongolia question, the World Cup question *and* the Rust
question, because "Modern World History" is the nearest thing this corpus has to
a world-history question — but they arrive at 0.82 and above, well outside the
gap. So the boilerplate changes *which* wrong document wins, not how close the
wrong document gets. That distinction is worth more to me than the prediction
would have been if it had been right.

**A crowding problem the gate doesn't catch.** The Aldridge laundry question
retrieves the right chunk first (0.2582), but four of the five chunks it brings
back are about *other buildings'* laundry, and
`housing_innisfree_hall_laundry.txt` quotes the same $1.75. The gate is
perfectly happy — the best distance is fine. The risk is attribution: an answer
that cites Innisfree would be factually right and still wrong. That is what
criterion 5 is for, and I didn't know it was a live risk until I read this
output.

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
