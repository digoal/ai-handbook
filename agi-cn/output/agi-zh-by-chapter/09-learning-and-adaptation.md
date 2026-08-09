# 第 9 章 学习与适应(Learning and Adaptation)

<!-- chapter: 9 | part: I | pages: 168-179 | translated_from: pdf/168-179 -->

学习与适应对于提升人工智能智能体的能力至关重要。这些过程使智能体能够突破预定义参数的局限，使其通过经验和环境交互自主地改进。通过学习与适应，智能体能够有效地应对新颖情境，并在没有持续人工干预的情况下优化自身性能。本章将详细探讨支撑智能体学习与适应的原理与机制。

## 全局视角

智能体通过基于新经验和数据改变其思维、行动或知识来进行学习与适应。这使得智能体能够从仅仅遵循指令，逐步演变为随时间推移而变得更加智能。

- 强化学习(RL):智能体尝试各种动作，对正面结果获得奖励、对负面结果受到惩罚，从而在变化的环境中学习到最优行为。适用于控制机器人或下棋的智能体。
- 监督学习(SL):智能体从带标签的样本中学习，将输入映射到期望输出，从而能够执行决策和模式识别等任务。非常适合用于邮件分类或趋势预测的智能体。
- 无监督学习(UL):智能体在无标签数据中发现隐藏的关联与模式，从而辅助洞察、组织信息，并构建其所处环境的心理地图。适用于在没有具体指导下探索数据的智能体。

## 实际应用与用例

自适应智能体通过基于经验数据的迭代更新，在多变环境中表现出更优的性能。

- **个性化助手智能体**:通过纵向分析个体用户行为来优化交互协议，从而生成高度定制化的响应。
- **交易机器人智能体**:根据高分辨率、实时市场数据动态调整模型参数来优化决策算法，从而最大化财务回报并降低风险因素。
- **应用智能体**:根据观察到的用户行为动态修改用户界面与功能，提升用户参与度和系统易用性。
- **机器人与自动驾驶车辆智能体**:通过整合传感器数据与历史动作分析，增强导航与响应能力，使其能够在多样化的环境条件下安全高效地运行。
- **欺诈检测智能体**:通过使用新发现的欺诈模式优化预测模型，提升异常检测能力，增强系统安全性并减少财务损失。
- **推荐智能体**:通过运用用户偏好学习算法，提升内容选择的精确度，提供高度个性化且符合上下文的推荐。
- **游戏 AI 智能体**:通过动态调整策略算法提升玩家参与度，从而增加游戏的复杂度和挑战性。
- **知识库学习型智能体**:智能体可以利用检索增强生成(RAG)来维护一个包含问题描述与已验证解决方案的动态知识库(参见第 14 章)。通过存储成功的策略与所遭遇的挑战，智能体在决策过程中可以参考这些数据，从而能够通过应用先前成功的模式或规避已知的陷阱，更有效地适应新情境。

## 案例研究：自我改进编码智能体(SICA)

由 Maxime Robeyns、Laurence Aitchison 和 Martin Szummer 开发的自我改进编码智能体(Self-Improving Coding Agent,SICA)代表了基于智能体的学习领域的进展，展示了智能体修改自身源代码的能力。这与传统方法形成对比——在传统方法中，一个智能体可能训练另一个智能体；而 SICA 同时充当修改者和被修改实体，通过迭代方式精炼其代码库，以在各种编码挑战中提升表现。

SICA 的自我改进通过一个迭代循环运作(参见图 9.1)。最初，SICA 会审视其过往版本的归档及其在基准测试中的表现。它选择表现得分最高的版本，该得分基于一个加权公式计算，综合考虑成功率、时间和计算成本。被选中的版本随后进入下一轮

**Fig. 9.1** SICA 的自我改进，基于其过往版本进行学习与适应

h an iterative cycle (see Fig. 9.1).

