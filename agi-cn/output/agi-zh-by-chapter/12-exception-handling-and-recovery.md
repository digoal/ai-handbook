# 第 12 章 异常处理与恢复(Exception Handling and Recovery)

<!-- chapter: 12 | part: I | pages: 208-215 | translated_from: pdf/208-215 -->

为了使智能体在多样化的真实环境中可靠地运行，它们必须能够管理不可预见的情况、错误和故障。正如人类适应意外障碍一样，智能体需要强大的系统来检测问题、启动恢复程序，或至少确保可控的失败。这一基本需求构成了异常处理与恢复(Exception Handling and Recovery)模式的基础。

该模式专注于开发异常持久且有韧性的智能体，使其能够在面对各种困难和异常时保持不间断的功能和操作完整性。它强调主动准备和被动响应策略两方面的重要性，以确保持续运行，即使在面临挑战时也是如此。这种适应性对于智能体在复杂且不可预测的环境中成功运行至关重要，最终提升其整体有效性和可信度。

处理意外事件的能力确保这些人工智能系统不仅智能，而且稳定可靠，从而增强对其部署和性能的信心。集成全面的监控和诊断工具进一步增强了智能体快速识别和解决问题的能力，防止潜在的中断，并确保在不断变化的条件中更顺畅地运行。这些先进的系统对于维护人工智能操作的完整性和效率至关重要，强化了其管理复杂性和不可预测性的能力。

该模式有时可以与反思(Reflection)结合使用。例如，如果初始尝试失败并引发异常，反思过程可以分析该失败并以改进后的方式(例如使用改进的提示)重新尝试该任务，以解决错误。

> 图 12.1 智能体异常处理与恢复的关键组件

可行的策略，尤其是针对瞬时错误的重试(Retries)。利用替代策略或方法(回退， Fallbacks)能够确保部分功能得以维持。在完全恢复无法立即实现的情况下，智能体可以保持部分功能以至少提供某些价值(优雅降级， Graceful Degradation)。最后，对于需要人工干预或协作的情形，将问题上报给人类操作员或其他智能体可能至关重要(通知， Notification)。**恢复(Recovery)** 此阶段旨在使智能体或系统在错误发生后恢复到稳定且可操作的状态。这可能涉及撤销最近的更改或事务以消除错误的影响(状态回滚， State Rollback)。对错误根本原因进行彻底调查对于防止再次发生至关重要。可能需要通过自我修正机制或重新规划过程来调整智能体的规划、逻辑或参数，以避免在未来出现相同的错误。在复杂或严重的情况下，将问题委派给人类操作员或更高级别的系统(升级， Escalation)可能是最佳的行动方案。实施这种稳健的异常处理与恢复模式可以将智能体从脆弱且不可靠的系统转变为稳健、可靠的组件，使其能够在充满挑战且高度不可预测的环境中有效且富有韧性地运行。这确保了智能体能够维持功能、最大限度地减少停机时间，并在面临意外问题时提供无缝且可靠的体验。

## 实际应用与用例

异常处理与恢复(Exception Handling and Recovery)对于任何部署在现实世界场景中、无法保证完美运行条件的智能体(Agent)都至关重要。

- **客服聊天机器人**:如果聊天机器人尝试访问客户数据库，而数据库暂时不可用，它不应崩溃。相反，它应该检测到 API 错误，告知用户这一临时问题，可能建议稍后重试，或将查询升级给人类坐席。
- **自动化金融交易**:交易机器人尝试执行一笔交易时，可能会遇到"资金不足"错误或"市场休市"错误。它需要通过记录错误来处理这些异常，而不是反复尝试同一笔无效交易，并且可能需要通知用户或调整其策略。
- **智能家居自动化**:控制智能灯具的智能体可能由于网络问题或设备故障而无法打开一盏灯。它应该检测到此故障，或许进行重试，如果仍然失败，则通知用户该灯无法打开，并建议手动干预。
- **数据处理智能体**:负责处理一批文档的智能体可能会遇到损坏的文件。它应该跳过损坏的文件，记录错误，继续处理其他文件，并在最后报告被跳过的文件，而不是中止整个流程。
- **网络爬虫智能体**:当网络爬虫智能体遇到验证码、网页结构变更或服务器错误(例如 404 Not Found、503 Service Unavailable)时，它需要优雅地处理这些情况。这可能包括暂停操作、使用代理，或报告失败的具体 URL。
- **机器人与制造业**:执行装配任务的机械臂可能由于未对准而无法抓取一个零件。

它需要检测
这一故障(例如通过传感器反馈),尝试重新调整，重试抓取，
若问题持续，则提醒人工操作员或切换到其他部件。总之，该模式对于构建不仅智能，而且在面对现实世界
复杂性时可靠、有韧性且用户友好的智能体而言，是根本性的。

## 动手实践代码示例(ADK)

异常处理与恢复对于系统的鲁棒性和可靠性至关重要。例如，考虑智能体对工具调用失败时的响应。此类失败可能源于错误的工具输入，或是工具所依赖的外部服务出现问题。

