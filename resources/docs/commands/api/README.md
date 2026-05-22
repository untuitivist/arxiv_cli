# api

Inspect and call endpoints from the bundled `resources/api_inventory`.

Examples:

```powershell
arxiv api stats
arxiv api list
arxiv api show /api/query
arxiv api params /api/query
arxiv api call GET /api/query --param search_query=all:electron --param start=0 --param max_results=1
arxiv api call POST /api/query --data search_query=all:electron --data start=0 --data max_results=1
```
