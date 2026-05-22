# C 单篇与批量拉取

## Goal

Fetch normalized metadata for one or more specific arXiv identifiers.

## Inputs

- one or more arXiv ids

## Commands

```powershell
arxiv paper get 1706.03762
arxiv paper get 1706.03762 2401.10401
```

## Success Criteria

- returned `entries` count matches requested ids when available
- title, authors, summary, links, and category fields are present
