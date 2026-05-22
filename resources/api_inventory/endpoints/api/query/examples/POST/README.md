# POST /api/query

## Parameter command

```powershell
curl -X POST "https://export.arxiv.org/api/query" -d "search_query=all:electron&start=0&max_results=1"
```

## File IO command

```powershell
Invoke-WebRequest -Method Post -Uri "https://export.arxiv.org/api/query" -Body @{search_query="all:electron"; start="0"; max_results="1"} -OutFile "arxiv_cli/resources/api_inventory/endpoints/api/query/examples/POST/file_output.xml"
```

Note: POST with only URL query parameters returned HTTP 400 during live probing.
