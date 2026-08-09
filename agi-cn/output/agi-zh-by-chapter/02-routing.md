# 第 2 章 路由(Routing)

<!-- chapter: 2 | part: I | pages: 55-68 | translated_from: pdf/055-068 -->

虽然通过提示链(Prompt Chaining)进行顺序处理是利用语言模型执行确定性线性工作流的基础技术，但其适用性在需要自适应响应的场景中存在局限。现实世界中的智能体式(Agentic)系统必须经常根据情境因素(例如环境状态、用户输入或前一步操作的输出)在多个潜在动作之间进行仲裁。这种动态决策能力——控制将控制流转交给不同专用函数、工具或子流程——通过一种称为路由(Routing)的机制来实现。

路由将条件逻辑引入智能体的操作框架，使其能够从固定执行路径转向一种模型，在该模型中智能体动态评估特定标准，以从一组可能的后续动作中进行选择。这使得系统行为更加灵活且具备上下文感知能力。

例如，一个为客户咨询设计的智能体，在配备路由功能后，可以首先对收到的查询进行分类，以确定用户意图。基于此分类，它可以将查询路由到专用智能体以直接问答、用于账户信息检索的数据库检索工具，或用于复杂问题的升级处理流程，而不是默认采用单一预定响应路径。因此，使用路由的更复杂智能体可以：

## 实际应用与用例

路由(Routing)模式是自适应智能体系统(Agentic System)设计中的关键控制机制，使系统能够根据变化的输入和内部状态动态调整其执行路径。它通过提供必要的条件逻辑层而应用于多个领域。

在人在回路中，例如虚拟助手或 AI 驱动的辅导系统，路由被用于解读用户意图。对自然语言查询的初步分析决定最合适的后续动作，无论是调用特定的信息检索工具、升级给人工操作员，还是根据用户表现选择课程中的下一个模块。这使系统能够超越线性的对话流程，并能够根据上下文进行响应。

在自动化的数据和文档处理流水线中，路由充当分类与分发功能。传入的数据（例如电子邮件、支持工单或 API 负载）会根据内容、元数据或格式进行分析。然后系统将每个项目引导至相应的工作流，例如销售线索接入流程、针对 JSON 或 CSV 格式的特定数据转换函数，或紧急问题升级路径。

在涉及多个专门工具或智能体的复杂系统中，路由充当高层调度器。由搜索、总结和分析信息的不同智能体组成的研究系统会使用路由器(Router)，根据当前目标将任务分配给最合适的智能体。同样，AI 编码助手使用路由来识别编程语言和用户的意图——调试、解释或翻译——然后将代码片段传递给正确的专门工具。

最终，路由提供了逻辑仲裁的能力，这对于创建功能多样且具备上下文感知能力的系统至关重要。

它将智能体(Agent)从预定义序列的静态执行者转变为一个动态系统，使其能够在不断变化的条件下，决策出完成任务的最有效方法。

## 实战代码示例(LangChain)

在代码中实现路由需要定义可能的路径以及决定采用哪条路径的逻辑。LangChain 和 LangGraph 等框架为此提供了特定的组件和结构。LangGraph 基于状态图的结构对于可视化与实现路由逻辑尤为直观。下面的代码演示了一个使用 LangChain 与 Google Generative AI 的简单智能体式系统。它设置了一个"协调器",根据请求的意图(预订、信息或不明确),将用户请求路由到不同的模拟"子智能体"处理器。该系统使用大语言模型对请求进行分类，然后将其委托给相应的处理函数，模拟了多智能体架构中常见的基本委派模式。

First, ensure you have the necessary libraries installed:

```bash
pip install langchain langgraph google-cloud-aiplatform langchain-google-genai google-adk deprecated pydantic
# Copyright (c) 2025 Marco Fago
# https://www.linkedin.com/in/marco-fago/
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
# --- Configuration ---
# Ensure your API key environment variable is set (e.g., GOOGLE_API_KEY)
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    print(f"Language model initialized: {llm.model}")
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None
# --- Define Simulated Sub-Agent Handlers (equivalent to ADK sub_agents) ---
def booking_handler(request: str) -> str:
    """Simulates the Booking Agent handling a request."""
    print("\n--- DELEGATING TO BOOKING HANDLER ---")
    return f"Booking Handler processed request: '{request}'. Result: Simulated booking action."
def info_handler(request: str) -> str:
    """Simulates the Info Agent handling a request."""
    print("\n--- DELEGATING TO INFO HANDLER ---")
    return f"Info Handler processed request: '{request}'. Result: Simulated information retrieval."
def unclear_handler(request: str) -> str:
    """Handles requests that couldn't be delegated."""
    print("\n--- HANDLING UNCLEAR REQUEST ---")
    return f"Coordinator could not delegate request: '{request}'.
```

