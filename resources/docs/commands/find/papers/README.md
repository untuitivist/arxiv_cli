# find/papers

Shortcut command for literature discovery from free-text intent plus optional filters.

## 概念说明

- 自由文本搜索，最口语化的方式
- 多个关键词自动用 AND 连接
- 适合快速探索，不用记 arXiv 查询语法

## 示例

### 基础搜索

```powershell
# 自由文本搜索
arxiv find papers graph neural network --max-results 5

# 搜索并指定分类
arxiv find papers graph neural network --category cs.LG --max-results 5

# 按提交日期排序
arxiv find papers graph neural network --category cs.LG --sort-by submittedDate --max-results 5
```

### 量化金融搜索

```powershell
# 搜索价格、成交量相关
arxiv find papers price volume --category q-fin.ST --max-results 8

# 搜索技术分析相关
arxiv find papers technical analysis --category q-fin.ST --max-results 10

# 搜索交易策略相关
arxiv find papers trading strategy --category q-fin.TR --max-results 8

# 搜索因子投资相关
arxiv find papers factor investing --category q-fin.PM --max-results 10
```

### 组合搜索

```powershell
# 搜索特定作者（配合 find 不太好用，推荐用 search query 或 search raw）
arxiv find papers deep learning --author "Yann LeCun" --dry-run
```

### 输出格式和保存

```powershell
# 文本格式输出
arxiv find papers price volume --category q-fin.ST --max-results 5 --format text

# JSON 格式输出
arxiv find papers price volume --category q-fin.ST --max-results 5 --format json

# 保存到文件
arxiv find papers price volume --category q-fin.ST --max-results 10 --output arxiv_find_price_volume.json
```

### 安全预览（dry-run）

```powershell
# 预览查询
arxiv find papers price volume --category q-fin.ST --dry-run
```

## 命令选择建议

- **口语化快速搜索** → 用 `find papers`
- **简单 AND 查询** → 用 `search query`
- **复杂 OR/AND/NOT 查询** → 用 `search raw`