最初，SICA 会审查其过往版本的存档及其在基准测试中的表现。它根据加权公式(综合考虑成功率、时间和计算成本)选出得分最高的版本，该版本随后进入下一轮自我修改。它分析存档以识别潜在的改进点，然后直接修改自身的代码库。修改后的智能体随即在基准测试中接受评估，结果记录到存档中。这一过程不断重复，使其能够直接从过往表现中学习。这种自我改进机制使 SICA 无需依赖传统训练范式即可逐步提升自身能力。SICA 经历了显著的自我改进，在代码编辑和导航方面取得了长足进步。起初，SICA 采用一种基本的文件覆盖方式来完成代码变更。随后，它发展出"智能编辑器(Smart Editor)",能够进行更智能、更贴合上下文的编辑。这一能力又演化为"差异增强型智能编辑器(Diff-Enhanced Smart Editor)",通过差异比对实现针对性修改与基于模式的编辑，并引入"快速覆盖工具(Quick Overwrite Tool)"以降低处理开销。SICA 还进一步实现了"最小差异输出优化(Minimal Diff Output Optimization)"与"上下文敏感的差异最小化(Context-Sensitive Diff Minimization)",借助抽象语法树(Abstract Syntax Tree, AST)解析提升效率。此外，系统还新增了"智能编辑器输入标准化器(SmartEditor Input Normalizer)"。在导航方面，SICA 自主创建了"AST 符号定位器(AST Symbol Locator)",利用代码的结构图(AST)在代码库中定位符号定义。后续又开发出"混合符号定位器(Hybrid Symbol Locator)",将快速搜索与 AST 检查相结合，并通过"混合符号定位器中的 AST 解析优化(Optimized AST Parsing in Hybrid Symbol Locator)"进一步聚焦于相关代码段，从而提升了搜索速度(见图 9.2)。SICA 的架构包含一套用于基础文件操作、命令执行和算术运算的基础工具集，并集成了结果提交以及专用子智能体(编码、问题求解与推理)的调用机制。

[图 9.1 SICA 基于过往版本进行自我改进、学习与适应]

[图 9.2 SICA 在代码编辑与导航能力上的演进]

这些子智能体能够分解复杂任务，并管理大语言模型(LLM)的上下文长度，尤其是在较长的改进周期中。SICA 还配备了一个异步监督器(由另一个大语言模型担任),负责监控 SICA 的行为，识别潜在问题，例如循环或停滞状态。该监督器与 SICA 通信，并在必要时进行干预以暂停执行。监督器接收 SICA 行为的详细报告，包括调用图(callgraph)以及消息和工具操作的日志，从而识别模式与低效之处。

SICA 的大语言模型在其短期记忆(Short-Term Memory)中以结构化方式组织信息，这种结构对系统运行至关重要。该结构包括以下组成部分：

- 系统提示(System Prompt):定义智能体目标、工具与子智能体的相关文档，以及系统指令。
- 核心提示(Core Prompt):包含问题陈述或指令、打开的文件内容以及目录映射。
- 助手消息(Assistant Messages):记录智能体逐步推理过程、工具与子智能体的调用记录及结果，以及与监督器的通信。

这种组织方式有助于高效的信息流转，提升大语言模型的运行效率，并降低开销，

**图 9.2** 跨迭代的性能表现。关键改进处标注了对应的工具或智能体修改。(由 Maxime Robeyns、Martin Szummer、Laurence Aitchison 提供)

处理时间和成本。最初，文件变更以差异( diff )形式记录，仅显示修改内容，并定期合并。

## SICA:代码解析

深入探究 SICA 的实现，可以发现支撑其能力的关键设计选择。如前所述，该系统采用模块化架构，集成了多个子智能体( sub-agent ),例如编码智能体、问题求解智能体和推理智能体。这些子智能体由主智能体调用，其方式类似于工具调用，用于分解复杂任务并有效管理上下文长度，尤其是在那些延长的元改进迭代过程中。

该项目正在积极开发中，旨在为那些对在工具使用及其他智能体式任务上对 LLM 进行后训练感兴趣的人提供一个稳健的框架，完整代码可在 https://github.com/MaximeRobeyns/self_improving_coding_agent/ 的 GitHub 仓库获取，以便进一步探索和贡献。

出于安全考虑，该项目强烈强调 Docker 容器化( Docker containerization ),这意味着智能体在专用的 Docker 容器内运行。这是一项关键措施，因为它能提供与宿主机的隔离，降低诸如智能体在执行 shell 命令时意外操纵文件系统的风险。

