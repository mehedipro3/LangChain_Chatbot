from typing import Literal

from pydantic import BaseModel, Field


Category = Literal["programming", "mathematics", "general"]


class AnswerFragment(BaseModel):
    """The main answer produced by the branch selected for a question."""

    answer: str = Field(description="A helpful, accurate answer to the user's question.")


class EnrichmentFragment(BaseModel):
    """Supporting fields produced in parallel with the main answer."""

    summary: str = Field(description="A concise, one-sentence summary of the answer.")
    confidence: int = Field(ge=0, le=100, description="Confidence in the response from 0 to 100.")
    keywords: list[str] = Field(description="Three to five useful keywords.")


class ChatResponse(BaseModel):
    """Final validated response rendered by the Streamlit interface."""

    answer: str
    summary: str
    confidence: int = Field(ge=0, le=100)
    category: Category
    keywords: list[str]
    follow_up_questions: list[str] = Field(default_factory=list)

