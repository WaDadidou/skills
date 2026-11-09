---
name: product-pass
description: Do a product pass on an app before a release. Learn what changed since the user's last visit, check the open issues, use the app like its users (on a real device when one is plugged in), draft one local issue per finding with screenshots, check the drafts against the code, then plan the release in a meta-issue. Use when the user says "do a pass on the app", "tour of the app", "find UX issues", "prepare the issues for the next release", or hands over a prompt asking for that.
---

# Product pass

Follow `PROMPT.md` in this same folder, in full. Read it now, before doing anything.

```
Read ~/.claude/skills/product-pass/PROMPT.md
```

If a `product-pass-<repo>` skill exists for this repo, read it right after: it holds the repo's
reference app, devices, folders and conventions.

Eight points that fatigue drops first.

1. **An issue says what was seen, not why.** Conditions, number of tries, method (a finger or an
   injected gesture, an ear or a system dump), what was not tested. No cause, no fix: whoever
   takes the issue reproduces it first. Hypotheses live in the private index. A proposal goes in
   only when the owner asks for one, under its own heading.

2. **A summary keeps its conditions.** "Seen once, phone locked, gesture injected" turned into
   "it happens" is how a false issue gets published. Never dismiss a lead by reasoning: measure
   it, or write that it was not measured.

3. **The reference app decides behaviour.** When the team's rule is "if the stock app does it and
   we don't, we take it", say what the stock app actually does, with its source: seen on a
   device, read in the vendor's guide, or not measured. The user is not an engineer of stock
   apps: when their instinct departs from the standard, say so in one line and let them choose.

4. **Nothing leaves the machine without an explicit go.** Drafts stay in the user's private,
   untracked folder, and nothing is committed. Opening an issue, editing a published one and
   commenting each need the go. A choice clicked in a question is not a go on a text the user
   has not read.

5. **One index, one status per issue.** Draft, published as #N, waiting for a test, retired.
   Every report says which. This is what keeps a pass from turning into a mess when quick issues,
   drafts, reviews and findings from other sessions pile up in the same week.

6. **The code check runs on the drafts, before they open.** On an issue already open, only check
   whether the code moved under it: fix the body of your own, comment on other people's. Every
   fact that goes public is verified by you, not only by a helper.

7. **Show, do not name.** A visual proposal comes with an image at real size, in context, labelled
   as a mockup. Draw from the project's design system; never ship a third-party asset that needs
   an attribution.

8. **Ask, concretely; say when blocked.** Name the screen and the element in every question. When
   something blocks (no device, no access, no second person), say it in one plain sentence, with
   what would unblock it.

This prompt is also designed to be pasted as-is into another agent. If the user asks for it,
give them the contents of `PROMPT.md` without paraphrasing.
