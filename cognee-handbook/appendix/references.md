# 参考文献与外部资源

> 本附录汇总《Cognee 记忆工程》中引用或用于复现实验的论文、官方文档、代码仓库与工具。链接按公开页面整理，并于 2026-07-26 抽查验证；项目版本以 Cognee v1.4.0 为本书基线。章节编号采用全书 Ch01–Ch30 的约定。
>
> **使用说明**：代码仓库、软件包和在线文档会持续更新。读者复现实验时，应同时查看项目的版本标签、迁移说明和许可协议；“引用章节”表示该资源在正文中出现、用于解释概念，或被示例作为可选后端/集成使用。

## A. 学术论文

### A.1 Cognee 核心论文

- **Markovic et al. (2025)**, *Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning*，arXiv:2505.24478。
  - 核心贡献：提出 ECL（Explicit Context Layer）范式，并以 BEAM 评测长上下文知识检索；讨论知识图谱与 LLM 之间的接口设计。
  - 引用章节：Ch01、Ch04、Ch26。
  - 链接：[arXiv 摘要页](https://arxiv.org/abs/2505.24478)

### A.2 BEAM Benchmark

- **BEAM Benchmark**，论文配套的长上下文检索评测资料。
  - 用途：比较上下文窗口、图结构检索和精确知识回答的效果；本书将其作为理解 Cognee 评估思路的入口，而非声称所有实验均直接复现原始数字。
  - 引用章节：Ch04、Ch26。
  - 链接：[arXiv:2505.24478](https://arxiv.org/abs/2505.24478)

### A.3 检索增强生成

- **Lewis et al. (2020)**, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*，arXiv:2005.11401，DOI:10.48550/arXiv.2005.11401。
  - 核心贡献：将参数化语言模型与外部非参数化记忆结合，为 RAG 奠定通用框架。
  - 引用章节：Ch02、Ch04、Ch05、Ch25。
  - 链接：[arXiv](https://arxiv.org/abs/2005.11401)

- **Gao et al. (2023)**, *Retrieval-Augmented Generation for Large Language Models: A Survey*，arXiv:2312.10997。
  - 用途：梳理检索器、生成器、索引、查询重写和评估方法；用于区分向量 RAG 与图增强检索。
  - 引用章节：Ch04、Ch05、Ch26。
  - 链接：[arXiv](https://arxiv.org/abs/2312.10997)

### A.4 向量表示与语义检索

- **Reimers & Gurevych (2019)**, *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*，arXiv:1908.10084，DOI:10.18653/v1/D19-1410。
  - 核心贡献：提出适合语义相似度和检索的句向量训练方法。
  - 引用章节：Ch04、Ch09、Ch12。
  - 链接：[arXiv](https://arxiv.org/abs/1908.10084)

- **Karpukhin et al. (2020)**, *Dense Passage Retrieval for Open-Domain Question Answering*，arXiv:2004.04906，DOI:10.18653/v1/2020.emnlp-main.550。
  - 用途：说明双编码器密集检索、正负样本与召回率之间的关系。
  - 引用章节：Ch04、Ch12、Ch26。
  - 链接：[arXiv](https://arxiv.org/abs/2004.04906)

- **Wang et al. (2020)**, *MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers*，arXiv:2002.10957。
  - 用途：理解轻量嵌入与本地推理的取舍。
  - 引用章节：Ch11、Ch12、Ch27。
  - 链接：[arXiv](https://arxiv.org/abs/2002.10957)

### A.5 知识图谱与图检索

- **Hogan et al. (2021)**, *Knowledge Graphs*，ACM Computing Surveys 54(4)，DOI:10.1145/3447772。
  - 核心贡献：系统介绍实体、关系、模式、链接预测和图谱构建。
  - 引用章节：Ch01、Ch03、Ch06、Ch10。
  - 链接：[DOI](https://doi.org/10.1145/3447772)

- **Bordes et al. (2013)**, *Translating Embeddings for Modeling Multi-relational Data*，NeurIPS 2013。
  - 用途：作为知识图谱嵌入与关系建模的经典背景。
  - 引用章节：Ch06、Ch12。
  - 链接：[NeurIPS 论文页](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)

- **Edge et al. (2024)**, *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*，arXiv:2404.16130。
  - 用途：说明图结构如何辅助全局主题发现、社区摘要与多跳问题回答。
  - 引用章节：Ch05、Ch06、Ch25、Ch26。
  - 链接：[arXiv](https://arxiv.org/abs/2404.16130)

### A.6 Agent 记忆与上下文

- **Park et al. (2023)**, *Generative Agents: Interactive Simulacra of Human Behavior*，arXiv:2304.03442，DOI:10.48550/arXiv.2304.03442。
  - 核心贡献：以记忆流、反思和规划构造可交互的生成式代理。
  - 引用章节：Ch02、Ch05、Ch15、Ch25。
  - 链接：[arXiv](https://arxiv.org/abs/2304.03442)

- **Packer et al. (2023)**, *MemGPT: Towards LLMs as Operating Systems*，arXiv:2310.08560。
  - 用途：讨论主上下文与外部记忆分层、分页和上下文管理。
  - 引用章节：Ch02、Ch05、Ch25。
  - 链接：[arXiv](https://arxiv.org/abs/2310.08560)

- **Yao et al. (2023)**, *ReAct: Synergizing Reasoning and Acting in Language Models*，arXiv:2210.03629，DOI:10.48550/arXiv.2210.03629。
  - 用途：解释代理如何在思考、工具调用和观察之间循环，并将记忆检索作为工具步骤。
  - 引用章节：Ch07、Ch15、Ch20。
  - 链接：[arXiv](https://arxiv.org/abs/2210.03629)

## B. Cognee 官方仓库

### B.1 主仓库

- **cognee**（`topoteretes/cognee`）。
  - 主页：[GitHub](https://github.com/topoteretes/cognee)
  - 版本基线：v1.4.0；实际部署应锁定相应 tag 或 commit。
  - 内容：记忆管道、数据摄取、分块、概念抽取、图谱构建、向量检索、搜索 API、任务编排和配置系统。
  - 引用章节：全部 30 章（Ch01–Ch30）。

- **Cognee 文档站**。
  - 链接：[docs.cognee.ai](https://docs.cognee.ai/)
  - 用途：安装、快速开始、数据集成、搜索模式、配置和部署说明。
  - 引用章节：Ch01、Ch02、Ch08、Ch09、Ch10、Ch14、Ch27、Ch30。

- **Cognee PyPI 包**。
  - 链接：[pypi.org/project/cognee](https://pypi.org/project/cognee/)
  - 用途：核对发布版本、Python 依赖与安装命令。
  - 引用章节：Ch02、Ch08、Ch27。

### B.2 集成仓库

- **cognee-integrations**（`topoteretes/cognee-integrations`）。
  - 链接：[GitHub](https://github.com/topoteretes/cognee-integrations)
  - 内容：面向代理、聊天平台、开发工具、低代码平台和运行时的集成示例；仓库内容会随版本变化，本书按 v1.4.0 时的 24 类集成组织说明。
  - 引用章节：Ch19–Ch23。

### B.3 子项目与协议适配

- **Cognee MCP 适配**。
  - 入口：[Cognee GitHub 搜索](https://github.com/topoteretes/cognee/search?q=mcp&type=code)
  - 用途：将记忆搜索和写入能力暴露为 MCP 工具，供支持 MCP 的客户端调用。
  - 引用章节：Ch20、Ch21。

- **LadybugDB**（`topoteretes/ladybug`）。
  - 链接：[GitHub](https://github.com/topoteretes/ladybug)（2026-07 核验：该公开路径暂不可访问，请以正文给出的仓库所有者与 tag 为准）
  - 用途：Cognee 默认图存储方向之一；其 API 与 Kuzu 生态存在历史关联。
  - 引用章节：Ch06、Ch10、Ch27。

## C. 存储与基础设施

### C.1 向量数据库

- **LanceDB**（默认向量后端之一）。[GitHub](https://github.com/lancedb/lancedb)；[文档](https://lancedb.com/docs/)。
  - 特点：嵌入式、基于 Lance 列式格式，适合本地开发和单机检索。
  - 引用章节：Ch10、Ch27。

- **pgvector**。[GitHub](https://github.com/pgvector/pgvector)；[PostgreSQL 扩展文档](https://github.com/pgvector/pgvector#readme)。
  - 特点：在 PostgreSQL 中保存向量并使用精确或近似最近邻索引。
  - 引用章节：Ch10、Ch27。

- **Qdrant**。[GitHub](https://github.com/qdrant/qdrant)；[文档](https://qdrant.tech/documentation/)。引用章节：Ch10。
- **Weaviate**。[GitHub](https://github.com/weaviate/weaviate)；[文档](https://weaviate.io/developers/weaviate)。引用章节：Ch10。
- **Chroma**。[GitHub](https://github.com/chroma-core/chroma)；[文档](https://docs.trychroma.com/)。引用章节：Ch10。
- **Milvus**。[GitHub](https://github.com/milvus-io/milvus)；[文档](https://milvus.io/docs)。引用章节：Ch10。

这些后端用于比较部署形态、索引类型、过滤能力、持久化方式和运维成本；它们不是同时必需的依赖，具体可用性取决于 Cognee 适配器和版本。

### C.2 图数据库

- **Ladybug**（Cognee 默认方向，原 Kuzu 生态的延续项目）。[GitHub](https://github.com/topoteretes/ladybug)（2026-07 核验：该公开路径暂不可访问）。引用章节：Ch06、Ch10、Ch27。
- **Kuzu**。[GitHub](https://github.com/kuzudb/kuzu)；[文档](https://docs.kuzudb.com/)。引用章节：Ch06、Ch10。
- **Neo4j**。[GitHub](https://github.com/neo4j/neo4j)；[开发者文档](https://neo4j.com/docs/)。引用章节：Ch06、Ch10、Ch27。

### C.3 关系数据库

- **SQLite**（默认关系存储）。[官网](https://sqlite.org/)；[Python 接口](https://docs.python.org/3/library/sqlite3.html)。引用章节：Ch08、Ch10、Ch27。
- **PostgreSQL**。[官网](https://www.postgresql.org/)；[官方文档](https://www.postgresql.org/docs/)。引用章节：Ch10、Ch27、Ch29。
- **SQLAlchemy**。[官网](https://www.sqlalchemy.org/)；[文档](https://docs.sqlalchemy.org/)。用于理解连接、方言和 ORM/SQL 层边界。引用章节：Ch08、Ch10、Ch27。

## D. LLM Provider 与嵌入模型

### D.1 LLM 与本地推理

- **OpenAI API**：[平台文档](https://platform.openai.com/docs)。引用章节：Ch02、Ch08、Ch11、Ch27。
- **Anthropic Claude API**：[文档](https://docs.anthropic.com/)。引用章节：Ch02、Ch11、Ch20。
- **Google Gemini API**：[Google AI for Developers](https://ai.google.dev/)。引用章节：Ch21、Ch27。
- **Ollama**：[官网](https://ollama.com/)；[GitHub](https://github.com/ollama/ollama)。本地模型运行和开发测试。引用章节：Ch02、Ch11、Ch27。
- **vLLM**：[GitHub](https://github.com/vllm-project/vllm)；[文档](https://docs.vllm.ai/)。服务化本地/私有模型推理。引用章节：Ch11、Ch27、Ch29。
- **LiteLLM**：[GitHub](https://github.com/BerriAI/litellm)；[文档](https://docs.litellm.ai/)。用于多 Provider 统一调用的对照方案。引用章节：Ch11、Ch27。

### D.2 嵌入模型

- **OpenAI Embeddings**：`text-embedding-3-small`、`text-embedding-3-large`，见 [Embeddings 指南](https://platform.openai.com/docs/guides/embeddings)。引用章节：Ch09、Ch12、Ch27。
- **Sentence-Transformers**：[sbert.net](https://sbert.net/)；[GitHub](https://github.com/UKPLab/sentence-transformers)。引用章节：Ch09、Ch12、Ch27。
- **BGE / FlagEmbedding**：[GitHub](https://github.com/FlagOpen/FlagEmbedding)。引用章节：Ch09、Ch12、Ch27。
- **Cohere Embed**：[Embedding 文档](https://docs.cohere.com/docs/embeddings)。引用章节：Ch09、Ch12。

选择嵌入模型时需保持维度、距离函数、语言覆盖和索引配置一致；切换模型通常意味着重建向量索引，而不是只替换一个环境变量。

## E. 集成框架

### E.1 Anthropic

- **Claude Code**：[官方文档](https://docs.claude.com/en/docs/claude-code)。引用章节：Ch20、Ch23。
- **Claude Agent SDK**：[概览](https://docs.claude.com/en/api/agent-sdk/overview)。引用章节：Ch20、Ch21。
- **Model Context Protocol SDK**：[GitHub 组织](https://github.com/modelcontextprotocol)。引用章节：Ch20、Ch21。

### E.2 Agent 框架

- **Strands Agents**：[官网](https://strandsagents.com/)。引用章节：Ch21。
- **LangGraph**：[文档](https://langchain-ai.github.io/langgraph/)。引用章节：Ch21、Ch25。
- **CrewAI**：[文档](https://docs.crewai.com/)。引用章节：Ch21。
- **Google ADK**：[文档](https://google.github.io/adk-docs/)。引用章节：Ch21。
- **LangChain**：[官网](https://www.langchain.com/)；[Python 文档](https://python.langchain.com/docs/)。作为编排和记忆抽象的对照。引用章节：Ch05、Ch21、Ch25。

### E.3 聊天工具

- **Telegram Bot API**：[官方 API](https://core.telegram.org/bots/api)。引用章节：Ch22。
- **Slack API 与 Socket Mode**：[Slack API](https://api.slack.com/)；[Socket Mode](https://api.slack.com/apis/events-api/using-socket-mode)。引用章节：Ch22。
- **Discord Developer Documentation**：[文档](https://discord.com/developers/docs)。作为消息平台适配的对照。引用章节：Ch22。

### E.4 无代码与低代码

- **n8n**：[文档](https://docs.n8n.io/)；[GitHub](https://github.com/n8n-io/n8n)。引用章节：Ch23。
- **Dify**：[文档](https://docs.dify.ai/)；[GitHub](https://github.com/langgenius/dify)。引用章节：Ch23。

### E.5 IDE 与终端代理

- **Visual Studio Code Extension API**：[官方 API](https://code.visualstudio.com/api)。引用章节：Ch23。
- **OpenCode**：[官网](https://opencode.ai/)。引用章节：Ch23。
- **Aider**：[官网](https://aider.chat/)；[GitHub](https://github.com/Aider-AI/aider)。引用章节：Ch23。
- **Codex CLI**：[GitHub](https://github.com/openai/codex)。引用章节：Ch23。
- **Hermes Agent**：[GitHub 搜索入口](https://github.com/search?q=Hermes+Agent&type=repositories)。引用章节：Ch23。由于同名项目较多，部署前应按正文给出的具体组织名和版本核对，不能仅凭项目名称安装。

## F. 协议、可观测性与工具链

### F.1 MCP 协议

- **Model Context Protocol**：[官网](https://modelcontextprotocol.io/)；[规范](https://modelcontextprotocol.io/specification/latest)。
  - 用途：规定模型客户端、服务器、工具、资源和提示模板之间的互操作协议。
  - 引用章节：Ch20、Ch21、Ch23。

### F.2 可观测性

- **OpenTelemetry**：[官网](https://opentelemetry.io/)；[规范](https://opentelemetry.io/docs/specs/)。引用章节：Ch11、Ch26、Ch29。
- **Langfuse**：[官网](https://langfuse.com/)；[GitHub](https://github.com/langfuse/langfuse)。用于 LLM 调用追踪、Token/成本统计和评估。引用章节：Ch11、Ch26。
- **Prometheus**：[官网](https://prometheus.io/)；[文档](https://prometheus.io/docs/)。用于指标采集与告警的基础设施对照。引用章节：Ch26、Ch29。
- **Grafana**：[官网](https://grafana.com/)；[文档](https://grafana.com/docs/)。用于观测面板和检索质量运营。引用章节：Ch26、Ch29。

### F.3 管道与编排

- **Apache Airflow**：[官网](https://airflow.apache.org/)；**Prefect**：[官网](https://www.prefect.io/)。二者用于对照有向无环任务、重试、调度和可观测编排。引用章节：Ch07、Ch14、Ch29。
- **LangChain LCEL**：[概念文档](https://python.langchain.com/docs/concepts/lcel/)。引用章节：Ch07、Ch21。
- **LlamaIndex Workflow**：[文档](https://docs.llamaindex.ai/en/stable/module_guides/workflow/)。引用章节：Ch07、Ch21。
- **Temporal**：[官网](https://temporal.io/)；[文档](https://docs.temporal.io/)。作为长事务、重试和持久化工作流的对照。引用章节：Ch14、Ch29。

### F.4 文档与图示

- **Mermaid**：[官网与语法](https://mermaid.js.org/)。全书 Mermaid 流程图、时序图和架构图均以其语法为基础。引用章节：全书。
- **mdBook**：[官方文档](https://rust-lang.github.io/mdBook/)。用于文档站生成。引用章节：Ch30。
- **GitBook**：[官网](https://www.gitbook.com/)。作为发布方案对照。引用章节：Ch30。
- **Pandoc**：[官网](https://pandoc.org/)；[用户指南](https://pandoc.org/MANUAL.html)。用于 EPUB/PDF 转换与发布阶段。引用章节：Ch30。

### F.5 Python 生态

- **Pydantic v2**：[文档](https://docs.pydantic.dev/latest/)。数据模型、配置校验和结构化输出。引用章节：Ch08、Ch13、Ch27。
- **FastAPI**：[官网](https://fastapi.tiangolo.com/)。用于将记忆管道封装为 HTTP 服务。引用章节：Ch17、Ch27、Ch29。
- **Python asyncio**：[标准库文档](https://docs.python.org/3/library/asyncio.html)。异步任务、并发限制和生命周期管理。引用章节：Ch07、Ch14、Ch17。
- **Python Packaging User Guide**：[packaging.python.org](https://packaging.python.org/)。用于虚拟环境、依赖锁定和发布实践。引用章节：Ch02、Ch27、Ch30。

## G. 同类项目参考

> Cognee 不是唯一的 Agent 记忆框架。以下项目用于比较记忆的写入策略、上下文管理、图结构、用户隔离和评估方式；它们不代表 Cognee 的运行时依赖。

- **Mem0**（`mem0ai/mem0`）。[GitHub](https://github.com/mem0ai/mem0)；[文档](https://docs.mem0.ai/)。引用章节：Ch05、Ch25。
- **Zep / Graphiti**（`getzep/graphiti`）。[GitHub](https://github.com/getzep/graphiti)；[文档](https://help.getzep.com/)。引用章节：Ch05、Ch06、Ch25。
- **Letta**（原 MemGPT 生态）。[GitHub](https://github.com/letta-ai/letta)；[文档](https://docs.letta.com/)。引用章节：Ch05、Ch25。
- **LangChain Memory**：[记忆概念文档](https://python.langchain.com/docs/concepts/memory/)。引用章节：Ch05、Ch21、Ch25。
- **LlamaIndex**：[记忆文档](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/memory/)。引用章节：Ch05、Ch21、Ch25。
- **Microsoft GraphRAG**：[GitHub](https://github.com/microsoft/graphrag)。引用章节：Ch05、Ch06、Ch25、Ch26。
- **Haystack**：[官网](https://haystack.deepset.ai/)；[GitHub](https://github.com/deepset-ai/haystack)。作为检索管道与评估的对照。引用章节：Ch04、Ch25。

## H. 安全、隐私与评估参考

- **OWASP Top 10 for LLM Applications**：[项目主页](https://owasp.org/www-project-top-10-for-large-language-model-applications/)。用于提示注入、敏感信息泄露、工具滥用和过度代理权限的威胁建模。引用章节：Ch16、Ch18、Ch29。
- **NIST AI Risk Management Framework**：[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)。用于风险识别、治理、测量和管理。引用章节：Ch16、Ch29。
- **NIST Privacy Framework**：[NIST Privacy Framework](https://www.nist.gov/privacy-framework)。用于个人数据最小化、用途限制和生命周期治理。引用章节：Ch16、Ch18。
- **MTEB: Massive Text Embedding Benchmark**：[论文](https://arxiv.org/abs/2210.07316)。用于比较嵌入模型在检索、分类、聚类等任务上的表现。引用章节：Ch12、Ch26。
- **RAGAS**：[官网](https://docs.ragas.io/)；[GitHub](https://github.com/explodinggradients/ragas)。用于上下文相关性、忠实性和答案相关性评估。引用章节：Ch12、Ch26。
- **BEIR**：[GitHub](https://github.com/beir-cellar/beir)。用于跨数据集信息检索基准的背景对照。引用章节：Ch12、Ch26。

## 索引：本附录涉及章节

- **Ch01**：A.1、A.5、B.1、B.2；概念总览、ECL、知识图谱与 Cognee 定位。
- **Ch02**：A.3、A.6、B.1、B.3、D.1；安装、LLM、RAG 与记忆分层。
- **Ch03**：A.5、B.1；实体、关系与知识表示。
- **Ch04**：A.1、A.2、A.3、A.4、F.3、G；检索、RAG 与基准。
- **Ch05**：A.3、A.6、A.5、B.1、G；记忆框架比较。
- **Ch06**：A.5、B.1、B.3、C.2、G；图谱与多跳检索。
- **Ch07**：A.3、A.6、B.1、F.3、F.5；任务管道与异步编排。
- **Ch08**：B.1、B.2、C.3、D.1、F.5；数据模型与配置。
- **Ch09**：B.1、D.2、A.4；分块、嵌入与索引输入。
- **Ch10**：B.1、B.3、C；存储后端矩阵。
- **Ch11**：B.1、D.1、D.2、F.2；本地模型与可观测性。
- **Ch12**：A.4、D.2、H；检索质量、嵌入和评估。
- **Ch13**：B.1、F.5；结构化输出与校验。
- **Ch14**：B.1、F.3、F.5；任务生命周期、重试与并发。
- **Ch15**：A.6、B.1；代理记忆与反思。
- **Ch16**：B.1、H；隐私、权限和提示注入防护。
- **Ch17**：B.1、F.5；服务接口与部署。
- **Ch18**：B.1、H；数据治理与安全边界。
- **Ch19**：B.2；集成总览。
- **Ch20**：B.2、E.1、E.5、F.1；Claude、Agent SDK 与 MCP。
- **Ch21**：B.2、D.1、E.1、E.2、F.1、F.3、G；Agent 框架集成。
- **Ch22**：B.2、E.3；Telegram、Slack 和消息适配。
- **Ch23**：B.2、E.4、E.5、F.4；低代码、IDE 与终端工具。
- **Ch24**：B.1、B.2；综合集成实践。
- **Ch25**：A.3、A.5、A.6、G；记忆框架与图增强 RAG 对比。
- **Ch26**：A.1、A.2、A.3、A.4、A.5、F.2、H；评估、基准和可观测性。
- **Ch27**：B.1、B.3、C、D、F.5；生产配置和基础设施。
- **Ch28**：B.1、H；上线检查与安全治理。
- **Ch29**：B.1、C.3、D.1、F.2、F.3、H；服务化、运维和风险管理。
- **Ch30**：B.1、F.4、F.5；文档构建、打包与发布。

## 链接与版本核验说明

本附录优先使用项目官网、官方文档、GitHub 官方组织和论文原始页面。外部服务的 API、价格、模型名称、仓库 stars 与兼容矩阵均可能变化，因此不把它们写成永久不变的事实；书中涉及 Cognee v1.4.0 的 API 细节，应以对应版本源码和锁定依赖为准。论文链接保留 arXiv 编号或 DOI，代码链接尽量同时给出仓库和文档入口。对于同名或迁移中的项目（尤其 Hermes Agent、Ladybug/Kuzu 生态），请以仓库所有者、tag 和许可证进行二次确认。
