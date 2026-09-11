---
name: review-pr
description: Review a GitHub pull request end to end. Rebuilds the PR's history, checks whether CI actually ran, reads the diff and maps the callers, then posts a short review with inline comments and suggestions. Use when the user says "review this PR", "help me review", or gives a pull request URL.
---

# Reviewing a pull request

The point is to **save the reader time**, not to prove you read the code. A
useful review states what it verified, asks the two or three questions that
actually need someone's decision, and stops.

A repo may have a skill extending this one with its map and its conventions.
Read that first if it exists.

## Three principles

Taken from davd-gzl's public skills (<https://github.com/davd-gzl/skills>, MIT).

1. **Measure, never assume.** A convention, a capability and a count come from a
   command run this session. Never from memory, never from a file that recorded
   them once. If you write "this repo has no frontend tests", it is because you
   just ran the `find`.
2. **Merge-base discipline.** A problem that also fires on the base is not a
   finding of this PR. Check before you blame the diff.
3. **A claim carries the command that proves it.** Line numbers included, read
   off the PR's head, not off the default branch.

## Procedure

### 1. Rebuild the chain

A PR often has ancestors: an issue, an abandoned PR, a PR that was reframed.
**Scope is judged against what the maintainer asked for, not in the abstract.**

```bash
gh pr view <PR> --json number,title,author,state,body,additions,deletions,changedFiles,baseRefName,headRefName
```

Follow the `#nnnn` refs in the body, and read the original issue: it says what
the user wanted, which is not always what the PR delivers.

### 2. Isolate the human comments

Review bots post walls of text that drown everything. Filter them out.

```bash
for PR in <numbers>; do
  for EP in issues/$PR/comments pulls/$PR/comments pulls/$PR/reviews; do
    gh api repos/<owner>/<repo>/$EP --paginate \
      --jq '.[] | select(.user.login|test("bot|qodo|sonar|codecov";"i")|not)
            | "=== \(.user.login) \(.created_at // .submitted_at)\n\(.body)\n"'
  done
done
```

The maintainer's comment on the previous PR is often the key to the scope.

### 3. Check whether CI actually ran

**Do this every time. It is often the highest-yield point of the whole review.**

```bash
gh run list --branch <headRefName> --limit 10
```

`action_required` means **nothing has been tested**: on a fork PR, GitHub waits
for a maintainer to click "Approve and run workflows". `gh pr checks <PR>` can
show green checks and suggest the opposite, because **GitHub apps** (Sonar,
Snyk, GitGuardian, Codecov) run without approval. Only the repo's own workflows
count.

When they have not run, run the suite locally. It is the most useful missing
piece of information, and it turns a complaint into a contribution. Take the
commands from the repo itself: `Makefile`, `package.json`, or the workflow.

**Three passes before pinning a failure on the PR:**

1. The full suite gives you the list of failures.
2. **Re-run them serially**, no parallelism. Whatever passes then is a
   scheduling flake, not a finding. A worker that dies produces several at once.
3. **Re-run the rest on the merge base** (`git merge-base <base> <head>`).
   Whatever fails there too does not belong to the branch. Cross-check with
   `gh run list --branch <base> --limit 3`: if the base is green in CI and red
   on your machine, it is your local environment.

Then run the test files the PR touches specifically.

A local run does not replace CI, which also does the lints and the images.
**Claim only what you ran.**

### 4. Read the whole diff, then map it

```bash
git fetch origin pull/<PR>/head:pr-<PR> && git checkout pr-<PR>
git diff --stat <base>...pr-<PR>
git diff <base>...pr-<PR> -- <source files, tests excluded>
```

Then, for every function or property the PR introduces or whose semantics it
changes, `grep -rn` every caller, **frontend included**. A PR that changes what
an API field returns touches screens it does not modify.

### 5. Write the verification table before the review

One row per thing checked, with the `file:line` and the verdict. This is what
the review leads with. **A check that holds is worth as much as a finding.**

### 6. Draft

Shape of a finding: **the problem, its stake, the line it sits on, stop.** No
sprawling justification, no redesign proposal. The reader who did not ask for
it should read it once.

Write in the language of the repo.

**Decide who each finding is addressed to before you write it.** A review has
three readers and they are not interchangeable.

