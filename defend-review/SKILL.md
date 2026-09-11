---
name: defend-review
description: Write the briefing for a review you already posted, to understand it and to defend it out loud. One plain-language layer per finding, one layer of likely pushback and answers, and what you could not verify. Use after review-pr, or when the user says "write me the briefing", "I need to be able to defend this", "explain what you reviewed".
---

# Review briefing

The user may have to **justify their review out loud**, to people who know the
code better than they do, with no notes in front of them. This briefing serves
two moments: understanding the review when it lands, defending it in a meeting.

**It invents nothing.** Everything comes from the review already written and the
commands already run. If an explanation needs a fact nobody measured, run the
command or write that you do not know.

Write it in the user's language, which is not necessarily the repo's.

## Before writing: ask where

**Always ask where to put the file.** Do not infer it, do not reuse last time's
location without confirming.

When the location is inside a git repository, verify it will not end up in a
commit, and say how you verified:

```bash
git status --short
git check-ignore -v <path>
```

**Never propose adding it to a `.gitignore`, to a global gitignore or to
`.git/info/exclude`.** Staying visible in `git status` is sometimes deliberate.
A folder that is untracked and unignored is a legitimate state, not a problem to
fix.

## The register

Plain, **never hollow**. The reader is going to repeat these sentences in front
of engineers: a childish analogy discredits them, an exact sentence in everyday
words carries them.

- Yes: "the media server broadcasts a small packet of information to participants"
- No: "it is like a door left open"

The right level is that of a competent engineer who has not read this PR. No
line numbers: nobody recites one in a meeting. Give the file's role in the
system instead.

## The shape

One file, two layers per finding. The first is enough to understand, both
together serve before a meeting. Never two files: the same explanation written
twice eventually drifts apart.

### At the top

- **The link to the review**, the date, the head sha.
- **The PR in three sentences**: what happens today, what the PR changes, what
  it leaves alone.
- **Who each finding is addressed to**: a table, one row per finding, who can
  act. Answers "why did you tag them on that one" before it is asked.

### Per finding

- **In plain words.** The mechanism in everyday language, two to four sentences.
- **Where.** The role of the file or the component, not the line.
- **The impact.** What breaks, and who notices. Saying "nothing opens up that
  should not" when that is the case beats leaving it hanging.
- **If challenged.** The most likely objection as a quote, then the answer. This
  is what makes it a briefing rather than a summary.
- **What I concede.** Name the weak point. Conceding at the right moment is what
  buys credibility on the others. A finding with nothing to concede says so too.

### At the end

**What I do not know.** The most important block. Four or five lines, to be said
as written if the question lands, so the user answers "I would have to check"
instead of bluffing. It holds:

- what was not tested, and what was used instead
- the author's intentions that were not understood
- what was observed but kept out of the review, and why
- the state of the PR that could invalidate the review: a conflict, an expected
  rebase

## The check

- **Every finding in the posted review has its block**, including the ones in
  the body that could not be anchored.
- **Every claim in the briefing traces back to the review or to a run.** The
  briefing adds no material, it translates.
- **No line numbers** in the spoken layers.
- **The "what I do not know" block is not empty.** If it is, nobody looked.