```python
# --- Define Coordinator Router Chain (equivalent to ADK coordinator's instruction) ---
# This chain decides which handler to delegate to.
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the user's request and determine which specialist handler should process it.
- If the request is related to booking flights or hotels, output 'booker'.
- For all other general information questions, output 'info'.
- If the request is unclear or doesn't fit either category, output 'unclear'. ONLY output one word: 'booker', 'info', or 'unclear'."""),
    ("user", "{request}")
])
if llm:
    coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

    # --- Define the Delegation Logic (equivalent to ADK's Auto-Flow based on sub_agents) ---
    # Use RunnableBranch to route based on the router chain's output.

    # Define the branches for the RunnableBranch
    branches = {
        "booker": RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
        "info": RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
        "unclear": RunnablePassthrough.assign(output=lambda x: unclear_handler(x['request']['request'])),
    }

    # Create the RunnableBranch.
```

```python
# 它接收路由链(router chain)的输出,并将原始输入('request')路由到相应的处理器。
delegation_branch = RunnableBranch(
    (lambda x: x['decision'].strip() == 'booker', branches["booker"]),  # Added .strip()
    (lambda x: x['decision'].strip() == 'info', branches["info"]),     # Added .strip()
    branches["unclear"]  # 'unclear' 或任何其他输出的默认分支
)

# 将路由链和委派分支合并为单个可运行对象(runnable)
# 路由链的输出('decision')与原始输入('request')一起传递给 delegation_branch。
coordinator_agent = {
    "decision": coordinator_router_chain,
    "request": RunnablePassthrough()
} | delegation_branch | (lambda x: x['output'])  # 提取最终输出

# --- 示例用法 ---
def main():
    if not llm:
        print("\n由于 LLM 初始化失败,跳过执行。")
        return

    print("--- 运行一个预订请求 ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"最终结果 A: {result_a}")

    print("\n--- 运行一个信息查询请求 ---")
    request_b = "What is the capital of Italy?"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"最终结果 B: {result_b}")

    print("\n--- 运行一个不明确的请求 ---")
    request_c = "Tell me about quantum physics."
    result_c = coordinator_agent.invoke({"request": request_c})
    print(f"最终结果 C: {result_c}")

if __name__ == "__main__":
    main()
```

你还需要为你选择的语言模型(例如 OpenAI、Google Gemini、Anthropic)设置 API key 环境变量。如前所述，这段 Python 代码使用 LangChain 库和 Google 的 Generative AI 模型(具体为 gemini-2.5-flash)构建了一个简单的类 agent 系统。具体来说，它定义了三个模拟的子 agent handler:`booking_handler`、`info_handler` 和 `unclear_handler`,每个 handler 旨在处理特定类型的请求。一个核心组件是 `coordinator_router_chain`,它利用 `ChatPromptTemplate` 来指示语言模型将传入的用户请求归类为三个类别之一：'booker'、'info' 或 'unclear'。该 router chain 的输出随后被 `RunnableBranch` 用于将原始请求委派给对应的 handler 函数。`RunnableBranch` 检查语言模型的决策，并将请求数据导向 `booking_handler`、`info_handler` 或 `unclear_handler` 中的一个。`coordinator_agent` 将这些组件组合在一起，首先对请求进行路由决策，然后将该请求传递给选定的 handler。最终输出从 handler 的响应中提取。主函数通过三个示例请求演示了该系统的使用，展示了不同输入是如何被模拟 agent 进行路由和处理的。其中包含了语言模型初始化的错误处理以确保鲁棒性。该代码结构模仿了一个基础的多 agent 框架，其中中央协调器根据意图将任务委派给专门的 agent。

### 动手代码示例(Google ADK)

Agent Development Kit(ADK)是一个用于工程化 agentic 系统的框架，它为定义 agent 的能力和行为提供了一个结构化的环境。与基于显式计算图的架构相比，ADK 范式中的路由通常通过定义一组离散的 "tools"(工具)来实现，这些工具代表 agent 的功能。

针对用户查询选择合适的工具，由框架的内部逻辑负责管理，该逻辑利用底层模型将用户意图匹配到正确的功能处理器。下面这段 Python 代码演示了一个使用 Google ADK 库的智能体开发工具包(Agent Development Kit, ADK)应用示例。它设置了一个 "Coordinator" 智能体，根据预定义指令将用户请求路由到专门的子智能体(用于预订的 "Booker" 和用于通用信息查询的 "Info")。随后，这些子智能体使用特定工具来模拟处理请求，展示了智能体系统中的一种基本委派模式。

