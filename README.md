# LangChain Chatbot — RunnableBranch & RunnableParallel

A Streamlit chatbot built with the latest LangChain Expression Language (LCEL)
APIs, demonstrating `RunnableBranch`, `RunnableParallel`, and Pydantic
structured output.

## Features

- 💬 Streamlit chat interface with persistent chat history
- 🌳 **RunnableBranch** — routes each question to a Programming Assistant,
  Math Tutor, or General Assistant prompt pipeline based on its category
- ⚡ **RunnableParallel** — generates the main answer, keywords, and
  follow-up questions concurrently from a single user request
- ✅ **Pydantic structured output** — every response is validated against a
  `ChatResponse` schema (`answer`, `summary`, `category`, `confidence`,
  `keywords`, `follow_up_questions`) before it reaches the UI
- 🔑 API keys loaded from a `.env` file — never hardcoded
- 🗑️ Optional "Clear Chat" button

## Project Structure

```
project/
│
├── app.py              # Streamlit UI
├── chatbot.py           # RunnableBranch + RunnableParallel + structured output pipeline
├── prompts.py           # All PromptTemplates
├── schemas.py            # Pydantic ChatResponse schema
├── requirements.txt
├── .env.example
├── README.md
└── assets/
```

## How it works

### 1. Classification
Every question first goes through a small classification chain that labels
it as `programming`, `mathematics`, or `general`.

### 2. RunnableBranch
```python
answer_branch = RunnableBranch(
    (lambda x: x["category"] == "programming", programming_chain),
    (lambda x: x["category"] == "mathematics", math_chain),
    general_chain,  # default branch
)
```
Based on the classified category, the question is routed to the matching
domain-specific prompt pipeline (Programming Assistant, Math Tutor, or
General Assistant).

### 3. RunnableParallel
```python
parallel_chain = RunnableParallel(
    answer=answer_branch,
    keywords=keywords_chain,
    followup=followup_chain,
)
```
The branch output (main answer), a keyword extractor, and a follow-up
question generator all run **simultaneously** from the same user input.

### 4. Pydantic Structured Output
```python
structured_llm = llm.with_structured_output(ChatResponse)
format_chain = format_prompt | structured_llm
```
The parallel results are fed into one final LLM call that is constrained to
return a validated `ChatResponse` object — not a raw string — which is then
rendered in the Streamlit UI.

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and add your `GROQ_API_KEY` (or switch `get_llm()` in
   `chatbot.py` to another provider, e.g. `ChatOpenAI`, and add the matching
   key).

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Switching LLM Providers

`chatbot.py` centralizes model creation in `get_llm()`. To use OpenAI,
Gemini, or a HuggingFace endpoint instead of Groq, swap the model class and
its key, for example:

```python
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=os.getenv("OPENAI_API_KEY"))
```

## Notes

- `.env` is git-ignored — never commit real API keys.
- The response schema in `schemas.py` can be extended with additional
  fields as needed.
