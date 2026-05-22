# B 检索查询

## Goal

Construct reproducible search queries against the arXiv metadata API.

## Inputs

- fielded search terms
- paging options
- sorting options

## Commands

```powershell
arxiv search query --all "diffusion model" --category cs.LG --max-results 10
arxiv search raw "cat:cs.LG AND abs:\"reasoning\"" --sort-by submittedDate
```

## Success Criteria

- response contains `ok: true`
- `request.url` is preserved
- `entries` is non-empty when matches exist
