import streamlit as st

from chatbot import get_response

st.set_page_config(page_title="LangChain Multi-Chain Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 LangChain Chatbot")
st.caption("RunnableBranch • RunnableParallel • Pydantic Structured Output")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("About")
    st.write(
        "This chatbot classifies your question and routes it through a "
        "**RunnableBranch** (Programming / Math / General). A "
        "**RunnableParallel** step then generates the main answer, "
        "keywords, and follow-up questions all at once. Everything is "
        "assembled into a validated **Pydantic** structured response."
    )
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


def render_structured_panel(data: dict) -> None:
    with st.expander("📋 Structured Output"):
        col1, col2 = st.columns(2)
        col1.metric("Category", data.get("category", "-"))
        col2.metric("Confidence", f"{data.get('confidence', 0):.2f}")
        st.markdown(f"**Summary:** {data.get('summary', '')}")
        st.markdown(f"**Keywords:** {', '.join(data.get('keywords', []))}")
        followups = data.get("follow_up_questions") or []
        if followups:
            st.markdown("**Follow-up questions:**")
            for q in followups:
                st.markdown(f"- {q}")


# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("structured"):
            render_structured_panel(msg["structured"])

# Chat input
user_input = st.chat_input("Ask me a programming, math, or general question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_response(user_input)
                st.markdown(response["answer"])
                render_structured_panel(response)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response["answer"],
                        "structured": response,
                    }
                )
            except Exception as exc: 
                error_msg = f"⚠️ Something went wrong: {exc}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