```javascript
# Copyright (c) 2025 Marco Fago
     #
     # This code is licensed under the MIT License.
     # See the LICENSE file in the repository for the full license text.
     import uuid
     from typing import Dict, Any, Optional
     from google.adk.agents import Agent
     from google.adk.runners import InMemoryRunner
     from google.adk.tools import FunctionTool
     from google.genai import types
     from google.adk.events import Event
     # --- Define Tool Functions ---
     # These functions simulate the actions of the specialist agents.
     def booking_handler(request: str) -> str:
        """
        Handles booking requests for flights and hotels.
        Args:
            request: The user's request for a booking.
        Returns:
            A confirmation message that the booking was handled.
        """
        print("------------- Booking Handler Called -------------")
        return f"Booking action for '{request}' has been simulated."
     def info_handler(request: str) -> str:
        """
        Handles general information requests.
        Args:
       request: The user's question.
   Returns:
       A message indicating the information request was handled.
   """
   print("------------- Info Handler Called ----------------")
   return f"Information request for '{request}'. Result:
Simulated information retrieval."
def unclear_handler(request: str) -> str:
   """Handles requests that couldn't be delegated."""
   return f"Coordinator could not delegate request: '{request}'.
Please clarify."
# --- Create Tools from Functions ---
booking_tool = FunctionTool(booking_handler)
info_tool = FunctionTool(info_handler)
# Define specialized sub-agents equipped with their respec-
tive tools
booking_agent = Agent(
   name="Booker",
   model="gemini-2.0-flash",
   description="A specialized agent that handles all flight
           and hotel booking requests by calling the book-
ing tool.",
   tools=[booking_tool]
)
info_agent = Agent(
   name="Info",
   model="gemini-2.0-flash",
   description="A specialized agent that provides general
information
      and answers user questions by calling the info tool.",
   tools=[info_tool]
)
# Define the parent agent with explicit delegation instructions
coordinator = Agent(
   name="Coordinator",
   model="gemini-2.0-flash",
   instruction=(
       "You are the main coordinator. Your only task is to analyze
        incoming user requests "
       "and delegate them to the appropriate specialist agent.
        Do not try to answer the user directly.\n"
       "- For any requests related to booking flights or hotels,
         delegate to the 'Booker' agent.\n"
       "- For all other general information questions, delegate
to the 'Info' agent."
   ),
   description="A coordinator that routes user requests to the
     correct specialist agent.",
        # The presence of sub_agents enables LLM-driven delegation
     (Auto- Flow) by default.
        sub_agents=[booking_agent, info_agent]
     )
     # --- Execution Logic ---
     async
      def run_coordinator(runner: InMemoryRunner, request: str):
        """Runs the coordinator agent with a given request and
     delegates."""
        print(f"\n---        Running    Coordinator     with    request:
     '{request}' ---")
        final_result = ""
        try:
            user_id = "user_123"
            session_id = str(uuid.uuid4())
            await
       runner.session_service.create_session(
                app_name=runner.app_name, user_id=user_id, session_
     id=session_id
            )
            for event in runner.run(
               user_id=user_id,
                session_id=session_id,
                new_message=types.Content(
                    role= 'user',
                    parts=[types.Part(text=request)]
                ),
            ):
                if event.is_final_response() and event.content:
                    # Try to get text directly from event.content
                    # to avoid iterating parts
                    if hasattr(event.content, 'text') and event.con-
     tent.text:
                         final_result = event.content.text
                    elif event.content.parts:
                        # Fallback: Iterate through parts and extract
     text (might trigger warning)
                        text_parts = [part.text for part in event.con-
     tent.parts if part.text]
                        final_result = "".join(text_parts)
                    # Assuming the loop should break after the final
     response
                    break
            print(f"Coordinator Final Response: {final_result}")
            return final_result
        except Exception as e:
            print(f"An      error   occurred   while   processing   your
     request: {e}")
         return f"An error occurred while processing your
  request: {e}"
  async
   def main():
     """Main function to run the ADK example."""
     print("--- Google ADK Routing Example (ADK Auto-Flow
  Style) ---")
     print("Note: This requires Google ADK installed and
  authenticated.")
     runner = InMemoryRunner(coordinator)
     # Example Usage
     result_a = await run_coordinator(runner, "Book me a hotel in
  Paris.")
     print(f"Final Output A: {result_a}")
     result_b = await run_coordinator(runner, "What is the high-
  est mountain in the world?")
     print(f"Final Output B: {result_b}")
     result_c = await run_coordinator(runner, "Tell me a random
  fact.") # Should go to Info
     print(f"Final Output C: {result_c}")
     result_d = await run_coordinator(runner, "Find flights to
  Tokyo next month.") # Should go to Booker
     print(f"Final Output D: {result_d}")
  if __name__ == "__main__":
     import nest_asyncio
     nest_asyncio.apply()
     await main()
```

