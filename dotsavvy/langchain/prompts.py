from langchain.prompts import PromptTemplate

planner_prompt: str = """
First understand the context. Your aim is to help with conducting quality research, not
necessarily solving the problem at hand. Generalize the context, when the prompt is too
specific. Then, formulate a plan that solves (part of) the problem, while keeping the
context in mind. Output the plan starting with the header 'Plan:' and follow up by a
numbered list of steps. Be concise. If the task is a question, the final step should
almost always be 'Given the above steps taken, please respond to the users original
question'. At the end of your plan, say '<END_OF_PLAN>'
"""

summary_prompt = PromptTemplate(
    input_variables=["text", "citation", "question", "summary_length"],
    template="Summarize the text below to help answer a question. "
    "Do not directly answer the question, instead summarize "
    "to give evidence to help answer the question. Include direct quotes. "
    'Reply "Not applicable" if text is irrelevant. '
    "Use {summary_length}. At the end of your response, provide a score from 1-10 on a "
    "newline "
    "indicating relevance to question. Do not explain your score. "
    "\n\n"
    "{text}\n"
    "Extracted from {citation}\n"
    "Question: {question}\n"
    "Relevant Information Summary:",
)
