# 第 29 章 结语

<!-- chapter: 29 | en_title: Conclusion | part: II | pages: 439-447 | toc_page: 413 -->

                                     Conclusion


Throughout this book we have journeyed from the foundational concepts of
agentic AI to the practical implementation of sophisticated, autonomous sys-
tems. We began with the premise that building intelligent agents is akin to
creating a complex work of art on a technical canvas—a process that requires
not just a powerful cognitive engine like a large language model, but also a
robust set of architectural blueprints. These blueprints, or agentic patterns,
provide the structure and reliability needed to transform simple, reactive
models into proactive, goal-oriented entities capable of complex reasoning
and action.
   This concluding chapter will synthesize the core principles we have explored.
We will first review the key agentic patterns, grouping them into a cohesive
framework that underscores their collective importance. Next, we will exam-
ine how these individual patterns can be composed into more complex sys-
tems, creating a powerful synergy. Finally, we will look ahead to the future of
agent development, exploring the emerging trends and challenges that will
shape the next generation of intelligent systems.


Review of Key Agentic Principles
The 21 patterns detailed in this guide represent a comprehensive toolkit for
agent development. While each pattern addresses a specific design challenge,
they can be understood collectively by grouping them into foundational cat-
egories that mirror the core competencies of an intelligent agent.


© The Author(s), under exclusive license to Springer Nature Switzerland AG 2025   413
A. Gullí, Agentic Design Patterns, https://doi.org/10.1007/978-3-032-01402-3_29

1. Core Execution and Task Decomposition: At the most fundamental
   level, agents must be able to execute tasks. The patterns of Prompt
   Chaining, Routing, Parallelization, and Planning form the bedrock of an
   agent’s ability to act. Prompt Chaining provides a simple yet powerful
   method for breaking down a problem into a linear sequence of discrete
   steps, ensuring that the output of one operation logically informs the next.
   When workflows require more dynamic behavior, Routing introduces con-
   ditional logic, allowing an agent to select the most appropriate path or tool
   based on the context of the input. Parallelization optimizes efficiency by
   enabling the concurrent execution of independent sub-tasks, while the
   Planning pattern elevates the agent from a mere executor to a strategist,
   capable of formulating a multi-step plan to achieve a high-level objective.
2. Interaction with the External Environment: An agent’s utility is signifi-
   cantly enhanced by its ability to interact with the world beyond its imme-
   diate internal state. The Tool Use (Function Calling) pattern is paramount
   here, providing the mechanism for agents to leverage external APIs, data-
   bases, and other software systems. This grounds the agent’s operations in
   real-world data and capabilities. To effectively use these tools, agents must
   often access specific, relevant information from vast repositories. The
   Knowledge Retrieval pattern, particularly Retrieval-Augmented Generation
   (RAG), addresses this by enabling agents to query knowledge bases and
   incorporate that information into their responses, making them more
   accurate and contextually aware.
3. State, Learning, and Self-Improvement: For an agent to perform more
   than just single-turn tasks, it must possess the ability to maintain context
   and improve over time. The Memory Management pattern is crucial for
   endowing agents with both short-term conversational context and long-­
   term knowledge retention. Beyond simple memory, truly intelligent agents
   exhibit the capacity for self-improvement. The Reflection and Self-­
   Correction patterns enable an agent to critique its own output, identify
   errors or shortcomings, and iteratively refine its work, leading to a higher
   quality final result. The Learning and Adaptation pattern takes this a step
   further, allowing an agent’s behavior to evolve based on feedback and expe-
   rience, making it more effective over time.
4. Collaboration and Communication: Many complex problems are best
   solved through collaboration. The Multi-Agent Collaboration pattern
   allows for the creation of systems where multiple specialized agents, each
   with a distinct role and set of capabilities, work together to achieve a com-
   mon goal. This division of labor enables the system to tackle multifaceted
   problems that would be intractable for a single agent. The effectiveness of

   such systems hinges on clear and efficient communication, a challenge
   addressed by the Inter-Agent Communication (A2A) and Model Context
   Protocol (MCP) patterns, which aim to standardize how agents and tools
   exchange information.

