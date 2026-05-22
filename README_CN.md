# arxiv-cli

[English](README.md) | 简体中文

`arxiv-cli` 是一个面向 Agent 原生设计的命令行工具，用于访问公开的 arXiv API，并结合本地打包文档完成可重复的论文检索工作流。

它优先服务于 coding agent 与长时运行的 research agent，而不是只做一层给人点着用的薄封装。命令默认输出结构化 JSON，保留原始 API 上下文，支持 `--dry-run` 安全预演，并且天然适合可重复的检索流程：API 发现、endpoint 检查、查询执行、论文拉取、快捷检索，以及本地 workflow/doc 复核。

- 仓库: [untuitivist/arxiv_cli](https://github.com/untuitivist/arxiv_cli)
- 作者: [wiz](https://github.com/untuitivist)
- 许可证: GPL-3.0-only with Commons Clause。详见 [LICENSE](LICENSE)。
- API 参考: [arXiv API Access](https://info.arxiv.org/help/api/index.html)

## Agent 原生设计

`arxiv-cli` 的设计目标，是让 Agent 在不依赖浏览器状态、隐藏 UI 步骤或复制粘贴胶水代码的前提下，安全且可检查地完成工作：

- 结构化命令输出可以通过 `--output` 落盘，并交给后续 workflow 节点继续消费。
- 命令保留原始请求与响应上下文，包括 method、URL、params、status code、content type 和解析后的 Atom 结果。
- 打包的 API inventory 与命令文档允许 Agent 在发起 live call 前先在本地检查可用接口面。
- 资源命令、快捷命令和 workflow 文档相互分层，便于 Agent 按合适抽象层工作。
- `--dry-run` 为构造请求类命令提供安全预演路径，再决定是否执行真实请求。
- 可选的 `--format text` 便于快速终端阅读，而 JSON 仍然是稳定的自动化输出格式。

## 功能概览

- 面向公开 arXiv 元数据接口的 API inventory。
- 用于 inventory 检查和直接 endpoint 调用的 raw API 命令。
- 针对 `/api/query` 的资源命令层。
- 面向论文发现任务的 shortcut 命令层。
- 打包的命令文档与 workflow 说明。
- 用于可重复执行的本地配置与环境变量覆盖。

## 重要说明

- 本项目与 arXiv 官方无隶属关系。
- 除非显式使用 `--dry-run`，否则命令会调用真实的公开 API。
- arXiv 返回的是 Atom XML；`arxiv-cli` 会把它标准化为结构化 JSON，便于下游消费。
- `local/` 下的机器本地产物按设计不应提交到仓库。
- 当前许可证属于 source-available，不属于 OSI open source，因为 Commons Clause 限制了销售权。

## 环境要求

- Python 3.11 或更新版本。
- 可访问 `https://export.arxiv.org/api/query` 的网络环境。
- 目前主要在 Windows PowerShell 下验证。

## 安装

克隆仓库：

```powershell
git clone https://github.com/untuitivist/arxiv_cli.git
cd arxiv_cli
```

以 editable 模式安装：

```powershell
python -m pip install -e .
```

确认 CLI 可用：

```powershell
arxiv --help
arxiv api stats
```

如果 `arxiv` 不在 `PATH` 中，可以从父目录直接通过 Python 运行：

```powershell
python -m arxiv_cli --help
```

当 probe 逻辑变更，或你需要新的 live 快照时，可刷新打包 inventory：

```powershell
python scripts/refresh_api_inventory.py
```

## 包元信息

Python 分发名是 `arxiv-cli`。

导入包名是 `arxiv_cli`。

命令行入口是：

```powershell
arxiv
```

当前包版本：

```toml
version = "0.2.0"
```

## 本地配置

初始化本地配置：

```powershell
arxiv config init
```

查看或更新配置：

```powershell
arxiv config show
arxiv config set contact you@example.com
arxiv config get delay_seconds
```

默认配置字段：

- `base_url`: `https://export.arxiv.org/api/query`
- `tool`: `arxiv-cli`
- `contact`: 用于 user-agent 标识的联系字符串
- `delay_seconds`: 默认请求间隔
- `timeout_seconds`: HTTP 超时

支持的环境变量覆盖：

- `ARXIV_CLI_BASE_URL`
- `ARXIV_CLI_TOOL`
- `ARXIV_CLI_CONTACT`
- `ARXIV_CLI_DELAY_SECONDS`
- `ARXIV_CLI_TIMEOUT_SECONDS`

## 仓库结构

```text
.
  cli.py
  commands/                 CLI 命令分组
  core/                     HTTP、配置、registry、解析、输出辅助
  resources/
    api_inventory/          打包的 API endpoint inventory 与探测产物
    docs/
      commands/             手写命令文档与示例
      generated/            生成的命令参考
  workflow/                 检索工作流节点文档
  tests/                    测试套件
  local/                    用户本地运行时数据，Git 忽略
  scripts/                  维护脚本，如 inventory 刷新
  LICENSE
  pyproject.toml
  README.md
  README_CN.md
```

## 常用命令

查看本地打包的 API inventory：

```powershell
arxiv api stats
arxiv api list
arxiv api show /api/query
arxiv api params /api/query
```

预演或调用原始 endpoint：

```powershell
arxiv api call GET /api/query --param search_query=all:electron --param max_results=1 --dry-run
arxiv api call GET /api/query --param search_query=all:electron --param max_results=1
```

使用资源命令层：

```powershell
arxiv query run --search-query "all:\"graph neural network\"" --max-results 5
arxiv query run --id 1706.03762 --id 2401.10401 --dry-run --format text
```

使用 shortcut 检索层：

```powershell
arxiv find papers graph neural network --category cs.LG --max-results 5 --format text
```

使用字段化检索层：

```powershell
arxiv search query --all "graph neural network" --category cs.LG --max-results 5
arxiv search raw "au:\"Yann LeCun\" AND cat:cs.LG" --sort-by submittedDate
```

按 arXiv id 精确拉取：

```powershell
arxiv paper get 1706.03762 2401.10401
```

查看本地文档与 workflow 说明：

```powershell
arxiv docs list
arxiv docs show query/run
arxiv workflow list --format text
arxiv workflow show graph
```

拿不准时，先看命令帮助：

```powershell
arxiv api call --help
arxiv query run --help
arxiv find papers --help
arxiv search query --help
```

## Agent 工作流层级

`arxiv-cli` 遵循一个 9 层的 Agent-native 架构：

1. `inventory`
2. `raw api`
3. `resource command`
4. `shortcut`
5. `workflow`
6. `safety`
7. `output`
8. `auth/config`
9. `release`

在实际使用中：

- 需要精确 endpoint 真相时，从 `api` 开始
- 需要 endpoint 原生参数时，用 `query`
- 需要字段化组合检索时，用 `search`
- 需要意图级检索快捷入口时，用 `find`
- Agent 需要本地任务说明时，用 `workflow` 和 `docs`

## API Inventory

打包的 endpoint inventory 位于：

```text
resources/api_inventory/
```

关键文件：

- `resources/api_inventory/api_inventory.json`
- `resources/api_inventory/api_inventory_complete.json`
- `resources/api_inventory/endpoints/api/query/endpoint.json`
- `resources/api_inventory/reports/endpoint_test_results.md`

## 命令文档

打包的命令文档位于：

```text
resources/docs/commands/
```

常用入口：

- `resources/docs/commands/README.md`
- `resources/docs/commands/api/README.md`
- `resources/docs/commands/query/run/README.md`
- `resources/docs/commands/find/papers/README.md`
- `resources/docs/commands/search/query/README.md`
- `resources/docs/commands/workflow/README.md`

## 工作流文档

结构化检索 workflow 文档位于：

```text
workflow/
```

主图为：

```text
workflow/workflow_graph.md
```

当前节点覆盖：

- 配置与速率限制
- 检索与排序
- 按 id 或 query 拉取
- 本地文档复核

## 开发

安装 editable 包：

```powershell
python -m pip install -e .
```

在仓库根目录运行测试：

```powershell
python -m pytest tests -q
```

构建发布产物：

```powershell
python -m build
```

不要提交：

- `local/`
- `dist/`
- `build/`
- `*.egg-info/`
- 机器本地查询产物或状态文件

## 常见问题

### `ModuleNotFoundError: No module named 'arxiv_cli'`

重新安装 editable 模式：

```powershell
python -m pip install -e .
```

或者从父目录运行：

```powershell
python -m arxiv_cli --help
```

### 类似 `wqb` 的构建警告

`python -m build` 当前可以成功，但 setuptools 仍会输出 package discovery warning。根因是当前项目采用平铺式包布局，同时又打包了 `resources/` 与 `workflow/` 目录。

这些 warning 当前不会阻止使用或打包，但说明后续如果要继续清理发布面，最好把代码包与资源目录进一步做标准化拆分。

## 发布

当前发布目标：

```toml
version = "0.2.0"
```

发布检查清单：

1. 更新 `pyproject.toml` 中的 `version`。
2. 执行 editable install。
3. 运行测试。
4. 运行 `python -m build`。
5. 提交改动。
6. 打 tag，例如 `v0.2.0`。
7. 推送分支和 tag。
8. 发布 GitHub Release。

## 许可证

本项目使用 GPL-3.0-only with the Commons Clause License Condition v1.0。

要求保留的署名：

```text
Original author: wiz
Original repository: https://github.com/untuitivist/arxiv_cli
Author GitHub: https://github.com/untuitivist
```

Commons Clause 按 [LICENSE](LICENSE) 的定义移除了销售该软件的权利。这意味着源码可见，但该项目不属于 OSI open source。
