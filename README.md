# LangChain Chatbot using RunnableBranch & RunnableParallel

A Streamlit chatbot that demonstrates current LangChain runnable composition with Groq. It routes questions to focused prompts, generates answer metadata concurrently, and validates the displayed result with Pydantic.

## Features

- Streamlit chat interface with session-based history and a clear-chat control.
- `PromptTemplate` variables for every model prompt; no prompt text is placed in `invoke()`.
- `RunnableBranch` for programming, mathematics, and general-question prompt pipelines.
- `RunnableParallel` for concurrent main-answer and enrichment generation from one question.
- Pydantic structured output via `ChatGroq.with_structured_output(...)`.
- Environment-based API-key configuration; `.env` is ignored by Git.

## Project layout

```
├── app.py          # Streamlit UI
├── chatbot.py      # Runnable graph and routing logic
├── prompts.py      # PromptTemplate definitions
├── schemas.py      # Pydantic response schemas
├── requirements.txt
└── .env.example
```

## How the runnable graph works

1. `RunnableBranch` examines the question and selects the programming, mathematics, or general `PromptTemplate`.
2. A structured answer model is run through that selected pipeline.
3. `RunnableParallel` runs the routed answer pipeline and a separate enrichment pipeline at the same time.
4. `ChatResponse` validates the combined result before Streamlit displays it.

The final structured schema contains `answer`, `summary`, `confidence`, `category`, and `keywords`. This is Pydantic validation, not a `StrOutputParser`.

## Installation

Requirements: Python 3.10+ and a Groq API key.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and replace `your_groq_api_key_here` with your own API key. The default model is `openai/gpt-oss-20b`; you may change `GROQ_MODEL` to another active Groq chat model your account can access.

## Run

```bash
streamlit run app.py
```

Open the local address printed by Streamlit, ask a question, then expand **Structured response** to inspect the validated Pydantic output.

## Security

Do not commit `.env`, API keys, or other credentials. The supplied `.gitignore` excludes common local secrets and virtual-environment files.