| Reader | Gets | Example |
|---|---|---|
| **The author** | the default. Everything they can fix themselves | a missing doc line, a bug, a suggestion |
| **The maintainer** | what the author cannot act on alone, and design calls they cannot settle unilaterally | approving the CI workflows, "should this refuse at boot instead?" |
| **Later readers** | the verification table, months later, on a public repo | which entry paths you enumerated and what held |

Most findings belong to the author: they wrote the branch, they will fix it.
Addressing the whole review to the maintainer is the common mistake, and it
reads as going over the author's head.

- A finding only the maintainer can act on **says so**, by `@`-mention or by
  naming the move. Do not order the author to do something they cannot.
- A design call the author cannot settle alone is phrased **as a question**,
  not as a defect. "Deliberate?" not "this is wrong".
- Judge scope against what the maintainer asked for, but write the finding to
  whoever can act on it.

On a repo with one central maintainer, they are a second reader for anything
touching scope. On a repo with many committers, there may be no single one:
then the author is the only addressee that exists.

**Four findings maximum.** Past that you are transferring your load onto the
maintainer instead of lifting it. Cut the nits.

A reflex that pays on a multilingual repo: **render the interpolated i18n
strings, in the locales other than English.** A sentence that reads in English
can be broken elsewhere, when the injected label is a verb where English has a
noun phrase. That is a typical contribution from a non-English reviewer.

### 7. Next round

When the author pushes fixes, compare patch-ids to tell genuinely new code from
a branch that merely moved on its base. **Nobody re-reviews unchanged code.**

```bash
git log --format='%H' <base>..pr-<PR> | xargs -n1 git show | git patch-id --stable
```

## Posting the review

A GitHub review is **one body plus an array of inline comments, in a single
call**. Four comments posted separately make four notifications and arrive out
of order.

```bash
gh api repos/<owner>/<repo>/pulls/<PR>/reviews --method POST --input payload.json
```

```json
{
  "event": "COMMENT",
  "body": "the body",
  "comments": [
    {"path": "path/file.py", "line": 27, "side": "RIGHT", "body": "..."},
    {"path": "path/other.py", "start_line": 259, "line": 265,
     "start_side": "RIGHT", "side": "RIGHT", "body": "..."}
  ]
}
```

