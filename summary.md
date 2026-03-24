# Addict in 2026: Is It Still Needed?

## What it does

Addict lets you build nested dicts with dot notation instead of bracket soup:

```python
# without addict
body = {'query': {'filtered': {'query': {'match': {'description': 'addictive'}}}}}

# with addict
body = Dict()
body.query.filtered.query.match.description = 'addictive'
```

It auto-vivifies missing keys, recursively merges on `update()`, and supports freeze/unfreeze for strict mode. 159 lines of code, zero dependencies.

## The honest answer: probably not needed anymore

The package is well-made and solves a real problem, but Python has largely caught up:

- **`types.SimpleNamespace`** — built-in, covers basic attribute access
- **`dataclasses`** (3.7+) — better when you know your structure upfront
- **`pydantic`** — attribute access + validation + serialization, the modern default
- **`TypedDict`** (3.8+) — type-safe dicts without runtime overhead
- **`ChainMap`**, `**` unpacking, `|` merge (3.9+) — cover the merge use case

The one thing addict still does uniquely well is **auto-vivification** — `d.a.b.c.d = 1` creating the entire chain. Nothing in stdlib does that. But in practice, if you need deeply nested dynamic structures that often, your data model probably wants a rethink.

## Red flags for production use in 2026

| Concern | Detail |
|---------|--------|
| Last commit | January 5, 2021 — over 5 years ago |
| Python coverage | Tested up to 3.9; no CI for 3.10–3.13 |
| Still supports Python 2.7 | Dead weight, signals dated codebase |
| No type hints | Won't play nicely with mypy/pyright |
| No maintainer activity | Issues and PRs appear unattended |

It *probably* still works on 3.13 (it's a simple dict subclass), but "probably" isn't great for production.

## When it might still make sense

- Quick scripts or notebooks where you're building nested JSON/config on the fly
- Legacy codebases already using it (no reason to rip it out)
- Prototyping where you don't want to define schemas yet

## Verdict

Addict was ahead of its time in 2014. In 2026, Python's own tooling covers most of the same ground with better type safety and ecosystem support. For new projects, reach for pydantic or dataclasses instead. For existing code, it's fine to leave in place — just don't expect upstream fixes.
