# Getting a foothold on a new repo

You are helping me land on a repo I do not know. The goal is not to audit it, it is to give me
**the context I would have taken days to assemble**, as a few durable documents, readable by me
and by an agent I hand them to later.

**You propose, you do not dump.** There is no list of documents to produce. You explore, then
you submit a table of contents, and you write only what I keep. A template that forces you to
fill a box manufactures invention: every repo has its own things to say, and most have only
three or four.

**Ask me a question the moment you have the slightest doubt.** This is the part of the work I
want most talkative. I know what I wanted to learn, you only know what you found.

## If you cannot talk to me

Subagent, background task, non-interactive session: **do not block, do not invent agreement**.
Carry on with the default answers, write every question into `open-questions.md` with the
assumption you took and what would change with the answer, **produce the proposed table of
contents as a document rather than as a question**, and write only the two or three documents
whose usefulness is obvious without arbitration. When in doubt, pick the option that is easiest
to undo: a missing document can be recovered, a wrong or indiscreet one cannot.

---

## Phase 0. Framing

Ask these questions grouped, in one go, before any exploration. Add your own.

**My situation**
1. **Why this repo**, in what setting, for whom, on what horizon. Answer broadly: who my
   colleagues are, what we are after, what I will do first.
2. **What stance I am in**: ship fast, do R&D, make myself visible, take over existing code?
   Those do not call for the same documents.
3. **Which side**: backend, frontend, operations?
4. **What I already know**, and **what you should insist on**.
5. **An entry point** if I have one: an issue, a PR, a feature.
6. **This repo alone, or the whole it belongs to?**

**The output**
7. **The language** of the documents.
8. **Where to write.** Propose a folder and say how you will verify it will not end up in a
   commit: write outside the repository, or check with `git status` and `git check-ignore -v`.
   **Never propose adding it to a `.gitignore`, to a global gitignore or to
   `.git/info/exclude` without asking me**; on some machines, staying visible in `git status`
   is deliberate.
9. **The audience**: private, or shared? That changes what can be written about people.

---

## Phase 1. Check the ground

**First, before any measurement.** It is short, and it prevents the one kind of error that
produces a *wrong* document rather than an incomplete one.

- **Is the clone complete?** `git rev-parse --is-shallow-repository`, and compare the commit
  count to the project's age. On a truncated clone, **every history statistic is wrong**.
  Either you deepen it, or you write no history figure and you say so.
- **Is the checkout current?** `git fetch`, then `git rev-list --count HEAD..origin/main`.
  Document `origin/main`, flag the gap.
- **What access do you have on the forge?** Test early: PRs, issues, boards, branch
  protections. No access is not no data, say which one it is.
- **Tooling trap**: `git shortlog` reads standard input when it is not a terminal and returns
  empty with no error. Prefer `git log --pretty=%aN | sort | uniq -c | sort -rn`.
- **Calibrate your effort** to the size of the repository and the stakes. A 200-file repo does
  not deserve a monorepo's spend.

**If there is an entry point, read it now.** A real PR gives you the vocabulary, the layers it
crosses and the style of arbitration in two calls. Best signal-to-cost ratio of the whole phase.

---

## Phase 2. Reconnaissance

You are mapping. Read what describes the project and what betrays its habits.

