# 第 21 章 探索与发现(Exploration and Discovery)

<!-- chapter: 21 | part: I | pages: 342-355 | translated_from: pdf/342-355 -->

本章探讨能够使智能体(Agent)主动寻求新信息、发掘新可能性，并识别其运行环境中"未知的未知"的设计模式。探索与发现不同于在预定义解空间中的反应式行为或优化；相反，其重点在于智能体主动涉足未知领域、试验新方法，并生成新知识或新理解。对于运行在开放式、复杂或快速演进领域中的智能体而言，这一模式至关重要，因为静态知识或预编程解决方案在这些场景下并不充分。该模式着重强调智能体拓展其理解力与能力的作用。

## 实际应用与用例

智能体(Agent)具备智能地进行优先级排序与探索的能力，这使其在各领域获得了广泛应用。通过自主评估与排列潜在行动，这些智能体能够驾驭复杂环境、揭示隐藏洞见并驱动创新。这种优先级排序式的探索能力使它们能够优化流程、发现新知识并生成内容。

示例：

- **科学研究自动化**:智能体可设计与运行实验，分析结果，并构建新假设，以发现新颖的材料、药物候选物或科学原理。

## Google Co-scientist

AI 共同科学家(AI co-scientist)是由 Google Research 开发的智能体系统，作为计算科学协作者而设计。它在假设生成、提案细化以及实验设计等方面协助人类科学家。该系统基于 Gemini 大语言模型运行。

AI 共同科学家的开发旨在应对科学研究中的挑战。这些挑战包括处理海量信息、生成可验证的假设以及管理实验规划。AI 共同科学家通过执行涉及大规模信息处理与综合的任务来支持研究人员，有望揭示数据中的关联关系。其目的在于通过处理早期研究中计算密集的环节，增强人类的认知过程。

### 系统架构与方法论

AI 共同科学家的架构基于多智能体框架，旨在模拟协作式与迭代式流程。该设计集成了多个专用智能体，每个智能体在研究目标中承担特定角色。监督器智能体在异步任务执行框架内管理并协调这些个体智能体的活动，从而实现计算资源的灵活伸缩。其核心智能体及其功能包括(见图 21.1):

图 21.1 AI 共同科学家：从构思到验证。(Courtesy of the authors)

- 生成智能体(Generation agent):通过文献探索和模拟科学辩论来启动整个流程，产出初始假设。
- 反思智能体(Reflection agent):扮演同行评审者角色，对生成假设的正确性、新颖性和质量进行批判性评估。
- 排序智能体(Ranking agent):采用基于 Elo 的锦标赛机制，通过模拟科学辩论对假设进行比较、排序和优先级排序。
- 进化智能体(Evolution agent):通过简化概念、综合思路和探索非常规推理，持续优化排名靠前的假设。
- 邻近智能体(Proximity agent):计算邻近图以对相似观点进行聚类，辅助探索假设空间。
- 元评审智能体(Meta-review agent):综合所有评审和辩论中的洞察，识别共性模式并提供反馈，使系统能够持续改进。该系统的运行基础依赖于 Gemini,它提供了语言理解、推理和生成能力。该系统还引入了"测试时算力扩展(test-time compute scaling)"机制，能够在推理过程中动态分配更多计算资源，以迭代方式推理并优化输出。系统从多种来源处理和综合信息，包括学术文献、网页数据和数据库。该系统遵循迭代式的"生成、辩论、进化"流程，模拟科学方法。在人类科学家输入科学问题后，系统进入一个自我改进的循环，不断进行假设的生成、评估和优化。假设会接受系统性的评估，包括智能体之间的内部互评以及基于锦标赛的排序机制。

## 验证与结果

AI 联合科学家的实用性已在多项验证研究中得到证实，特别是在生物医学领域，其性能通过自动化基准测试、专家评审和端到端湿实验进行了全面评估。

## 自动化评估与专家评估

在具有挑战性的 GPQA 基准测试中，系统的内部 Elo 评分与其结果准确率表现出高度一致性，在困难的"钻石集"上达到了 78.4% 的 top-1 准确率。对超过 200 个研究目标的分析表明，正如 Elo 评分所衡量的，扩展测试时计算(Test-Time Compute)能够持续提升假设的质量。在精心挑选的 15 道高难度问题中，该 AI 联合科学家(AI Co-Scientist)超越了其他最先进的 AI 模型以及人类专家提供的"最佳猜测"解。在一项小规模评估中，生物医学专家评定该联合科学家的输出在新颖性和影响力方面优于其他基线模型。系统所提出的药物再利用方案(以 NIH Specific Aims 页面形式呈现)也由六位肿瘤学专家组成的评审小组评定为高质量。

