# search/raw

Send a raw arXiv `search_query` string directly.

Examples:

```powershell
arxiv search raw "all:\"diffusion model\" AND cat:cs.CV"
arxiv search raw "au:goodfellow AND cat:cs.LG" --sort-by submittedDate --sort-order descending
```