These principles, when applied through their respective patterns, provide a
robust framework for building intelligent systems. They guide the developer
in creating agents that are not only capable of performing complex tasks but
are also structured, reliable, and adaptable.


Combining Patterns for Complex Systems
The true power of agentic design emerges not from the application of a single
pattern in isolation, but from the artful composition of multiple patterns to
create sophisticated, multi-layered systems. The agentic canvas is rarely popu-
lated by a single, simple workflow; instead, it becomes a tapestry of intercon-
nected patterns that work in concert to achieve a complex objective.
   Consider the development of an autonomous AI research assistant, a task
that requires a combination of planning, information retrieval, analysis, and
synthesis. Such a system would be a prime example of pattern composition:

• Initial Planning: A user query, such as “Analyze the impact of quantum
  computing on the cybersecurity landscape,” would first be received by a
  Planner agent. This agent would leverage the Planning pattern to decom-
  pose the high-level request into a structured, multi-step research plan. This
  plan might include steps like “Identify foundational concepts of quantum
  computing,” “Research common cryptographic algorithms,” “Find expert
  analysis on quantum threats to cryptography,” and “Synthesize findings
  into a structured report.”
• Information Gathering with Tool Use: To execute this plan, the agent
  would rely heavily on the Tool Use pattern. Each step of the plan would
  trigger a call to a Google Search or vertex_ai_search tool. For more struc-
  tured data, it might use tools to query academic databases like ArXiv or
  financial data APIs.
• Collaborative Analysis and Writing: A single agent might handle this,
  but a more robust architecture would employ Multi-Agent Collaboration.
  A “Researcher” agent could be responsible for executing the search plan
  and gathering raw information. Its output—a collection of summaries and
  source links—would then be passed to a “Writer” agent. This specialist

  agent, using the initial plan as its outline, would synthesize the collected
  information into a coherent draft.
• Iterative Reflection and Refinement: A first draft is rarely perfect. The
  Reflection pattern could be implemented by introducing a third “Critic”
  agent. This agent’s sole purpose would be to review the Writer’s draft,
  checking for logical inconsistencies, factual inaccuracies, or areas lacking
  clarity. Its critique would be fed back to the Writer agent, which would
  then leverage the Self-Correction pattern to refine its output, incorporating
  the feedback to produce a higher-quality final report.
• State Management: Throughout this entire process, a Memory
  Management system would be essential. It would maintain the state of the
  research plan, store the information gathered by the Researcher, hold the
  drafts created by the Writer, and track the feedback from the Critic, ensur-
  ing that context is preserved across the entire multi-step, multi-
  agent workflow.

In this example, at least five distinct agentic patterns are woven together. The
Planning pattern provides the high-level structure, Tool Use grounds the
operation in real-world data, Multi-Agent Collaboration enables specializa-
tion and division of labor, Reflection ensures quality, and Memory
Management maintains coherence. This composition transforms a set of indi-
vidual capabilities into a powerful, autonomous system capable of tackling a
task that would be far too complex for a single prompt or a simple chain.


Looking to the Future
The composition of agentic patterns into complex systems, as illustrated by
our AI research assistant, is not the end of the story but rather the beginning
of a new chapter in software development. As we look ahead, several emerging
trends and challenges will define the next generation of intelligent systems,
pushing the boundaries of what is possible and demanding even greater
sophistication from their creators.
   The journey toward more advanced agentic AI will be marked by a drive for
greater autonomy and reasoning. The patterns we have discussed provide the
scaffolding for goal-oriented behavior, but the future will require agents that
can navigate ambiguity, perform abstract and causal reasoning, and even
exhibit a degree of common sense. This will likely involve tighter integration
with novel model architectures and neuro-symbolic approaches that blend the
pattern-matching strengths of LLMs with the logical rigor of classical AI. We

will see a shift from human-in-the-loop systems, where the agent is a co-pilot,
to human-on-the-loop systems, where agents are trusted to execute complex,
long-running tasks with minimal oversight, reporting back only when the
objective is complete or a critical exception occurs.
   This evolution will be accompanied by the rise of agentic ecosystems and
