# search/query

Build a structured `search_query` from common arXiv fields.

## 概念说明

- 多个 `--all` 参数是 **AND** 关系：所有关键词都必须同时出现
- 用 `--dry-run` 可以预览请求而不实际执行
- 支持的字段：`--all`、`--title`、`--author`、`--abstract`、`--category` 等

## 示例

### 基础搜索

```powershell
# 搜索所有包含 "graph neural network" 的论文
arxiv search query --all "graph neural network" --max-results 5

# 搜索 cs.LG 分类下的论文
arxiv search query --all "graph neural network" --category cs.LG --max-results 5

# 按提交日期排序
arxiv search query --all "graph neural network" --category cs.LG --sort-by submittedDate --max-results 5
```

### 量化金融相关搜索

```powershell
# 搜索价格、成交量相关的量化金融论文
arxiv search query --all "volume" --all "price" --category q-fin.ST --max-results 10

# 搜索技术指标相关论文
arxiv search query --all "technical indicator" --category q-fin.ST --max-results 8

# 搜索交易因子相关论文
arxiv search query --all "trading" --all "factor" --category q-fin.TR --max-results 10

# 搜索波动率相关论文
arxiv search query --all "volatility" --category q-fin.ST --sort-by relevance --max-results 10
```

### 组合搜索

```powershell
# 按作者和标题搜索
arxiv search query --author "Yann LeCun" --title "convolutional" --sort-by submittedDate

# 搜索包含特定摘要关键词的论文
arxiv search query --abstract "price volume" --category q-fin.ST --max-results 10

# 搜索特定分类并按相关性排序
arxiv search query --all "market microstructure" --category q-fin.ST --sort-by relevance --max-results 8
```

### 输出格式和保存

```powershell
# 输出为文本格式（人类可读）
arxiv search query --all "volume" --all "price" --category q-fin.ST --max-results 5 --format text

# 输出为 JSON 格式（机器可读）
arxiv search query --all "volume" --all "price" --category q-fin.ST --max-results 5 --format json

# 保存结果到文件
arxiv search query --all "volume" --all "price" --category q-fin.ST --max-results 10 --output arxiv_volume_price.json
```

### 安全预览（dry-run）

```powershell
# 预览查询而不实际执行
arxiv search query --all "volume" --all "price" --category q-fin.ST --max-results 5 --dry-run
```

## arXiv 分类参考

常用量化金融分类：
- `q-fin.ST` - Statistical Finance（统计金融）
- `q-fin.TR` - Trading and Market Microstructure（交易和市场微观结构）
- `q-fin.PM` - Portfolio Management（投资组合管理）
- `q-fin.RM` - Risk Management（风险管理）
- `q-fin.CP` - Computational Finance（计算金融）

完整列表：https://arxiv.org/category_taxonomy