## 端到端实验验证

- **药物再利用**:针对急性髓系白血病(AML),该系统提出了新颖的候选药物。其中一些(如 KIRA6)是完全没有先例的全新建议，在此之前没有任何关于其用于 AML 的临床前证据。随后的体外实验证实，KIRA6 及其他被建议的药物能够在临床相关浓度下抑制多种 AML 细胞系中的肿瘤细胞活力。
- **新靶点发现**:该系统为肝纤维化识别出了新的表观遗传学靶点。利用人类肝脏类器官进行的实验室实验验证了这些发现，表明针对所建议的表观遗传修饰因子的药物具有显著的抗纤维化活性。其中一种被识别出的药物已获得 FDA 批准用于另一种疾病，从而为药物再利用提供了机会。
- **抗菌素耐药性**:该 AI 联合科学家独立复现了未发表的实验发现。系统被赋予的任务是解释为何某些移动遗传元件(cf-PICIs)出现在众多细菌物种中。

在两天内，系统排名第一的假设是 cf-PICI 与多种噬菌体尾部相互作用以扩展其宿主范围。这一结论与一个独立研究团队经过十余年研究后通过实验验证的新发现相吻合。

## 增强与局限性

AI 联合科学家的设计理念强调对人类研究的增强(增强),而非完全自动化。研究人员通过自然语言与系统交互并对其进行引导，提供反馈、贡献自己的想法，并以"科学家在回路(Scientist-in-the-Loop)"的协作范式指导 AI 的探索过程。然而，该系统存在一些局限性。其知识受限于对开放获取文献的依赖，可能遗漏付费墙背后的关键已有工作。它对负面实验结果的访问也有限，而这类结果虽很少发表，但对资深科学家至关重要。此外，系统还继承了底层大语言模型(LLM)的局限性，包括可能出现事实性错误或"幻觉(Hallucination)"。

## 安全性

安全性是一项关键考量，系统内置了多重防护措施。所有研究目标在输入时都会经过安全审查，生成的假设也会被检查，以防止系统被用于不安全或不道德的研究。一项使用 1200 个对抗性研究目标的初步安全评估发现，系统能够稳健地拒绝危险输入。为确保负责任的开发，系统正通过"可信测试者规划(Trusted Tester Program)"向更多科学家开放，以收集真实世界的反馈。

## 动手代码示例

让我们看一个探索与发现领域中智能体式 AI(Agentic AI)的具体实例：Agent Laboratory,这是 Samuel Schmidgall 在 MIT 许可证下开发的一个项目。

"Agent Laboratory" 是一个自主研究工作流框架，旨在增强而非取代人类的科学探索工作。该系统利用专用大语言模型(LLM)来自动化科学研究过程的各个阶段，从而使人类研究人员能够将更多认知资源投入到概念构思与批判性分析中。该框架整合了 "AgentRxiv",这是一个面向自主研究智能体的去中心化知识库。AgentRxiv 支持研究成果的归档、检索与持续改进。Agent Laboratory 通过若干明确阶段来引导研究流程：

1. **文献综述(Literature Review)**:在初始阶段，由专用 LLM 驱动的智能体负责自主收集与批判性分析相关学术文献。这包括利用 arXiv 等外部数据库来识别、归纳并分类相关研究，从而为后续阶段奠定全面的知识基础。

2. **实验(Experimentation)**:此阶段涵盖实验设计的协同制定、数据准备、实验执行以及结果分析。智能体使用集成工具，如 Python 进行代码生成与执行，以及 Hugging Face 进行模型访问，以开展自动化实验。该系统支持迭代改进，智能体能够根据实时结果调整并优化实验流程。

3. **报告撰写(Report Writing)**:在最后阶段，系统自动化地生成完整的研究报告。

这涉及综合实验阶段的发现与文献综述的洞察，按照学术规范结构化文档，并整合外部工具如 LaTeX 用于专业排版和图表生成。
4. 知识共享：AgentRxiv 是一个平台，使自主研究智能体能够共享、访问并协作推进科学发现。它允许智能体在先前发现的基础上进行构建，促进累积的研究进展。Agent Laboratory 的模块化架构确保了计算灵活性。其目标是通过自动化任务来增强研究生产力，同时保持人类研究者的参与。

