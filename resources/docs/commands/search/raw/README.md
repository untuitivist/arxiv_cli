# search/raw

Send a raw arXiv `search_query` string directly.

## 概念说明

- 直接使用 arXiv API 的 `search_query` 语法
- 支持完整的 AND/OR/NOT 逻辑
- 适合复杂查询，与直接用 `arxiv api call` 完全等价
- 查询语法参考：https://arxiv.org/help/api/user-manual#531-search-query

## arXiv 查询语法

常用字段前缀：
- `all:` - 搜索所有字段
- `ti:` - 只搜索标题
- `au:` - 只搜索作者
- `abs:` - 只搜索摘要
- `cat:` - 分类
- `id_list:` - arXiv ID 列表

逻辑操作符：
- `AND` - 同时满足
- `OR` - 满足任一即可
- `NOT` - 排除
- `(...)` - 分组

## 示例

### 基础搜索

```powershell
# 搜索所有包含 "diffusion model" 的论文
arxiv search raw "all:\"diffusion model\""

# 搜索 cs.CV 分类下的论文
arxiv search raw "all:\"diffusion model\" AND cat:cs.CV"

# 按提交日期排序
arxiv search raw "all:\"diffusion model\" AND cat:cs.CV" --sort-by submittedDate
```

### 量化金融相关搜索（OR 逻辑）

```powershell
# 搜索包含 volume price OR technical indicator OR trading factor 的论文
arxiv search raw "cat:q-fin.ST AND (all:\"volume price\" OR all:\"technical indicator\" OR all:\"trading factor\")" --max-results 10 --format text

# 搜索市场微观结构相关论文
arxiv search raw "cat:q-fin.TR AND (all:\"market microstructure\" OR all:\"price impact\")" --max-results 8

# 搜索技术分析相关论文
arxiv search raw "cat:q-fin.ST AND (all:\"technical analysis\" OR all:\"technical indicator\" OR all:\"trading rule\")" --max-results 10
```

### 复杂查询

```powershell
# 搜索特定作者的论文
arxiv search raw "au:goodfellow AND cat:cs.LG" --sort-by submittedDate --sort-order descending --max-results 5

# 搜索特定标题关键词
arxiv search raw "ti:\"volume\" AND ti:\"price\" AND cat:q-fin.ST" --max-results 8

# 搜索特定摘要关键词
arxiv search raw "abs:\"price volume\" AND cat:q-fin.ST" --max-results 10
```

### 多个分类组合

```powershell
# 搜索 q-fin.ST 或 q-fin.TR 分类下的论文
arxiv search raw "(cat:q-fin.ST OR cat:q-fin.TR) AND all:\"trading factor\"" --max-results 10

# 排除某些特定分类
arxiv search raw "cat:q-fin.ST AND NOT all:\"cryptocurrency\"" --max-results 10
```

### 输出格式和保存

```powershell
# 输出为文本格式
arxiv search raw "cat:q-fin.ST AND (all:\"volume price\" OR all:\"technical indicator\")" --max-results 6 --format text

# 输出为 JSON 格式
arxiv search raw "cat:q-fin.ST AND (all:\"volume price\" OR all:\"technical indicator\")" --max-results 6 --format json

# 保存结果到文件
arxiv search raw "cat:q-fin.ST AND (all:\"volume price\" OR all:\"technical indicator\")" --max-results 10 --output arxiv_complex_query.json
```

### 安全预览（dry-run）

```powershell
# 预览查询而不实际执行
arxiv search raw "cat:q-fin.ST AND (all:\"volume price\" OR all:\"technical indicator\")" --dry-run
```

## 实用技巧

1. **当需要 OR 逻辑时用 `search raw`
2. **精确短语搜索用双引号
3. **用 `--dry-run` 预览查询构造
4. **复杂查询推荐用 `search raw`
5. **简单 AND 查询用 `search query`
