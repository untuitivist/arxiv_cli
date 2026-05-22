# GET /api/query

## Parameter command

```powershell
curl "https://export.arxiv.org/api/query?search_query=all%3Aelectron&start=0&max_results=1"
```

## File IO command

```powershell
Invoke-WebRequest -Uri "https://export.arxiv.org/api/query?search_query=all%3Aelectron&start=0&max_results=1" -OutFile "resources/api_inventory/endpoints/api/query/examples/GET/file_output.xml"
```
