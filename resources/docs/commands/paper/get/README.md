# paper/get

Fetch one or more arXiv records by id.

## 概念说明

- 通过 arXiv ID 精确获取一篇或多篇论文
- arXiv ID 格式：`2501.01234` 或 `hep-th/9901001`（旧格式）

## 示例

### 基础获取

```powershell
# 获取单篇论文
arxiv paper get 2501.01234

# 获取多篇论文
arxiv paper get 2501.01234 2407.12345 2305.67890
```

### 量化金融相关示例

```powershell
# 获取经典因子论文（示例 ID）
arxiv paper get 1410.5513

# 获取多篇相关论文
arxiv paper get 1410.5513 2308.08554 1201.5448
```

### 输出格式和保存

```powershell
# 文本格式输出（人类可读）
arxiv paper get 2501.01234 --format text

# JSON 格式输出（机器可读）
arxiv paper get 2501.01234 --format json

# 保存到文件
arxiv paper get 2501.01234 2407.12345 --output arxiv_papers.json
```

## 实用技巧

1. **先搜索找到感兴趣的论文**（用 `search query` 或 `search raw` 或 `find papers`）
2. **获取 arXiv ID**（从搜索结果的 `id` 字段，形如 `http://arxiv.org/abs/2501.01234`）
3. **用 `paper get` 精确获取完整元数据**

## 真实示例

```powershell
# 假设搜索到了这篇论文，ID 是 1410.5513
arxiv paper get 1410.5513 --format text

# 保存到文件
arxiv paper get 1410.5513 --output paper_1410.5513.json
```
