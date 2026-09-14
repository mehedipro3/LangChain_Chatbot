from langchain_core.prompts import PromptTemplate


# Classification prompt — categorizes the question
classification_prompt = PromptTemplate.from_template(
    """Classify the following question into one of these categories: Programming, Mathematics, or General.
Reply with just one word: the category.

Question: {question}"""
)

# Domain-specific answer prompts
programming_prompt = PromptTemplate.from_template(
    """You are a patient programming assistant. Answer the user's question with a practical
explanation. Include a small code example only when it makes the answer clearer.

Question: {question}"""
)

math_prompt = PromptTemplate.from_template(
    """You are a precise math tutor. Solve the problem step by step, state important
assumptions, and make the final result easy to find.

Question: {question}"""
)

general_prompt = PromptTemplate.from_template(
    """You are a clear, friendly general assistant. Give a direct, useful answer. If the
question needs current or specialized verification, say what should be checked.

Question: {question}"""
)

# Keywords extraction prompt
keywords_prompt = PromptTemplate.from_template(
    """Extract 3-5 key concepts from the following question as a comma-separated list.
Reply with only the keywords, no extra text.

Question: {question}"""
)

# Follow-up questions prompt
followup_prompt = PromptTemplate.from_template(
    """Generate 2-3 interesting follow-up questions based on this question:

Question: {question}

Format your response as a numbered list."""
)

# Format/Enrichment prompt for structured output
format_prompt = PromptTemplate.from_template(
    """Based on the user question and answer provided, generate:
1. A one-sentence summary of the answer
2. A confidence score from 0 to 100 indicating how well the answer addresses the question
3. Extract 3-5 key concepts from the answer
4. Generate 2-3 follow-up questions

Return the data in a structured format with:
- summary: (one sentence summary)
- confidence: (integer 0-100)
- keywords: (list of 3-5 keywords)
- follow_up_questions: (list of 2-3 follow-up questions)

Question: {question}
Answer: {answer}
Keywords: {keywords}
Follow-up: {followup}"""
)