## 代码分析

虽然全面的代码分析超出了本书的范围，但我想为你提供一些关键洞察，并鼓励你自行深入研究代码。

```python
Judgment In order to emulate human evaluative processes, the system
employs a tripartite agentic judgment mechanism for assessing outputs. This
involves the deployment of three distinct autonomous agents, each config-
ured to evaluate the production from a specific perspective, thereby collec-
tively mimicking the nuanced and multi-faceted nature of human judgment.
This approach allows for a more robust and c omprehensive appraisal, moving
beyond singular metrics to capture a richer qualitative assessment.
  class ReviewersAgent:
     def __init__(self, model="gpt-4o-mini", notes=None,
  openai_api_key=None):
         if notes is None: self.notes = []
         else: self.notes = notes
         self.model = model
         self.openai_api_key = openai_api_key
     def inference(self, plan, report):
         reviewer_1 = "You are a harsh but fair reviewer and expect
  good experiments that lead to insights for the research topic."
         review_1 = get_score(outlined_plan=plan, latex=report,
  reward_model_llm=self.model, reviewer_type=reviewer_1, openai_
  api_key=self.openai_api_key)
         reviewer_2 = "You are a harsh and critical but fair
  reviewer who is looking for an idea that would be impactful in
  the field."
         review_2 = get_score(outlined_plan=plan, latex=report,
  reward_model_llm=self.model, reviewer_type=reviewer_2, openai_
  api_key=self.openai_api_key)
         reviewer_3 = "You are a harsh but fair open-minded
  reviewer that is looking for novel ideas that have not been
  proposed before."
         review_3 = get_score(outlined_plan=plan, latex=report,
  reward_model_llm=self.model, reviewer_type=reviewer_3, openai_
  api_key=self.openai_api_key)
         return f"Reviewer #1:\n{review_1}, \nReviewer
  #2:\n{review_2}, \nReviewer #3:\n{review_3}"
```

评审智能体(Judgment Agent)使用一个特定的提示进行设计，该提示紧密模拟了人类评审员通常采用的认知框架与评估标准。该提示引导智能体(Agent)透过类似于人类专家的视角来分析输出，综合考量相关性、连贯性、事实准确性以及整体质量等要素。通过精心设计这些提示来映射人类评审协议，系统旨在实现一种接近人类判别能力的评估精密度。

```python
def get_score(outlined_plan, latex, reward_model_llm, reviewer_type=None, attempts=3, openai_api_key=None):
    e = str()
    for _attempt in range(attempts):
        try:
            template_instructions = """
            Respond in the following format:
            THOUGHT:
            <THOUGHT>
            REVIEW JSON:
            ```json
            <JSON>
```text
            In <THOUGHT>, first briefly discuss your intuitions and reasoning for the evaluation. Detail your high-level arguments, necessary choices and desired outcomes of the review. Do not make generic comments here, but be specific to your current paper. Treat this as the note-taking phase of your review.
```

以 JSON 格式提供评审意见，包含以下字段(按此顺序):

- "Summary":对论文内容及其贡献的总结。
- "Strengths":论文优点列表。
- "Weaknesses":论文缺点列表。
- "Originality":评分 1 到 4(低、中、高、很高)。
- "Quality":评分 1 到 4(低、中、高、很高)。
- "Clarity":评分 1 到 4(低、中、高、很高)。
- "Significance":评分 1 到 4(低、中、高、很高)。
- "Questions":一组需要由论文作者回答的澄清性问题。
- "Limitations":一组关于该项工作局限性及潜在负面社会影响的说明。
- "Ethical Concerns":布尔值，表示是否存在伦理方面的顾虑。
- "Soundness":评分 1 到 4(差、中、良、优)。
- "Presentation":评分 1 到 4(差、中、良、优)。
- "Contribution":评分 1 到 4(差、中、良、优)。
- "Overall":评分 1 到 10(强烈拒收到授予质量)。
- "Confidence":评分 1 到 5(低、中、高、很高、绝对)。
- "Decision":必须为以下两个值之一：Accept(接受)或 Reject(拒绝)。对于 "Decision" 字段，不得使用 Weak Accept(弱接受)、Borderline Accept(边缘接受)、Borderline Reject(边缘拒绝)或 Strong Reject(强烈拒绝),仅可使用 Accept 或 Reject。此 JSON 将被自动解析，因此必须确保格式精确。

