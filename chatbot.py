import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableParallel
from langchain_groq import ChatGroq

from prompts import (
    classification_prompt,
    followup_prompt,
    format_prompt,
    general_prompt,
    keywords_prompt,
    math_prompt,
    programming_prompt,
)
from schemas import ChatResponse

load_dotenv()


def get_llm():
    """
    Returns the chat model used across the app (FR-1).

    Swap this for ChatOpenAI, ChatGoogleGenerativeAI, HuggingFaceEndpoint,
    etc. if you'd rather use a different provider — just add the matching
    key to your .env file.
    """
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "gemma-7b-it"),
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY"),
    )


llm = get_llm()


# Step 1 — classify

classification_chain = classification_prompt | llm | StrOutputParser()


def normalize_category(raw_category: str) -> str:
    text = raw_category.strip().lower()
    if "program" in text or "code" in text:
        return "programming"
    if "math" in text:
        return "mathematics"
    return "general"



# Step 2 : RunnableBranch 

programming_chain = programming_prompt | llm | StrOutputParser()
math_chain = math_prompt | llm | StrOutputParser()
general_chain = general_prompt | llm | StrOutputParser()

answer_branch = RunnableBranch(
    (lambda x: x["category"] == "programming", programming_chain),
    (lambda x: x["category"] == "mathematics", math_chain),
    general_chain,  
)


# Step 3: RunnableParallel 

keywords_chain = keywords_prompt | llm | StrOutputParser()
followup_chain = followup_prompt | llm | StrOutputParser()

parallel_chain = RunnableParallel(
    answer=answer_branch,
    keywords=keywords_chain,
    followup=followup_chain,
)


# Step 4 : Pydantic str

structured_llm = llm.with_structured_output(ChatResponse)
format_chain = format_prompt | structured_llm


def _parse_followup(raw_text: str) -> list[str]:
    """Best-effort split of the numbered follow-up text into a clean list."""
    lines = [line.strip(" -*0123456789.") for line in raw_text.strip().splitlines()]
    return [line for line in lines if line][:3]


def get_response(question: str) -> dict:
    """
    Run the full pipeline for a single user question and return a plain
    dict matching the ChatResponse schema, ready for the Streamlit UI.
    """
    raw_category = classification_chain.invoke({"question": question})
    category = normalize_category(raw_category)

    parallel_result = parallel_chain.invoke({"question": question, "category": category})

    structured: ChatResponse = format_chain.invoke(
        {
            "question": question,
            "answer": parallel_result["answer"],
            "keywords": parallel_result["keywords"],
            "followup": parallel_result["followup"],
        }
    )

    result = structured.model_dump()

    if not result.get("category"):
        result["category"] = category
    if not result.get("follow_up_questions"):
        result["follow_up_questions"] = _parse_followup(parallel_result["followup"])

    return result
