# arxiv-cli

English | 简体中文

`arxiv-cli` is an agent-native command line toolkit for working with the public arXiv API and bundled local retrieval documentation.

`arxiv-cli` 是一个面向 Agent 原生设计的命令行工具，用于访问公开的 arXiv API，并结合本地打包文档完成可重复的论文检索工作流。

It is built for coding agents and long-running research agents first, not as a thin human-only wrapper. Commands produce structured JSON, preserve raw API context, support safe request preview with `--dry-run`, and fit naturally into repeatable retrieval workflows: API discovery, endpoint inspection, query execution, paper lookup, shortcut search, and local workflow/doc review.

它优先服务于 coding agent 与长时运行的 research agent，而不是只做一层给人点着用的薄封装。命令默认输出结构化 JSON，保留原始 API 上下文，支持 `--dry-run` 安全预演，并且天然适合可重复的检索流程：API 发现、endpoint 检查、查询执行、论文拉取、快捷检索，以及本地 workflow/doc 复核。

- Repository: [untuitivist/arxiv_cli](https://github.com/untuitivist/arxiv_cli)
- Author: [wiz](https://github.com/untuitivist)
- License: GPL-3.0-only with Commons Clause. See [LICENSE](LICENSE).
- API reference: [arXiv API Access](https://info.arxiv.org/help/api/index.html)

## Agent-Native Design

`arxiv-cli` is designed so an agent can operate it safely and inspectably without browser state, hidden UI steps, or copy-paste glue:

`arxiv-cli` 的设计目标，是让 Agent 在不依赖浏览器状态、隐藏 UI 步骤或复制粘贴胶水代码的前提下，安全且可检查地完成工作：

- Structured command outputs that can be saved with `--output` and consumed by later workflow nodes.
- Commands preserve raw request and response context, including method, URL, params, status code, content type, and parsed Atom payloads.
- Bundled API inventory and command docs let agents inspect the available surface locally before making live calls.
- Resource commands, shortcut commands, and workflow notes are separated, so an agent can choose the right abstraction level.
- `--dry-run` provides a safe preview path for request-building commands before live execution.
- Optional `--format text` views help with quick terminal review, while JSON remains the stable automation format.

- 结构化命令输出可以通过 `--output` 落盘，并交给后续 workflow 节点继续消费。
- 命令保留原始请求与响应上下文，包括 method、URL、params、status code、content type 和解析后的 Atom 结果。
- 打包的 API inventory 与命令文档允许 Agent 在发起 live call 前先在本地检查可用接口面。
- 资源命令、快捷命令和 workflow 文档相互分层，便于 Agent 按合适抽象层工作。
- `--dry-run` 为构造请求类命令提供安全预演路径，再决定是否执行真实请求。
- 可选的 `--format text` 便于快速终端阅读，而 JSON 仍然是稳定的自动化输出格式。

## What This Tool Provides

- API inventory for the public arXiv metadata endpoint.
- Raw API commands for inventory inspection and direct endpoint execution.
- Resource commands for `/api/query`.
- Shortcut commands for literature discovery.
- Bundled command documentation and workflow notes.
- Local config and environment-variable overrides for repeatable execution.

- 面向公开 arXiv 元数据接口的 API inventory。
- 用于 inventory 检查和直接 endpoint 调用的 raw API 命令。
- 针对 `/api/query` 的资源命令层。
- 面向论文发现任务的 shortcut 命令层。
- 打包的命令文档与 workflow 说明。
- 用于可重复执行的本地配置与环境变量覆盖。

## Important Notes

- This project is not affiliated with arXiv.
- Commands call the live public API unless `--dry-run` is used.
- arXiv returns Atom XML; `arxiv-cli` normalizes it into structured JSON for downstream use.
- Machine-local outputs under `local/` are intentionally not committed.
- The license is source-available but not OSI open source because Commons Clause restricts selling the software.

- 本项目与 arXiv 官方无隶属关系。
- 除非显式使用 `--dry-run`，否则命令会调用真实的公开 API。
- arXiv 返回的是 Atom XML；`arxiv-cli` 会把它标准化为结构化 JSON，便于下游消费。
- `local/` 下的机器本地产物按设计不应提交到仓库。
- 当前许可证属于 source-available，不属于 OSI open source，因为 Commons Clause 限制了销售权。

## Requirements

- Python 3.11 or newer.
- Network access to `https://export.arxiv.org/api/query`.
- Windows PowerShell is the primary tested shell.

- Python 3.11 或更新版本。
- 可访问 `https://export.arxiv.org/api/query` 的网络环境。
- 目前主要在 Windows PowerShell 下验证。

## Installation

Clone the repository:

克隆仓库：

```powershell
git clone https://github.com/untuitivist/arxiv_cli.git
cd arxiv_cli
```

Install in editable mode:

以 editable 模式安装：

```powershell
python -m pip install -e .
```

Confirm the CLI is available:

确认 CLI 可用：

```powershell
arxiv --help
arxiv api stats
```

If `arxiv` is not on `PATH`, run commands through Python from the parent directory:

如果 `arxiv` 不在 `PATH` 中，可以从父目录直接通过 Python 运行：

```powershell
python -m arxiv_cli --help
```

Refresh the bundled inventory when probe logic changes or when you want a fresh live snapshot:

当 probe 逻辑变更，或你需要新的 live 快照时，可刷新打包 inventory：

```powershell
python scripts/refresh_api_inventory.py
```

## Package Metadata

The Python distribution name is `arxiv-cli`.

Python 分发名是 `arxiv-cli`。

The import/package name is `arxiv_cli`.

导入包名是 `arxiv_cli`。

The command line entry point is:

命令行入口是：

```powershell
arxiv
```

Current package version:

当前包版本：

```toml
version = "0.2.0"
```

## Local Config

Initialize local config:

初始化本地配置：

```powershell
arxiv config init
```

Inspect or update config:

查看或更新配置：

```powershell
arxiv config show
arxiv config set contact you@example.com
arxiv config get delay_seconds
```

Default config keys:

默认配置字段：

- `base_url`: `https://export.arxiv.org/api/query`
- `tool`: `arxiv-cli`
- `contact`: contact string for user-agent identification
- `delay_seconds`: default request spacing
- `timeout_seconds`: HTTP timeout

- `base_url`: `https://export.arxiv.org/api/query`
- `tool`: `arxiv-cli`
- `contact`: 用于 user-agent 标识的联系字符串
- `delay_seconds`: 默认请求间隔
- `timeout_seconds`: HTTP 超时

Supported environment overrides:

支持的环境变量覆盖：

- `ARXIV_CLI_BASE_URL`
- `ARXIV_CLI_TOOL`
- `ARXIV_CLI_CONTACT`
- `ARXIV_CLI_DELAY_SECONDS`
- `ARXIV_CLI_TIMEOUT_SECONDS`

## Repository Layout

```text
.
  cli.py
  commands/                 CLI command groups
  core/                     HTTP, config, registry, parsing, output helpers
  resources/
    api_inventory/          Bundled API endpoint inventory and probe artifacts
    docs/
      commands/             Handwritten command docs and examples
      generated/            Generated command references
  workflow/                 Retrieval workflow node documents
  tests/                    Test suite
  local/                    User-local runtime data, ignored by Git
  scripts/                  Maintenance scripts such as inventory refresh
  LICENSE
  pyproject.toml
  README.md
```

## Common Commands

Inspect the bundled API inventory:

查看本地打包的 API inventory：

```powershell
arxiv api stats
arxiv api list
arxiv api show /api/query
arxiv api params /api/query
```

Preview or call the raw endpoint:

预演或调用原始 endpoint：

```powershell
arxiv api call GET /api/query --param search_query=all:electron --param max_results=1 --dry-run
arxiv api call GET /api/query --param search_query=all:electron --param max_results=1
```

Use the resource command layer:

使用资源命令层：

```powershell
arxiv query run --search-query "all:\"graph neural network\"" --max-results 5
arxiv query run --id 1706.03762 --id 2401.10401 --dry-run --format text
```

Use the shortcut search layer:

使用 shortcut 检索层：

```powershell
arxiv find papers graph neural network --category cs.LG --max-results 5 --format text
```

Use the fielded search layer:

使用字段化检索层：

```powershell
arxiv search query --all "graph neural network" --category cs.LG --max-results 5
arxiv search raw "au:\"Yann LeCun\" AND cat:cs.LG" --sort-by submittedDate
```

Fetch exact arXiv ids:

按 arXiv id 精确拉取：

```powershell
arxiv paper get 1706.03762 2401.10401
```

Inspect local docs and workflow notes:

查看本地文档与 workflow 说明：

```powershell
arxiv docs list
arxiv docs show query/run
arxiv workflow list --format text
arxiv workflow show graph
```

When in doubt, check command help:

拿不准时，先看命令帮助：

```powershell
arxiv api call --help
arxiv query run --help
arxiv find papers --help
arxiv search query --help
```

## Agent Workflow Layers

`arxiv-cli` follows a 9-layer agent-native architecture:

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

In practice:

在实际使用中：

- start with `api` when you need exact endpoint truth
- use `query` when you want endpoint-native arguments
- use `search` when you want structured field composition
- use `find` when you want an intent-level retrieval shortcut
- use `workflow` and `docs` when an agent needs local task guidance

- 需要精确 endpoint 真相时，从 `api` 开始
- 需要 endpoint 原生参数时，用 `query`
- 需要字段化组合检索时，用 `search`
- 需要意图级检索快捷入口时，用 `find`
- Agent 需要本地任务说明时，用 `workflow` 和 `docs`

## API Inventory

Bundled endpoint inventory lives in:

打包的 endpoint inventory 位于：

```text
resources/api_inventory/
```

Key files:

关键文件：

- `resources/api_inventory/api_inventory.json`
- `resources/api_inventory/api_inventory_complete.json`
- `resources/api_inventory/endpoints/api/query/endpoint.json`
- `resources/api_inventory/reports/endpoint_test_results.md`

## Command Documentation

Bundled command documentation lives in:

打包的命令文档位于：

```text
resources/docs/commands/
```

Useful entry points:

常用入口：

- `resources/docs/commands/README.md`
- `resources/docs/commands/api/README.md`
- `resources/docs/commands/query/run/README.md`
- `resources/docs/commands/find/papers/README.md`
- `resources/docs/commands/search/query/README.md`
- `resources/docs/commands/workflow/README.md`

## Workflow Documents

The structured retrieval workflow is documented under:

结构化检索 workflow 文档位于：

```text
workflow/
```

The main graph is:

主图为：

```text
workflow/workflow_graph.md
```

Nodes currently cover:

当前节点覆盖：

- config and rate limit
- search and ranking
- fetch by id or query
- local doc review

- 配置与速率限制
- 检索与排序
- 按 id 或 query 拉取
- 本地文档复核

## Development

Install editable package:

安装 editable 包：

```powershell
python -m pip install -e .
```

Run tests from the repository root:

在仓库根目录运行测试：

```powershell
python -m pytest tests -q
```

Build package artifacts:

构建发布产物：

```powershell
python -m build
```

Do not commit:

不要提交：

- `local/`
- `dist/`
- `build/`
- `*.egg-info/`
- machine-local query outputs or state files

- `local/`
- `dist/`
- `build/`
- `*.egg-info/`
- 机器本地查询产物或状态文件

## Troubleshooting

### `ModuleNotFoundError: No module named 'arxiv_cli'`

Install editable mode again:

重新安装 editable 模式：

```powershell
python -m pip install -e .
```

Or run from the parent directory:

或者从父目录运行：

```powershell
python -m arxiv_cli --help
```

### `wqb`-style build warnings about ignored packages

`python -m build` currently succeeds, but setuptools still emits package-discovery warnings because this project uses a flat package layout plus bundled resource/workflow directories.

当前 `python -m build` 可以成功，但 setuptools 仍会输出 package discovery warning。根因是当前项目采用平铺式包布局，同时又打包了 `resources/` 与 `workflow/` 目录。

These warnings do not currently block use or packaging, but they indicate that a future packaging cleanup should move the project toward a more standard package/data split.

这些 warning 当前不会阻止使用或打包，但说明后续如果要继续清理发布面，最好把代码包与资源目录进一步做标准化拆分。

## Release

Current release target:

当前发布目标：

```toml
version = "0.2.0"
```

Release checklist:

发布检查清单：

1. Update `version` in `pyproject.toml`.
2. Run editable install.
3. Run tests.
4. Run `python -m build`.
5. Commit changes.
6. Tag the release, for example `v0.2.0`.
7. Push the branch and tag.
8. Publish a GitHub Release.

1. 更新 `pyproject.toml` 中的 `version`。
2. 执行 editable install。
3. 运行测试。
4. 运行 `python -m build`。
5. 提交改动。
6. 打 tag，例如 `v0.2.0`。
7. 推送分支和 tag。
8. 发布 GitHub Release。

## License

This project is licensed under GPL-3.0-only with the Commons Clause License Condition v1.0.

本项目使用 GPL-3.0-only with the Commons Clause License Condition v1.0。

Required attribution:

要求保留的署名：

```text
Original author: wiz
Original repository: https://github.com/untuitivist/arxiv_cli
Author GitHub: https://github.com/untuitivist
```

The Commons Clause removes the right to sell the software as defined in [LICENSE](LICENSE). This means the source is available, but the project is not OSI open source.

Commons Clause 按 [LICENSE](LICENSE) 的定义移除了销售该软件的权利。这意味着源码可见，但该项目不属于 OSI open source。