为确保透明度和可控性，该系统通过交互式网页提供强大的可观测性( observability ),可视化事件总线上的事件以及智能体的调用图( callgraph )。这提供了对智能体行为的全面洞察，允许用户检查单个事件、读取监督器( Overseer )消息，并折叠子智能体的调用轨迹以获得更清晰的理解。

在核心智能方面，该智能体框架支持接入来自不同提供商的 LLM,从而能够针对特定任务尝试不同模型以找到最佳匹配。最后，一个关键组件是异步监督器——一个与主智能体并发运行的 LLM。该监督器会周期性地评估智能体的行为，检查是否存在病态偏离或停滞，并在必要时通过发送通知甚至取消智能体的执行来介入。它接收系统状态的详细文本表示，包括调用图以及 LLM 消息、工具调用和响应的事件流，从而能够检测低效模式或重复工作。在最初的 SICA 实现中，一个值得关注的挑战是，如何提示基于 LLM 的智能体在每次元改进迭代中独立地提出新颖、创新、可行且引人入胜的修改。在 LLM 智能体中促进开放式学习和真实创造力这一局限，仍是当前研究中的一个关键探索方向。

## AlphaEvolve 和 OpenEvolve

AlphaEvolve 是由 Google 开发的智能体，旨在发现并优化算法。它结合使用 LLM(具体而言是 Gemini 模型，包括 Flash 和 Pro)、自动化评估系统以及进化算法框架。该系统旨在推进理论数学和实际计算应用的发展。AlphaEvolve 采用一组 Gemini 模型的集成。其中 Flash 用于生成广泛的初始算法提案，而 Pro 则提供更深入的分析与优化。所提出的算法随后会根据预定义的标准进行自动评估和打分。这种评估提供的反馈被用于迭代地改进解决方案，从而得到经过优化的新算法。在实际计算领域，AlphaEvolve 已被部署于 Google 的基础设施中。

AlphaEvolve 已在 Google 基础设施内部署，展示了在数据中心调度方面的改进，使全局计算资源使用率降低了 0.7%。它还通过为即将推出的 Tensor Processing Units (TPUs) 中的 Verilog 代码提出优化建议，为硬件设计做出了贡献。此外，AlphaEvolve 加速了 AI 性能，包括 Gemini 架构中一个核心内核提速 23%,以及 FlashAttention 的底层 GPU 指令优化达 32.5%。在基础研究领域，AlphaEvolve 为矩阵乘法新算法的发现做出了贡献，包括一种针对 4x4 复值矩阵使用 48 次标量乘法的方法，超越了此前已知的解法。在更广泛的数学研究中，它以 75% 的比例重新发现了超过 50 个开放问题的现有最先进解，并在 20% 的情况下改进了现有解，例如在接触数(kissing number)问题上的进展。OpenEvolve 是一个利用 LLM 的进化式编码智能体(见图 9.3),可迭代地优化代码。它编排了一个由 LLM 驱动的代码生成、评估和选择流水线，以持续增强面向广泛任务的程序。OpenEvolve 的一个关键方面是它能够进化整个代码文件，而不仅限于单个函数。该智能体专为通用性而设计，支持多种编程语言，并兼容任何 LLM 的 OpenAI 兼容 API。此外，它融合了多目标优化，支持灵活的提示工程，并能够进行分布式评估以高效处理复杂的编码挑战。这段代码片段使用 OpenEvolve 库对程序执行进化式优化。它使用相关路径初始化 OpenEvolve 系统。

**图 9.3** OpenEvolve 内部架构由控制器管理。

该控制器负责编排若干关键组件：程序采样器(Program Sampler)、程序数据库(Program Database)、评估器池(Evaluator Pool)以及大语言模型集成(LLM Ensembles)。其主要功能是促进这些组件的学习与适应(Learning and Adaptation)过程，以提升代码质量。

`evolve.run(iterations = 1000)` 这一行启动进化过程，运行 1000 次迭代以寻找程序的改进版本。最后，它打印进化过程中找到的最佳程序的指标，格式化为四位小数。

