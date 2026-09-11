---
name: onboard-repo
description: Build up context on a repo you do not know. Asks scoping questions, explores, proposes a table of contents fitted to THIS repo, then writes only what is kept. Use when the user lands on a project they do not know, or says "onboard", "survey this repo", "I am new to this repo", "get familiar with the repo".
---

# Getting a foothold on a new repo

Follow `PROMPT.md` in this same folder, in full. Read it now, before doing anything.

```
Read ~/.claude/skills/onboard-repo/PROMPT.md
```

Five points that fatigue drops first.

1. **You propose, you do not dump.** There is no list of documents to produce. Phase 3 is the
   heart: you explore, you submit a table of contents fitted to this repo, and **you write
   nothing before agreement**. Three or four documents are almost always enough. On a small
   repo, one document and one figure are the right answer.

2. **Check the ground before measuring.** Shallow clone, stale checkout, access refused on the
   forge: those are the only errors that produce a *wrong* document rather than merely an
   incomplete one. A `git shortlog` on a truncated clone invents a dominant contributor.

3. **Phase 0 is talkative and blocking when you can speak.** When you cannot, apply the
   prompt's fallback: carry on, record the questions, write the table of contents instead of
   asking for it, and produce neither of the two sensitive outputs (profile of the people who
   decide, dominant external brick).

4. **Look for the project's policy on AI contributions.** It varies from repo to repo inside a
   single organisation, from "welcome" to "closed without review". You are probably an agent.

5. **A finding that gets re-verified deserves a script; a script that acts does not install
   itself.** Perishable figures and checks the project's CI does not replay on my machine call
   for an executable rather than a paragraph. But you **propose** it: never write into a tool
   configuration, an automation file or a repository hook without explicit agreement.

This prompt is also designed to be pasted as-is into another agent. If the user asks for it,
give them the contents of `PROMPT.md` without paraphrasing.