该脚本由一个主协调器(Coordinator)智能体和两个专门的子智能体(Sub-Agent)组成：预订智能体(Booker)与信息智能体(Info)。每个专门智能体都配备了一个 FunctionTool,该工具封装了一个用于模拟操作的 Python 函数。其中 booking_handler 函数模拟处理航班和酒店预订，而 info_handler 函数模拟检索一般信息。unclear_handler 作为回退选项，用于处理协调器无法委派的请求，尽管当前的协调器逻辑在主 run_coordinator 函数中并未明确将其用于委派失败的处理。

如协调器智能体的指令所定义，其主要职责是分析传入的用户消息，并将其委派给 Booker 或 Info 智能体。由于协调器定义了子智能体，这种委派由 Google ADK 的 Auto-Flow 机制自动处理。run_coordinator 函数设置了一个 InMemoryRunner,创建了用户和会话 ID,然后使用该运行器通过协调器智能体处理用户的请求。runner.run 方法处理请求并产出事件(yield events),代码从 event.content 中提取最终的响应文本。

主函数通过使用不同请求运行协调器来展示系统的用法，演示了系统如何将预订请求委派给 Booker,以及将信息请求委派给 Info。

## 速览

**是什么** 智能体系统(Agentic System)经常需要应对各种各样的输入和场景，这些输入和场景无法由单一的线性流程处理。简单的顺序工作流(Workflow)缺乏基于上下文进行决策的能力。如果没有为特定任务选择正确工具或子流程的机制，系统就会变得僵化且缺乏适应性。这一局限使得构建能够应对真实世界用户请求的复杂性、多样性的成熟应用变得困难。

为什么 

路由(Routing)模式(Pattern)通过在智能体(Agent)的运行框架中引入条件逻辑，提供了一种标准化的解决方案。该模式使系统能够先分析传入的查询(query)，以判定其意图或性质。智能体根据此分析结果，将控制流动态地导向最合适的专用工具、函数或子智能体(sub-agent)。这一决策可由多种方法驱动，包括提示大语言模型(LLM)、套用预定义规则，或采用基于嵌入(Embedding)的语义相似度计算。最终，路由将一条静态的、预先确定的执行路径，转变为能够选取最优动作的、灵活且具备上下文感知能力的工作流(Workflow)。

**经验法则** 当智能体必须根据用户输入或当前状态在多个不同的工作流、工具或子智能体之间做出决策时，应使用路由(Routing)模式。对于需要对传入请求进行分流或分类以处理不同类型任务的应用而言，该模式至关重要，例如客户支持机器人需要区分销售咨询、技术支持和账户管理问题。

**可视化摘要(图 2.1)**

**核心要点**

- 路由(Routing)使智能体能够根据条件，在工作流中动态决定下一步操作。
- 它允许智能体处理多样化的输入并调整自身行为，跳出线性执行的局限。
- 路由逻辑可以使用 LLM、基于规则的系统或嵌入相似度来实现。
- LangGraph 和 Google ADK 等框架为智能体工作流中路由的定义与管理提供了结构化方式，尽管它们采用了不同的架构思路。

## 结论

路由(Routing)模式是构建真正动态且响应式智能体系统(Agentic System)的关键一步。通过实现路由，我们超越了简单、线性的执行流程，使智能体能够就如何处理信息、响应用户输入以及利用可用工具或子智能体做出智能决策。

我们已经看到路由可以应用于各种领域，从客户服务聊天机器人到复杂的数据处理流水线。分析输入并有条件地引导工作流的能力，是创建能够处理真实世界任务内在可变性的智能体的基础。

使用 LangChain 和 Google ADK 的代码示例展示了两种不同但有效的路由实现方法。LangGraph 基于图的结构提供了一种可视化且显式的方式来定义状态和转换，这使其非常适合具有复杂路由逻辑的多步骤工作流。另一方面，Google ADK 通常侧重于定义不同的能力(工具),并依赖框架将用户请求路由到相应工具处理程序的能力，这对于具有明确定义的离散动作集的智能体而言可能更为简单。

掌握路由模式对于构建能够智能应对不同场景、并根据上下文提供量身定制的响应或动作的智能体至关重要。这是创建多功能且健壮的智能体应用程序的关键组件。

## 参考文献

- Google Agent Developer Kit Documentation: https://google.github.io/adk-docs/
- LangGraph Documentation: https://www.langchain.com/