standardization. The Multi-Agent Collaboration pattern highlights the
power of specialized agents, and the future will see the emergence of open
marketplaces and platforms where developers can deploy, discover, and
orchestrate fleets of agents-as-a-service. For this to succeed, the principles
behind the Model Context Protocol (MCP) and Inter-Agent Communication
(A2A) will become paramount, leading to industry-wide standards for how
agents, tools, and models exchange not just data, but also context, goals, and
capabilities.
   A prime example of this growing ecosystem is the “Awesome Agents”
GitHub repository, a valuable resource that serves as a curated list of open-­
source AI agents, frameworks, and tools. It showcases the rapid innovation in
the field by organizing cutting-edge projects for applications ranging from
software development to autonomous research and conversational AI.
   However, this path is not without its formidable challenges. The core issues
of safety, alignment, and robustness will become even more critical as agents
become more autonomous and interconnected. How do we ensure an agent’s
learning and adaptation do not cause it to drift from its original purpose?
How do we build systems that are resilient to adversarial attacks and unpre-
dictable real-world scenarios? Answering these questions will require a new set
of “safety patterns” and a rigorous engineering discipline focused on testing,
validation, and ethical alignment.


Final Thoughts
Throughout this guide, we have framed the construction of intelligent agents
as an art form practiced on a technical canvas. These Agentic Design patterns
are your palette and your brushstrokes: the foundational elements that allow
you to move beyond simple prompts and create dynamic, responsive, and
goal-oriented entities. They provide the architectural discipline needed to
transform the raw cognitive power of a large language model into a reliable
and purposeful system.
   The true craft lies not in mastering a single pattern but in understanding
their interplay: in seeing the canvas as a whole and composing a system where
planning, tool use, reflection, and collaboration work in harmony. The

principles of agentic design are the grammar of a new language of creation,
one that allows us to instruct machines not just on what to do, but on
how to be.
   The field of agentic AI is one of the most exciting and rapidly evolving
domains in technology. The concepts and patterns detailed here are not a
final, static dogma but a starting point—a solid foundation upon which to
build, experiment, and innovate. The future is not one where we are simply
users of AI, but one where we are the architects of intelligent systems that will
help us solve the world’s most complex problems. The canvas is before you,
the patterns are in your hands. Now, it is time to build.

                                          Glossary


Fundamental Concepts
Prompt A prompt is the input, typically in the form of a question, instruction, or
   statement, that a user provides to an AI model to elicit a response. The quality and
   structure of the prompt heavily influence the model’s output, making prompt
   engineering a key skill for effectively using AI.
Context Window The context window is the maximum number of tokens an AI
   model can process at once, including both the input and its generated output.
   This fixed size is a critical limitation, as information outside the window is ignored,
   while larger windows enable more complex conversations and document analysis.
In-Context Learning In-context learning is an AI’s ability to learn a new task from
   examples provided directly in the prompt, without requiring any retraining. This
   powerful feature allows a single, general-purpose model to be adapted to countless
   specific tasks on the fly.
Zero-Shot, One-Shot, and Few-Shot Prompting These are prompting techniques where a
   model is given zero, one, or a few examples of a task to guide its response. Providing
   more examples generally helps the model better understand the user’s intent and
   improves its accuracy for the specific task.
Multimodality Multimodality is an AI’s ability to understand and process information
   across multiple data types like text, images, and audio. This allows for more versa-
   tile and human-like interactions, such as describing an image or answering a spo-
   ken question.
Grounding Grounding is the process of connecting a model’s outputs to verifiable,
   real-world information sources to ensure factual accuracy and reduce ­hallucinations.


© The Editor(s) (if applicable) and The Author(s), under exclusive license to Springer Nature   419
Switzerland AG 2025
A. Gullí, Agentic Design Patterns, https://doi.org/10.1007/978-3-032-01402-3

420           Glossary

    This is often achieved with techniques like RAG to make AI systems more
    trustworthy.


Core AI Model Architectures
Transformers The Transformer is the foundational neural network architecture for
   most modern LLMs. Its key innovation is the self-attention mechanism, which
   efficiently processes long sequences of text and captures complex relationships
   between words.
Recurrent Neural Network (RNN) The Recurrent Neural Network is a foundational
   architecture that preceded the Transformer. RNNs process information sequen-
   tially, using loops to maintain a “memory” of previous inputs, which made them
   suitable for tasks like text and speech processing.
