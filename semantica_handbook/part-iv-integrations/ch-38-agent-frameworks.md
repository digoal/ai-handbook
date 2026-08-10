---
title: Agent Frameworks 集成 — Agno 原生 + 6 家二等
slug: ch-38-agent-frameworks
part: part-iv-integrations
audience: all
reading_time: 10
prerequisites: [ch-21-context-decision, ch-30-mcp-server]
semantica_version: 0.6.0
---

# ch-38 Agent Frameworks 集成 — Agno 原生 + 6 家二等

> Semantica 把 Agno 作为原生一等集成, 其它 6 家 Agent 框架通过 REST + MCP 二等支持。

## 1. 用户视角(User)

### 1.1 我能用它做什么

- **Agno**: 一等公民, 5 个模块 (`context_store / decision_kit / kg_toolkit / knowledge_graph / shared_context`), 装 `pip install semantica[agno]`。
- **OpenClaw**: MCP + REST 双接入 (`mcp_tool.py` + `OpenClawKGTool`)。
- **LangChain / LangGraph / CrewAI / LlamaIndex / AutoGen / OpenAI Agents / Google ADK**: 走 REST API + MCP server, 不需额外依赖。

### 1.2 集成矩阵

| 框架 | 集成方式 | 安装 | 模块 |
|---|---|---|---|
| **Agno** | 原生一等 | `pip install semantica[agno]` | context_store / decision_kit / kg_toolkit / knowledge_graph / shared_context |
| **OpenClaw** | MCP + REST 双接入 | (内置) | mcp_tool / OpenClawKGTool |
| **LangChain** | REST + MCP | (内置) | SemanticaRetriever / SemanticaKnowledgeGraph |
| **LangGraph** | REST + MCP | (内置) | SemanticaState / SemanticaGraph |
| **CrewAI** | REST + MCP | (内置) | SemanticaTool |
| **LlamaIndex** | REST + MCP | (内置) | SemanticaReader |
| **AutoGen** | REST + MCP | (内置) | SemanticaAgent |
| **OpenAI Agents SDK** | MCP | (内置) | (走 MCP 12 tools) |
| **Google ADK** | MCP | (内置) | (走 MCP 12 tools) |

### 1.3 一段最小可跑示例 (Agno 原生)

```python
from agno.agent import Agent
from semantica.integrations.agno import SemanticaKnowledgeGraph, DecisionKit

kg = SemanticaKnowledgeGraph(workspace="acme_credit")
agent = Agent(
    name="credit_analyst",
    tools=[kg.query_tool(), DecisionKit().recommend_tool()],
)
agent.print_response("Acme Corp 申请 100 万美元贷款, 应该批吗?")
```

### 1.4 何时不用

- 你不用任何 Agent 框架 → 直接用 SDK ([ch-12-semantic-extract])。
- 你要用 LangGraph 复杂状态机 → 走 MCP, 但工具 12 个可能不够。

## 2. 开发者视角(Developer)

### 2.1 关键代码路径

- `semantica/integrations/agno/__init__.py` — 5 个 Agno 模块导出。
- `semantica/integrations/agno/context_store.py` — ContextGraph [[ch-55-glossary]] ↔ Agno 状态。
- `semantica/integrations/agno/decision_kit.py` — DecisionKit (决策推荐 / 因果链)。
- `semantica/integrations/agno/kg_toolkit.py` — KG 查询工具。
- `semantica/integrations/agno/knowledge_graph.py` — Agno KnowledgeGraph 适配。
- `semantica/integrations/agno/shared_context.py` — 多 agent 共享 context。
- `semantica/integrations/openclaw/mcp_tool.py` — OpenClaw MCP 接入。
- `semantica/integrations/openclaw/openclaw_kg_tool.py` — OpenClaw KG 工具。
- `semantica/mcp_server/` — 12 MCP tools 给所有支持 MCP 的 Agent 框架。

### 2.2 最小复现脚本 (MCP 模式)

```python
# examples/ch-38-mcp-agent.py mirror
# 任何支持 MCP 的 agent SDK 都可这样调:
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    params = StdioServerParameters(command="semantica-mcp", args=[])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            tools = await session.list_tools()
            print("Available MCP tools:", [t.name for t in tools.tools])

asyncio.run(run())
```

### 2.3 扩展点

- **加新 Agent 原生集成**: 在 `semantica/integrations/` 加 `my_agent/`, 注册到 `pyproject.toml:[agent-*]` extras。
- **加新 MCP 工具**: 见 [ch-30-mcp-server] § 2.4。
- **加 LangChain Retriever**: 在 `semantica/integrations/langchain/` 加 `retriever.py`。

## 3. 架构师视角(Architect)

### 3.1 设计取舍

**为什么 Agno 是原生一等, 其它走 MCP?**
- Agno 是 Semantica 同源团队, 协同紧密。
- 其它框架走 MCP, 让用户按"已有栈"选, 不强行绑定。

**为什么不学 LangChain 做"全 Agent 都 deep 集成"?**
- 维护成本爆炸 (每个框架版本都要跟)。
- MCP 是标准, 一次实现到处用。

### 3.2 与同类对比

| 维度 | Semantica Agent 集成 | LangChain Agent | LlamaIndex Agent |
|---|---|---|---|
| 原生一等 | Agno | ❌ | ❌ |
| MCP 接入 | ✅ | ⚠ | ⚠ |
| 决策图工具 | ✅ | ❌ | ❌ |

### 3.3 何时重新设计

- 出现"Agent 互操作标准" → 切 A2A (Google) / ANP。
- 原生一等 > 3 个 → 维护成本骤增, 全部转 MCP。

## 跨章引用

- 上一章: [[ch-37-data-sources]]
- 下一章: [[ch-39-ide-plugins]]