```python
from google.adk.agents import Agent, SequentialAgent
  # Agent 1: Tries the primary tool. Its focus is narrow and clear.
  primary_handler = Agent(
     name="primary_handler",
     model="gemini-2.0-flash-exp",
     instruction="""
  Your job is to get precise location information.
  Use the get_precise_location_info tool with the user's provided
  address.
     """,
     tools=[get_precise_location_info]
  )
  # Agent 2: Acts as the fallback handler, checking state to
  decide its action.
  fallback_handler = Agent(
     name="fallback_handler",
     model="gemini-2.0-flash-exp",
     instruction="""
  Check if the primary location lookup failed by looking at
  state["primary_location_failed"].
  - If it is True, extract the city from the user's original query
  and use the get_general_area_info tool.
  - If it is False, do nothing.
     """,
     tools=[get_general_area_info]
  )
  # Agent 3: Presents the final result from the state.
  response_agent = Agent(
     name="response_agent",
     model="gemini-2.0-flash-exp",
     instruction="""
  Review      the     location      information      stored     in
  state["location_result"].
  Present this information clearly and concisely to the user.
  If state["location_result"] does not exist or is empty, apolo-
  gize that you could not retrieve the location.
     """,
     tools=[] # This agent only reasons over the final state.
  )
  # The SequentialAgent ensures the handlers run in a guaran-
  teed order.
  robust_location_agent = SequentialAgent(
     name="robust_location_agent",
     sub_agents=[primary_handler,                fallback_handler,
  response_agent]
  )
```

```python
robust_location_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent]
)
```

这段代码使用 ADK 的 SequentialAgent 定义了一个健壮的位置检索系统，其中包含三个子智能体。primary_handler 是第一个智能体，尝试使用 get_precise_location_info 工具获取精确的位置信息。fallback_handler 作为备份，负责检查主查找是否失败，具体方法是通过检查一个状态变量。如果主查找失败，fallback 智能体会从用户的查询中提取城市信息，并使用 get_general_area_info 工具。response_agent 是序列中的最后一个智能体，负责审查存储在状态中的位置信息。该智能体被设计为向用户展示最终结果。如果未找到任何位置信息，它会向用户致歉。SequentialAgent 确保这三个智能体按照预定义顺序执行。这种结构允许采用分层方式来检索位置信息。

## 概览

**是什么** 在真实环境中运行的 AI 智能体不可避免地会遇到突发状况、错误以及系统故障。这些干扰的范围从工具故障、网络问题到无效数据，不一而足，从而威胁智能体完成任务的能力。如果没有结构化的方式来管理这些问题，智能体可能会变得脆弱、不可靠，并且在面对意外障碍时容易完全崩溃。这种不可靠性使得它们难以被部署在需要稳定表现的关键或复杂应用中。

**为什么** 异常处理与恢复(Exception Handling and Recovery)模式为构建健壮且有韧性的 AI 智能体提供了一种标准化的解决方案。它赋予智能体预测、管理并从故障中恢复的智能体式能力，确保系统即便在出现意外错误时也能继续运行。

异常处理与恢复模式为构建健壮且具有韧性的智能体(Agent)提供了一套标准化解决方案。它赋予智能体预测、管理和恢复运行故障的智能体式(Agentic)能力。该模式包含主动的错误检测，例如监控工具输出和 API 响应，以及被动响应式的处理策略，如用于诊断的日志记录、对瞬时故障的重试，或使用回退机制。对于更严重的问题，它定义了恢复协议，包括回退到稳定状态、通过调整自身规划进行自我修正，或将问题上报给人类操作员。这种系统化的方法能够确保智能体在不可预测的环境中保持运行完整性、从失败中学习，并可靠地运作。

**Rule of Thumb(经验法则)** 在任何部署于动态真实世界环境的智能体(Agent)中使用此模式，这类环境中可能出现系统故障、工具错误、网络问题或不可预测的输入，而运行可靠性是核心需求。

**Visual Summary(图 12.2)**

## 关键要点

需要铭记的关键要点：

- 异常处理与恢复(Exception Handling and Recovery)对于构建健壮且可靠的智能体至关重要。
- 该模式涉及检测错误、优雅地处理错误，并实施恢复策略。
- 错误检测可以包括验证工具输出、检查 API 错误码以及使用超时机制。
- 处理策略包括日志记录、重试、回退、优雅降级以及通知。
- 恢复聚焦于通过诊断、自我修正或上报升级来恢复稳定运行。
- 该模式确保智能体即使在不可预测的真实环境中也能有效运行。

## 结论

本章探讨了异常处理与恢复(Exception Handling and Recovery)模式，该模式对于开发稳健且可靠的 AI 智能体至关重要。该模式阐述了 AI 智能体如何识别与管理意外问题、实施恰当的响应，以及恢复至稳定的运行状态。本章讨论了该模式的多个方面，包括错误检测、通过日志、重试与回退等机制进行错误处理，以及用于恢复智能体或系统正常运行的策略。异常处理与恢复模式在多个领域的实际应用得到了展示，以说明其在处理现实世界复杂性与潜在故障中的相关性。这些应用表明，为 AI 智能体配备异常处理能力，有助于提升其在动态环境中的可靠性与适应性。

## 参考文献

1. McConnell, S. (2004). 《Code Complete》(第 2 版). Microsoft Press.
2. O'Neill, V. (2022). 《Improving Fault Tolerance and Reliability of Heterogeneous Multi-Agent IoT Systems Using Intelligence Transfer》. *Electronics*, 11(17), 2724.
3. Shi, Y., Pei, H., Feng, L., Zhang, Y., & Yao, D. (2024). 《Towards Fault Tolerance in Multi-Agent Reinforcement Learning》. *arXiv 预印本*, arXiv:2412.00534.