Mixture of Experts (MoE) Mixture of Experts is an efficient model architecture where
   a “router” network dynamically selects a small subset of “expert” networks to han-
   dle any given input. This allows models to have a massive number of parameters
   while keeping computational costs manageable.
Diffusion Models Diffusion models are generative models that excel at creating high-­
   quality images. They work by adding random noise to data and then training a
   model to meticulously reverse the process, allowing them to generate novel data
   from a random starting point.
Mamba Mamba is a recent AI architecture using a Selective State Space Model (SSM)
   to process sequences with high efficiency, especially for very long contexts. Its
   selective mechanism allows it to focus on relevant information while filtering out
   noise, making it a potential alternative to the Transformer.


The LLM Development Lifecycle1
Pre-training Techniques Pre-training is the initial phase where a model learns general
    knowledge from vast amounts of data. The top techniques for this involve differ-
    ent objectives for the model to learn from. The most common is Causal Language
    Modeling (CLM), where the model predicts the next word in a sentence. Another
    is Masked Language Modeling (MLM), where the model fills in intentionally hid-
    den words in a text. Other important methods include Denoising Objectives,

1
 The development of a powerful language model follows a distinct sequence. It begins with Pre-training,
where a massive base model is built by training it on a vast dataset of general internet text to learn lan-
guage, reasoning, and world knowledge. Next is Fine-tuning, a specialization phase where the general
model is further trained on smaller, task-specific datasets to adapt its capabilities for a particular purpose.
The final stage is Alignment, where the specialized model’s behavior is adjusted to ensure its outputs are
helpful, harmless, and aligned with human values.

   where the model learns to restore a corrupted input to its original state, Contrastive
   Learning, where it learns to distinguish between similar and dissimilar pieces of
   data, and Next Sentence Prediction (NSP), where it determines if two sentences
   logically follow each other.
Fine-tuning Techniques Fine-tuning is the process of adapting a general pre-trained
   model to a specific task using a smaller, specialized dataset. The most common
   approach is Supervised Fine-Tuning (SFT), where the model is trained on labeled
   examples of correct input-output pairs. A popular variant is Instruction Tuning,
   which focuses on training the model to better follow user commands. To make
   this process more efficient, Parameter-Efficient Fine-Tuning (PEFT) methods are
   used, with top techniques including LoRA (Low-Rank Adaptation), which only
   updates a small number of parameters, and its memory-optimized version,
   QLoRA. Another technique, Retrieval-Augmented Generation (RAG), enhances
   the model by connecting it to an external knowledge source during the fine-­tuning
   or inference stage.
Alignment and Safety Techniques Alignment is the process of ensuring an AI model’s
   behavior aligns with human values and expectations, making it helpful and harm-
   less. The most prominent technique is Reinforcement Learning from Human
   Feedback (RLHF), where a “reward model” trained on human preferences guides
   the AI’s learning process, often using an algorithm like Proximal Policy
   Optimization (PPO) for stability. Simpler alternatives have emerged, such as
   Direct Preference Optimization (DPO), which bypasses the need for a separate
   reward model, and Kahneman-Tversky Optimization (KTO), which simplifies
   data collection further. To ensure safe deployment, Guardrails are implemented as
   a final safety layer to filter outputs and block harmful actions in real-time.


Enhancing AI Agent Capabilities
Chain of Thought (CoT) This prompting technique encourages a model to explain its
   reasoning step-by-step before giving a final answer. This process of “thinking out
   loud” often leads to more accurate results on complex reasoning tasks.
Tree of Thoughts (ToT) Tree of Thoughts is an advanced reasoning framework where
   an agent explores multiple reasoning paths simultaneously, like branches on a tree.
   It allows the agent to self-evaluate different lines of thought and choose the most
   promising one to pursue, making it more effective at complex problem-solving.
ReAct (Reason and Act) ReAct is an agent framework that combines reasoning and
   acting in a loop. The agent first “thinks” about what to do, then takes an “action”
   using a tool, and uses the resulting observation to inform its next thought, making
   it highly effective at solving complex tasks.