Professor 智能体(Professor Agent) Professor 智能体充当主要的研究主管，负责制定研究议程、定义研究问题，并将任务委派给其他智能体。该智能体设定战略方向，并确保与项目目标保持一致。

```python
class ProfessorAgent(BaseAgent):
    def __init__(self, model="gpt4omini", notes=None, max_steps=100, openai_api_key=None):
        super().__init__(model, notes, max_steps, openai_api_key)
        self.phases = ["report writing"]
    def generate_readme(self):
        sys_prompt = f"""You are {self.role_description()} \n
Here is the written paper \n{self.report}. Task instructions:
Your goal is to integrate all of the knowledge, code, reports,
and notes provided to you and generate a readme.md for a github
repository."""
        history_str = "\n".join([_[1] for _ in self.history])
        prompt = (
            f"""History: {history_str}\n{'~' * 10}\n"""
            f"Please produce the readme below in markdown:\n")
        model_resp = query_model(model_str=self.model, system_prompt=sys_prompt,      prompt=prompt,      openai_api_key=self.openai_api_key)
        return model_resp.replace("```markdown", "")
```

PostDoc 智能体(PostDoc Agent)

PostDoc 智能体的职责是执行研究。这包括开展文献综述、设计并实施实验，以及生成研究产出物(例如论文)。重要的是，PostDoc 智能体具备编写和执行代码的能力，从而能够实际实施实验方案和数据分析。该智能体是研究产出物的主要生产者。

```python
class PostdocAgent(BaseAgent):
     def __init__(self, model="gpt4omini", notes=None, max_
  steps=100, openai_api_key=None):
         super().__init__(model, notes, max_steps, openai_api_key)
         self.phases = ["plan formulation", "results
  interpretation"]
     def context(self, phase):
         sr_str = str()
         if self.second_round:
             sr_str = (
                 f"The following are results from the previous
  experiments\n",
                 f"Previous
  Experiment code: {self.prev_results_code}\n"
                 f"Previous Results: {self.prev_exp_results}\n"
                 f"Previous Interpretation of results: {self.
  prev_interpretation}\n"
                 f"Previous Report: {self.prev_report}\n"
                 f"{self.reviewer_response}\n\n\n"
             )
         if phase == "plan formulation":
             return (
                 sr_str,
                 f"Current
  Literature Review: {self.lit_review_sum}",
             )
         elif phase == "results interpretation":
             return (
                 sr_str,
                 f"Current
  Literature Review: {self.lit_review_sum}\n"
                 f"Current Plan: {self.plan}\n"
                 f"Current Dataset code: {self.dataset_code}\n"
                 f"Current
  Experiment code: {self.results_code}\n"
                 f"Current Results: {self.exp_results}"
             )
         return ""