A suggestion is a ` ```suggestion ` block inside a comment's `body`. It replaces
**exactly** the anchored lines, indentation included.

**The constraint that settles everything: you can only anchor on lines present
in the diff.** The most actionable finding often bears on what is missing, hence
on a file outside the diff: it stays in the body. Check before posting, a single
invalid anchor fails the whole call.

```bash
gh api repos/<owner>/<repo>/pulls/<PR>/files --paginate > files.json
~/.claude/skills/review-pr/check-anchors.py files.json payload.json
```

Other traps:

- `line` is the **right-side** number, after the diff, at the head commit.
- Multi-line needs `start_line` **and** `line`, `start_side` **and** `side`.
- `event`: `COMMENT` for an opinion, `REQUEST_CHANGES` to block, `APPROVE` to
  sign off. A second pair of eyes who is not a maintainer posts `COMMENT`.
- **Omitting `event` creates the review as `PENDING`**: readable in the browser,
  then submitted or discarded. That is the safety net before sending.

**Never post unless the user asked for it in the current turn.** Show the body
and the JSON, wait for the word.

### Disclosing AI assistance

**Look for the repo's policy before posting**, it often exists.

```bash
grep -rn -i 'AI contributions\|AI-assisted\|generated with AI' README.md CONTRIBUTING.md .github/
```

When the repo asks for transparency, one line at the end of the body is enough.
It has to do three things and not one more: **say it was AI-assisted, keep
ownership with the user, and give the reader something to verify against.** That
is what the policy is after, not a badge.

> AI-assisted, per the README. I directed it and checked every claim before
> posting; the permalinks are pinned to `<sha>` so you can verify any of them.

What **not** to write: the name of the tool or of the skill. It tells the
maintainer nothing about how to read the review, and it shifts responsibility
onto a tool when the user is the one signing. Trust comes from the commands,
the shas and the links already in the review, not from a mention.

With no policy in the repo, it is the user's call, and their default rule wins.
An explicit request from them in the current turn outranks any standing rule
that says otherwise.

### Editing a review already posted

REST `PUT /repos/<owner>/<repo>/pulls/<PR>/reviews/<id>` answers **404 when you
lack write access on the repo**, even on your own review, and even when `GET` on
the same URL works. Go through GraphQL:

```bash
NODE=$(gh api repos/<owner>/<repo>/pulls/<PR>/reviews/<id> --jq '.node_id')
gh api graphql -f query='
mutation($id:ID!,$body:String!){
  updatePullRequestReview(input:{pullRequestReviewId:$id, body:$body}){
    pullRequestReview { url lastEditedAt }
  }
}' -f id="$NODE" -f body="$BODY"
```

An edit notifies nobody, so it is the right move for an afterthought. For an
inline comment it is `updatePullRequestReviewComment`.

## Final check

Last pass before showing the JSON, over the artifact and not from memory. It
does not judge the substance, which is already settled: it catches what makes a
review **stale, unreadable or expensive**.

1. **Freshness.** Is `headRefOid` still the one you read? Is the PR still open,
   not draft, with no new comment or review since you read it? A review of a
   tree nobody will read is wasted. Re-run this right before posting, not at the
   start.

   ```bash
   gh pr view <PR> --json headRefOid,state,isDraft,mergeable,updatedAt
   gh api 'repos/<owner>/<repo>/issues/<PR>/comments?since=<the date you read it>'
   ```

2. **The anchors say what the comment claims.** `check-anchors.py` verifies the
   line is inside a hunk, not that it carries the right code. Print the anchored
   lines next to each comment's first sentence, and read.

3. **No dangling deixis.** At an anchor the reader sees six lines, not the file.
   "the comment below", "this line", "above" have no referent when the anchored
   block already contains a comment. Name the line or the symbol.

4. **Nothing that duplicates a bot or a resolved thread.** When your finding
   follows up on the fix to an already-resolved thread, say so and name the
   commit, otherwise it reads as reopening it.

5. **Every finding names the decision it asks for.** A question, a choice
   between two options, or a clickable suggestion. A finding with no ask is
   commentary, and it costs a read for nothing.

6. **Every finding reaches someone who can act on it.** Approving the workflows
   is the maintainer's move, not the author's. State the fact, do not order.
   Re-read the addressing table in step 6: a review aimed at the wrong reader
   is work for both of them.

7. **The body / inline split is right.** What cannot be anchored goes in the
   body, the rest goes inline, nothing appears twice.

8. **Every number and every quoted output comes from a command run this
   session.** Line numbers re-read on the PR's head, test counts taken from the
   run, not from a memory.

9. **References carry a permalink, pinned to a sha.**

   ```
   https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<n>
   https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<a>-L<b>
   ```

   - **Pin to a sha, never to a branch.** A branch link follows the head: the
     line number drifts and ends up pointing at something else. A sha permalink
     is immutable, it cannot rot. If it becomes historical after a force-push,
     that is correct: it shows the tree you reviewed.
   - **The head sha for the branch's code, the merge-base sha for what is not in
     the PR** (a doc the PR does not touch is cited on the base, not on the
     branch).
   - **The body needs links, the inline comments do not.** In the body the
     reader is not in the file, and some references are not even in the diff.
     Inline they have the file in front of them: only link a reference to
     **another** file, or to a line outside the displayed hunk.
   - GitHub expands a range permalink into a code excerpt inside the comment, so
     a link there is worth a quotation.
   - Leave shas and `#1234` bare: they autolink.

## After posting

Offer the user a briefing on their own review: each finding in plain words, the
likely pushback and the answer, and an explicit list of what they could not
verify. They may have to justify the review out loud, to people who know the
code better than they do, without notes in front of them.

Ask where to write it, and never assume last time's location.

## What we do not raise

- **Performance**, unless the PR touches a hot path or a query. A reflex
  performance comment shows.
- **Security in "what if" mode.** Enumerate the entry paths, say which ones
  hold. One verified list beats ten open questions.
- **What the repo does not do.** Measure before demanding tests in a layer that
  has none.
- **Style nits** the linter already catches.
