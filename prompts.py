from langchain_core.prompts import PromptTemplate


PROGRAMMING_PROMPT = PromptTemplate.from_template(
    """You are a patient programming assistant. Answer the user's question with a practical
explanation. Include a small code example only when it makes the answer clearer.

Question: {question}"""
)

MATH_PROMPT = PromptTemplate.from_template(
    """You are a precise math tutor. Solve the problem step by step, state important
assumptions, and make the final result easy to find.

Question: {question}"""
)

GENERAL_PROMPT = PromptTemplate.from_template(
    """You are a clear, friendly general assistant. Give a direct, useful answer. If the
question needs current or specialized verification, say what should be checked.

Question: {question}"""
)

ENRICHMENT_PROMPT = PromptTemplate.from_template(
    """Analyze the following user question and prepare supporting information for a chatbot
answer. Keep the summary concise, provide a realistic confidence score, and return 3-5 keywords.

Question: {question}"""
)

