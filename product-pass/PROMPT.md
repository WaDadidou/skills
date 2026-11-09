# Product pass: from "what changed" to issues ready for the next release

You are doing a product pass on an app: use it as its users do, find what breaks or falls short
of the reference app, and prepare issues the team can open and fix in the next release.

**Product, usage and UX only**, unless the user widens it. Infrastructure, security and code
quality are out by default. Open pull requests are context, not the subject: this pass does not
review them.

## Phase 0: scope (talkative, blocking)

Ask, in one round, the questions the repo cannot answer:

- **Which app, and since when**: the date of the user's last pass, or the last release they know.
- **The base of the next release.** Usually the main branch; sometimes a stack of open PRs that
  will merge first. Issues are checked against both: what users run today, and what will ship.
- **The reference app**, and the rule that goes with it. For an alarm clock: "if the phone's
  Clock does it and we don't, we take it". Which platforms count.
- **Devices**: a phone on USB (which one, debugging authorised?), an emulator, a second phone for
  anything between two people, a tester for a platform the user does not own. Test accounts, and
  who you may send things to.
- **Where private drafts go.** Never a tracked file. If the user's instructions name a folder,
  use it.
- **The issue format.** Default: the repo's existing issues, closed and open (title pattern,
  sections, language, length). Show one example and ask.
- What is out of scope, and who decides product questions.

When nobody can answer (no user in the loop), carry on with the defaults, write the questions at
the top of the index, and publish nothing.

## Phase 1: inventory

1. **What changed since the last pass.** `git log --since`, merged PRs, release notes or
   changelog, open PRs (context only). Note which open PRs form the next release's base.
2. **Open issues.** For each: still current? Done in code, partly done, duplicated, overtaken by a
   decision? One table, a verdict and an action each: keep, narrow, close, ask. For a colleague's
   issue, propose a comment that completes it rather than rewriting their text.