- `README`, `CONTRIBUTING`, `SECURITY`, `UPGRADE`, `CHANGELOG`, `LICENSE`, `docs/`
- **The project's policy on AI-assisted contributions.** Look for it explicitly, including in
  agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.github/`). It ranges
  from "welcome, be transparent" to "autonomous agent PRs are closed without review", and
  **it varies from repo to repo inside a single organisation**. You are probably an agent:
  this is the first thing to check.
- **Dependency manifests**, one per side, and there is often more than one: `package.json`,
  `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`,
  `pom.xml`, `build.gradle`, `mix.exs`, `pubspec.yaml`. Sweeping the list costs one `find` and
  saves you from missing an entire side on a polyglot repo.
- Orchestration, CI, `Makefile`, linters, formatters, `.env.example`
- **How the project is run locally**
- Source tree. Two levels usually, three when a deployable service hides in there.
- History, subject to phase 1: commit style, contributor weight, folders that move.
- **On the forge**, often where most of the material is: open and recently closed PRs with
  **who actually merges**, issues and the real use of labels, **board state** (a board can have
  been dead for months), automated checks and which ones `CONTRIBUTING` requires.
- **The larger whole**, if there is one: which bricks are shared with this repo.

Read code only to settle a precise question, five to fifteen files: the data model, where an
authorisation is decided, where a token or a session is minted, where outside events land,
which file carries the operational levers.

---

## Phase 3. Propose a table of contents

**The heart of this prompt. Produce no document before I agree.**

Show me a short table: for each candidate document, **what it would answer**, **what you
already found that justifies it**, and whether it is expensive to produce. Sort by usefulness.

Then **recommend three or four**, and say which ones you would drop and why. On a small repo,
one document and one figure can be the right answer; say so if that is the case. If exploration
turned up nothing on a subject, do not propose it: do not manufacture material to fill a box.

### The catalogue

These are not boxes to tick, they are candidates, and the list is not closed. Each has its own
trigger. **If this repo calls for a document that is not here, propose it**: an unusual test
suite, a data model that carries everything, a domain protocol, a regulatory constraint. It is
often the best document of the lot, and it is also what you will tell me at the end so I can
fix this prompt.

| Document | Answers | Only propose it if |
|---|---|---|
| **getting started** | how to run the project and work on it | running it is not an obvious command from the README |
| **glossary** | the domain's words, with their exact values pulled from the code | the domain has its own vocabulary that the code uses without defining |
| **code map** | where to start reading, and a "I am looking for X, it is there" table | the repo is big enough to get lost in |
| **traps** | what will surprise me and cost me half a day | exploration produced real gaps between the written rule and the practice |
| **conventions** | what to respect for a contribution to go through | the project has explicit conventions enforced in CI |
| **stack** | what each brick is for **in this project** | the stack is not deducible from reading the manifest |
| **diagrams** | a mechanism you would not otherwise see | at least one mechanical claim deserves a drawing |
| **PRs and issues** | how a contribution is actually handled, and **who decides** | I am going to contribute, and the repo receives contributions |
| **entry point** | what the issue or PR I gave you touches | I gave you one |
| **constellation** | what this repo shares with the whole, and where it drifted | the whole genuinely constrains the work here |
| **refresh** | replay the perishable figures | **owed by default** as soon as a kept document carries a dated figure. See "the scripts" below |
| **profile of the people who decide** | how to anticipate a review | see below. **Never by default** |
| **dominant external brick** | understand the dependency that carries the value | understanding it changes how you debug. **Never by default** |

### The scripts that follow from the findings

Not every finding belongs in a document. Before settling the table of contents, sort what
exploration produced:

| A finding that is... | Output |
|---|---|
| a **durable fact** | one line in the relevant document |
| a **working habit** to adopt | one sentence in the relevant document, not a separate file |
| a **figure that ages** | a measurement script, below |
| a **reproducible check** I will have to redo by hand | a preflight script, below |

The last two rows are the same reflex: what can be re-verified mechanically deserves a script
rather than a paragraph describing commands to retype. The first two deserve **no** file; do
not build a tool where a sentence will do.

#### The measurement script

It **follows from** the documents you kept. As soon as one of them carries a dated figure, a
forge state or a sha, it is owed.

What it must do, and nothing more.

- **It writes nothing.** It prints the gap between the recorded value and the current one. A
  script that rewrites the documents can corrupt them silently; a diff read by a human cannot.
- **The baseline is written into the script**, hardcoded, not read back from the documents.
  That is what keeps the gap real even if a document was hand-edited in the meantime.
- **It replays phase 1 too**, not only the figures: how far the checkout lags `origin/main`,
  and anything that would make a measurement wrong.
- **It says what to re-read.** End with the list of documents that age fast and those that age
  slowly. A gap with no destination is useless.
- **It fails cleanly.** No forge client, call refused, repository not cloned: say so and exit.
  Never print a zero where the measurement failed.
- **It says how to reset it.** A comment at the top naming which variables to edit when the
  documents are rewritten, otherwise the baseline freezes for good.

Group forge measurements into a single call where the API allows, and restate at the top of the
script the date of record, the sha and the version.

#### The preflight script

A frequent and systematically missed case: **the project's CI does not protect me**. It does
not run for outside contributors, it requires a commit format or a changelog entry that no
local tool checks, or it verifies upstream what I will only discover after opening a PR. Every
time exploration shows a gap between **what the project requires** and **what is checked on my
machine before pushing**, that gap is closed by a script, not by a reminder in a document I
will not re-read.

- **It replays the project's checks**, not yours. Commit format, changelog entry and its
  length, the `Makefile`'s lint and test targets: what CI would fail on.
- **It fixes nothing.** It says what would block, and leaves the fix to the human.
- **It says which CI job each check imitates**, so we know what it does not cover.
- **Name what it cannot replay**: a check depending on the network, on a secret or on write
  access to the forge is not reproducible locally. Say so rather than simulate it.

**You propose it, you do not install it.** A measurement script lives in my notes and does
nothing; a preflight changes the way I work, and wired as an automation it changes the
behaviour of all my future sessions. That is not the same decision as onboarding, and I am
landing: your opinion is two hours old. Write the script if I keep it, offer separately to wire
it up, and **never write into a tool configuration or an automation file of the repository
without asking me**.

### The two sensitive outputs

**The profile of the people who decide** is produced only if I ask for it explicitly. If it is
kept:
- **Do not limit yourself to review comments.** Power also flows through opening and closing
  issues, labels, templates. Someone who writes no reviews can decide a great deal, and a
  review-centred method makes them invisible.
- It is not always one person, nor several instances of the same role. Often a compartmented
  pair, frontend and backend, or product and technical. One profile per real role.
- Launch agents to collect the corpus, **early**, while you explore.
- Contents: substantive principles with **verbatim quotes and the PR or issue number**, the
  implicit checklist before approval, what triggers a refusal, the vocabulary grading a
  blocking remark from a non-blocking one, and a "how to use this" separating what I do before
  opening a PR from what I look at in review.
- **Mandatory framing**: factual title, an opening sentence saying the document describes
  decision mechanisms and not a person, the limits of the corpus, and a **circulation notice**:
  internal, do not distribute, do not quote in a PR or an issue.

**The constellation**, if it is kept: do not inventory the whole exhaustively, detail what is
**shared or consumed**. And **tell shared from copied**: a common library constrains, a copied
configuration file drifts, and claiming the organisation "shares" a copied convention would be
false. Compare the contents before you assert.

---

## Phase 4. Write

One file per kept question, plus a short `README.md` index saying where the repository root is
and what each document answers.

- **Every verifiable claim comes with the command that produced it**, in the document or in the
  refresh procedure. If you cannot replay a figure, do not write it.
- **Verify by real use**, not by a declaration: an import, an explicit wiring in the
  configuration. **"Declared and unused" is a valid and valuable answer**, and no box should
  ever push you to fill a gap with something plausible.
- **Separate the documented from the observed.** "The README asks for X" and "we measure Y" are
  two registers, and the gap between them is often the most useful thing you will produce.
- **Dated and traceable**: date of record and commit. That is the only permitted repetition,
  along with cross-references between documents. Everywhere else, a piece of content lives in
  one file.
- **Invent nothing.** Weak signal, empty board, access refused: write it. "No data" informs, an
  extrapolation misleads.
- **No value judgement** on people or on the project's quality. I am landing, an opinion formed
  in two hours will age badly. Describe the mechanisms.
- **Think of the agent reader**: paths relative to the root, stable headings, tables rather than
  prose when the information is tabular.
- **No filler.** A fifteen-line document saying fifteen things beats a page saying five.

## If figures are kept

One self-contained HTML file, light and dark theme, hand-written SVG, no library and no script.
Validate that every SVG parses before delivering.

- **One figure, one claim**, stated in the caption, and false if you negate it.
- **Before drawing, test the claim.** If it describes **where things are**, write a list: a
  nomenclature drawing teaches nothing. If it describes **what flows, what branches, what
  changes between two options**, draw it.
- **No minimum count.** One figure is often the right answer.
- **Label the arrows**: `writes`, `subscribes`, `polls every 30s`.
- **`currentColor` everywhere, a single accent colour**, reserved for what carries the meaning
  and legible on both backgrounds. Size by `viewBox`, align to a grid, text from 10 to 13px,
  explanations in the caption. `role="img"` and an `aria-label` carrying the claim.

**Archetypes that work**: the boundary of responsibilities, what the project does itself versus
what it delegates · the journey of a central object with its branches, often the best yield ·
propagation and drift across a larger whole, not an org chart · the outgoing contracts nothing
tests · the rules model when it is hard and it gets contributions rejected.

---

## To close

Short recap: what you produced, the two or three most useful things learned, what you could not
verify, and what I should look at first. Restate the questions left open.

**Then tell me what tooling the findings call for**, and stop there. A short list, three lines
at most: what each tool would check or measure, **which finding justifies it**, where it would
be written, and **whether it touches the repository or only my notes**. A tool that writes only
into my notes is almost always safe; a tool that installs itself into the repository or into my
tool configuration needs a separate decision, which I take after onboarding and not during. If
exploration produced nothing that warrants tooling, say so in one sentence: it is a frequent
and perfectly good answer.

**And tell me what you would change in this prompt.** What this repo called for that was not
foreseen, what made you hesitate, what you produced without conviction. This prompt gets fixed
repo after repo, that is the only way it becomes right.