```yaml
from openevolve import OpenEvolve
   # Initialize the system
   evolve = OpenEvolve(
      initial_program_path="path/to/initial_program.py",
      evaluation_file="path/to/evaluator.py",
      config_path="path/to/config.yaml"
   )
   # Run the evolution
   best_program = await evolve.run(iterations=1000)
   print(f"Best program metrics:")
   for name, value in best_program.metrics.items():
      print(f"  {name}: {value:.4f}")
At a Glance
What AI agents often operate in dynamic and unpredictable environments
where pre-programmed logic is insufficient. Their performance can degrade
when faced with novel situations not anticipated during their initial design.
Without the ability to learn from experience, agents cannot optimize their
strategies or personalize their interactions over time. This rigidity limits their
effectiveness and prevents them from achieving true autonomy in complex,
real-world scenarios.
```

标准化的解决方案是集成学习与适应(Learning and Adaptation)机制，将静态智能体转变为动态的、持续演化的系统。这使得智能体能够基于新数据和交互自主地完善其知识与行为。智能体式(Agentic)系统可以使用多种方法，从强化学习到更先进的技术(如自我修改),正如自我改进编码智能体(Self-Improving Coding Agent,SICA)所展示的那样。Google 的 AlphaEvolve 等先进系统利用 LLM 和进化算法来发现全新的、更高效的复杂问题解决方案。通过持续学习，智能体能够掌握新任务、提升性能并适应变化的条件，而无需持续的、手动的重编程。

> **经验法则**:在构建必须在动态、不确定或不断演化的环境中运行的智能体时，应使用此模式。对于需要个性化、持续性能改进以及能够自主处理新情境的应用来说，该模式至关重要。

**可视化总结(图 9.4)**

**关键要点**

- 学习与适应(Learning and Adaptation)关注的是智能体如何借助过往经验提升自身能力，并应对新情境。
- "适应"是学习带来的智能体行为或知识层面的可见变化。
- SICA(Self-Improving Coding Agent,自我改进的编码智能体)通过基于过往表现修改自身代码来实现自我改进，并由此衍生出诸如智能编辑器(Smart Editor)与 AST 符号定位器(AST Symbol Locator)等工具。
- 借助专用的"子智能体"与"监督者",这些自我改进系统能够更好地管理大规模任务并保持方向不偏离。
- 大语言模型(LLM)"上下文窗口"的组织方式(包括系统提示、核心提示与助手消息)对于智能体的工作效率至关重要。
- 对于需要在持续变化、不确定或需要个性化处理的环境中运行的智能体而言，该模式不可或缺。
- 构建具备学习能力的智能体，通常需要将其与机器学习工具集成，并妥善管理数据流。
- 一个仅配备基础编码工具的智能体系统，能够自主修改自身代码，从而提升其在基准任务上的表现。
- AlphaEvolve 是 Google 推出的智能体，它结合大语言模型与进化框架，自主地发现并优化算法，在基础研究与实际计算应用方面均带来了显著提升。

**结论**

本章探讨了学习与适应在人工智能中的关键作用。AI 智能体通过持续的数据获取与经验积累来提升自身表现。Self-Improving Coding Agent(SICA)正是其中的典范，它通过代码修改自主地增强自身能力。我们已经回顾了智能体式 AI 的基本组成要素，涵盖架构、应用、规划、多智能体协作、记忆管理以及学习与适应。其中，学习原则对于多智能体系统中的协同改进尤为关键。

要实现这一目标，微调数据必须准确反映完整的交互轨迹，捕捉每个参与智能体的输入与输出。这些要素推动了重大进展，例如 Google 的 AlphaEvolve。该 AI 系统通过 LLM、自动化评估和演化方法，自主发现并优化算法，从而推动科学研究和计算技术的进步。上述模式能够相互组合，构建复杂的 AI 系统。AlphaEvolve 等进展表明，由 AI 智能体自主进行算法发现与优化是可行的。

- AlphaEvolve 博客：https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill.
- OpenEvolve:https://github.com/codelion/openevolve
- Proximal Policy Optimization Algorithms,作者 John Schulman、Filip Wolski、Prafulla Dhariwal、Alec Radford 与 Oleg Klimov。论文可在 arXiv 获取：https://arxiv.org/abs/1707.06347
- Robeyns, M., Aitchison, L., & Szummer, M. (2025). *A Self-Improving Coding Agent*. arXiv:2504.15228v2:https://arxiv.org/pdf/2504.15228 https://github.com/MaximeRobeyns/self_improving_coding_agent
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.

