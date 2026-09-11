# skills

> # 🚧 WIP 🚧
>
> **Work in progress.** Personal Claude Code skills, extracted one at a time from real
> sessions. Nothing here is stable yet: names, structure and prompts still move.

My [Claude Code](https://claude.com/claude-code) skills. A skill is a folder with a
`SKILL.md` whose front matter tells Claude when to load it, plus whatever files that
skill needs.

Written in English, so they travel. My repo-specific and personal skills stay
on my machine.

## Skills

| Skill | What it does |
| --- | --- |
| [`onboard-repo`](onboard-repo/) | Build up context on a repo you just landed on. Asks scoping questions, explores, proposes a table of contents fitted to *that* repo, and writes only what you keep. |
| [`review-pr`](review-pr/) | Review a GitHub pull request end to end. Rebuilds the PR's history, checks whether CI actually ran, reads the diff and maps the callers, then posts a short review with inline comments and suggestions. |

## Install

Clone anywhere, then link the skills you want into `~/.claude/skills/`:

```sh
git clone git@github.com:WaDadidou/skills.git
ln -s "$PWD/skills/onboard-repo" ~/.claude/skills/onboard-repo
ln -s "$PWD/skills/review-pr" ~/.claude/skills/review-pr
```

Or make `~/.claude/skills` itself the clone, so editing a skill and committing it are
the same gesture.

Skills are picked up at session start, so restart Claude Code after adding one.

## Credits

Four rules in [`review-pr`](review-pr/) come from
[davd-gzl/skills](https://github.com/davd-gzl/skills) (MIT): measure never
assume, the merge-base discipline, a claim carries the run that proves it, and
the shape of a posted comment.

## License

MIT, see [LICENSE](LICENSE).