3. **Notes from outside the repo** (a teammate's doc, a dashboard, user feedback): requalify each
   point as a new issue, an existing issue, or "not a product issue", with the reason.
4. **What the repo already knows.** Before proposing anything, search the docs, audits, plans and
   changelog for the subject: say whether it is known, under which id, at which priority.

## Phase 2: plan the tests

Split the work three ways, and tell the user:

- **What you test yourself**, through the device on USB or the emulator.
- **What only the user can judge**: what is heard, what is felt half-asleep, what needs a second
  person, a real night, a real payment. A short prioritised list, one line each, with what to
  note and a screenshot when it is visual.
- **What you need from the user** to test: plug the phone, unlock it, authorise debugging, sign
  in, a second phone, a volume level. Ask before you need it, not twenty minutes in.

## Phase 3: use the app like a user

- Start with the build users have (the store version), then the release candidate if there is
  one. An emulator without sound proves nothing about sound.
- Compare with the reference app on the same device, screen by screen, and capture it too.
- **Device safety, every time:**
  - Before any action, check what is on screen: the user may be using the phone. If another app
    is in front, stop and ask.
  - Before and after every screenshot, check that no notification shade, private message or
    personal data is visible. Delete a capture that caught one.
  - Keep test sounds quiet. Never leave anything that can ring, notify or send after you go, and
    tell the user how to stop what you start.
  - Note every side effect (setting changed, volume, test data) and restore it at the end.
  - Destructive or long tests go on an emulator.
- **Journal** every measure: time, build, device, state of the app (foreground, background,
  killed), state of the phone (locked or not), method, number of tries, raw evidence (a log line,
  a dump). The journal is what answers "why do you say that?" a week later.

## Phase 4: one draft per issue

- One folder per issue, `issue-<slug>/`, with `issue.md` and its images. The first line of
  `issue.md` is the title; the rest is the body.
- **Title**: "Scope: observed effect", in the repo's language.
- **Body**, adapted to the format agreed in phase 0:
  - **Observed**: what happened, in which conditions, how many times.
  - **Steps**, when there are any.
  - **Expected**, or **Reference**: what the reference app does, with its source.
  - **Test conditions**: device, OS, build, method, tries, and what was not tested.
  - **Screenshots** for anything visual: real size, annotated, cropped of anything private.
  - Last line: "Reproduce this on a device before working on it."
- **One subject per issue.** When the title and the main subject diverge, split. A bundle of
  missing settings becomes one issue per setting.
- **Quick issues are fine.** When the user notes something in passing, a screenshot and one
  sentence make a valid draft. It still gets a folder, a row in the index, and the code check.
- Questions nobody can answer yet go into the issue, as questions.
- An issue that challenges a documented decision (a design rule, a deliberate behaviour) says so,
  and points to where the decision is written.

## Phase 5: the private index

One file, in the user's language, never published. It is the single source of truth.

- **Status of every issue**: draft, published #N, waiting for a test, retired (and why).
- **Classification**, one row per issue:
  - Importance: P0 (a core function fails, data is lost, strong pain every time), P1 (frequent
    pain, or the reference app does better), P2 (occasional), P3 (polish).
  - Frequency: how often a user meets it. An estimate, said as one.
  - Difficulty to reproduce: easy (a minute), medium (setup or waiting), hard (two devices,
    intermittent).
  - Evidence: device by hand, device by injected gesture, code, documentation.
  - Effort: S, M, L, plus native, server or console work when it applies.
  - Wider change: should the fix go beyond the issue? You may leave the scope here.
  - Dark zones: what is tricky, unknown, or a likely dead end.
- **Decisions** the user took, dated.
- **Unverified leads**: hypotheses from the code, kept out of the issues so they do not steer
  whoever fixes them.

## Phase 6: validate the format

Before writing the whole batch, show the user one draft and ask, with questions, whether the
format suits them: title, sections, length, language, screenshots. Default to the repo's existing
issues. Many short concrete questions beat one vague one.

## Phase 7: check the drafts against the code

Once the drafts exist, **before any is opened**:

- Read each against the code of the current release and of the next release's base. With many
  drafts, split the reading across read-only helpers by family, in a bounded number, then
  **verify yourself every fact that will go public**.
- Per draft: correct a wrong sentence, merge duplicates, split mixed subjects, mark "re-test on
  the next base" where the code path changes there, retire what is already fixed. A behaviour that
  turns out deliberate stays only if the owner wants to change it, and the draft says where the
  decision is written.
- Facts from the code go in as "From the code, not tested on a device", never as a cause.
- List what the code could not settle: it becomes the user's next device test list.
- **For issues already open**: only check whether the code moved under them. Fix the body of the
  issues you or the user wrote (the forge keeps the history); comment only on other people's. A
  pile of comments contradicting the body drowns the next reader.

## Phase 8: the meta-issue

A draft for one issue that gathers what the next release takes on:

- **Rules for this release**: the reference-app rule, "reproduce first".
- **Decisions taken**, short. For each open product question, give your recommendation and its
  reason. For behaviour, follow the reference app and cite it. Add a mockup when the decision is
  visual.
- **With the maintainer**: what must be agreed before the batch, such as a design rule to change
  or a deliberate behaviour to undo.
- **Before the batch**: what must merge or be fixed first, and the issues to re-test on the new
  base.
- **Lots**, by theme, ordered by importance.
- **Not in this release**, one line of why each.
- **To confirm before opening**: what was seen once and needs a second look.
- **Coverage**: what was tested, how, and what was not.
- **Release gate**: the device checks that must pass before shipping.

## Phase 9: publish, only on the user's go

- Search the forge for each title first, open and closed: a draft may already be an issue.
- Open first the issues that others cite, so their numbers replace placeholders.
- On GitHub: `gh issue create --title "…" --body-file body.md --attach image.png`, run from the
  issue's folder, where `body.md` is `issue.md` without its first line. `gh` uploads the images
  and rewrites their references. Check that the installed `gh` supports `--attach` before
  inventing a workaround.
- Read each body back from the forge and compare it with the local file. Record the number in
  the index.
- Labels follow the repo's conventions, for instance a label for any action needed in a store or
  service console.

## Phase 10: report

Short, in the user's language: what is published (numbers), what waits and for what (which test,
which decision), what is blocked and what would unblock it, the next step. Never "done" for
something only drafted.
