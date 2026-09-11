# skills

> # 🚧 WIP 🚧
>
> **Work in progress.** Personal Claude Code skills, extracted one at a time from real
> sessions. Nothing here is stable yet: names, structure and prompts still move.

My [Claude Code](https://claude.com/claude-code) skills. A skill is a folder with a
`SKILL.md` whose front matter tells Claude when to load it, plus whatever files that
skill needs.

Written in French, because that is how I work with Claude.

## Skills

| Skill | What it does |
| --- | --- |
| [`onboard-repo`](onboard-repo/) | Build up context on a repo you just landed on. Asks scoping questions, explores, proposes a table of contents fitted to *that* repo, and writes only what you keep. |

## Install

Clone anywhere, then link the skills you want into `~/.claude/skills/`:

```sh
git clone git@github.com:WaDadidou/skills.git
ln -s "$PWD/skills/onboard-repo" ~/.claude/skills/onboard-repo
```

Or make `~/.claude/skills` itself the clone, so editing a skill and committing it are
the same gesture.

Skills are picked up at session start, so restart Claude Code after adding one.

## License

MIT, see [LICENSE](LICENSE).