Reviewer Agents Reviewer agents perform critical evaluations of research
outputs from the PostDoc Agent, assessing the quality, validity, and scientific
rigor of papers and experimental results. This evaluation phase emulates the
peer-review process in academic settings to ensure a high standard of research
output before finalization.
```

机器学习工程智能体(Machine Learning Engineering Agents)扮演机器学习工程师的角色，与博士生进行对话式协作以开发代码。其核心功能是根据所提供的文献综述和实验方案，生成简洁的数据预处理代码。这保证了数据能够以恰当的格式进行准备，以适配所指定的实验。

"你是一位软件开发工程师，正在指导一位机器学习工程师。这位机器学习工程师将负责编写代码，你可以通过对话与他们进行交互。\n"
"你的目标是帮助这位机器学习工程师编写代码，为所给定的实验准备数据。你应当追求非常简单的数据准备代码，而非复杂的代码。你需要结合所提供的文献综述和方案，给出为本实验准备数据的代码。\n"

SWEngineerAgents 软件工程智能体(SWEngineerAgents)指导机器学习工程师智能体。它们的主要目的是协助机器学习工程师智能体为特定实验编写简洁的数据准备代码。软件工程智能体整合所提供的文献综述与实验规划，确保生成的代码简洁明了且直接契合研究目标。

"你是一名机器学习工程师，由一名博士生指导完成代码编写，你可以通过对话与他们互动。\n"
"你的目标是生成代码，为所提供的实验准备数据。你应该追求简单而非复杂的数据准备代码。你需要整合所提供的文献综述与规划，并提出用于为该实验准备数据的代码。\n"
综上所述，"Agent Laboratory"代表了一个用于自主科学研究的精密框架。它旨在通过自动化关键研究阶段，并促进协作式 AI 驱动的知识生成，来增强人类的研究能力。该系统致力于通过管理日常任务来提高研究效率，同时保持人类的监督。

## 一览

智能体(Agent)通常在预定义的范围内运作，这限制了它们应对全新场景或开放式问题的能力。在复杂且动态的环境中，这种静态的、预编程的信息不足以支撑真正的创新或发现。其根本挑战在于：必须使智能体能够超越简单优化，主动搜寻新信息并识别"未知的未知"(unknown unknowns)。这要求实现一种范式转变——从纯粹被动的行为转向主动的智能体式(Agentic)探索，从而拓展系统自身的理解力与能力。

为什么要采用这种方法 标准化解决方案是构建专门为自主探索与发现而设计的智能体式(Agentic) AI 系统。这类系统通常采用多智能体(Multi-Agent)框架，由专门化的大语言模型(LLM)彼此协作，以模拟科学方法等过程。例如，可以用不同的智能体分别承担生成假设、批判性审阅以及演进最具潜力的概念等任务。这种结构化、协作式的方法使系统能够智能地穿越广阔的信息空间、设计并执行实验，并生成真正的新知识。通过自动化探索中劳动密集的环节，这些系统拓展了人类智力，并显著加快发现的速度。

**经验法则** 在开放式、复杂或快速演化的领域中使用探索与发现(Exploration and Discovery)模式，因为这些领域的解空间并未被完全定义。当任务需要生成新颖的假设、策略或洞察时(例如在科学研究、市场分析和创意内容生成中),该模式是理想之选。当目标是揭示"未知的未知"(unknown unknowns)而非仅仅优化一个已知过程时，此模式至关重要。

**可视化总结**(图 21.2)

**图 21.2 探索与发现(Exploration and Discovery)设计模式**

## 关键要点

- 人工智能中的探索与发现使智能体能够主动寻求新信息和可能性，这对于在复杂且不断演变的环境中导航至关重要。
- 以 Google Co-Scientist 为代表的系统展示了智能体如何自主生成假设并设计实验，从而补充人类科学研究。
- 以 Agent Laboratory 的专业化角色为代表的多智能体框架，通过自动化文献综述、实验和报告撰写来改进研究。
- 最终，这些智能体旨在通过管理计算密集型任务来增强人类的创造力和问题解决能力，从而加速创新与发现。

## 结论

总之，探索与发现(Exploration and Discovery)模式是真正智能体系统(Agentic System)的精髓，它定义了系统超越被动遵循指令、主动探索环境的能力。这种内在的智能体式(Agentic)驱动力使 AI 能够在复杂领域内自主运行，不仅执行任务，还能独立设定子目标以发掘新颖信息。这种高级的智能体行为在多智能体框架中得以最有力地实现，其中每个智能体在整个协作过程中承担特定的、主动的角色。例如，Google Co-scientist 这一高度智能体化的系统便展现了智能体自主生成、辩论并演化科学假设的能力。

Agent Laboratory 等框架通过构建模拟人类研究团队的智能体层级结构，进一步将这一过程系统化，使系统能够自主管理整个发现生命周期。该模式的核心在于编排涌现式的智能体行为，使系统能够以最小的人工干预追求长期、开放式目标。这提升了人机协作关系，将 AI 定位为真正的智能体式协作者，负责自主执行探索性任务。通过将这种主动发现工作委派给智能体系统，人类智力得以显著增强，从而加速创新。如此强大的智能体能力的发展，也需要对安全与伦理监督做出坚定承诺。最终，该模式为打造真正智能体式 AI 提供了蓝图，将计算工具转变为在知识追求中独立、目标驱动的合作伙伴。

- Agent Laboratory: Using LLM Agents as Research Assistants https://github.com/SamuelSchmidgall/AgentLaboratory
- AgentRxiv: Towards Collaborative Autonomous Research: https://agentrxiv.github.io/
- Exploration-Exploitation Dilemma: A fundamental problem in reinforcement learning and decision-making under uncertainty. https://en.wikipedia.org/wiki/Exploration%E2%80%93exploitation_dilemma
- Google Co-Scientist: https://research.google/blog/accelerating-%C2%ADscientific-%C2%ADbreakthroughs-%C2%ADwith-%C2%ADan-%C2%ADai-%C2%ADco-%C2%ADscientist/

