"""Chat interface for the rag-multimodal-2026 Streamlit app.

Shows the answer, any images that were retrieved and used (with their captions),
and a trace of the multimodal retrieval, so the text and image sources are both
visible rather than hidden.
"""

import base64

import streamlit as st

from frontend import api_utils

_STEP_LABEL = {
    "retrieve": "Retrieve text and images",
    "grounded_answer": "Grounded answer",
}


def _image_bytes(data_uri: str) -> bytes:
    return base64.b64decode(data_uri.split(",", 1)[1])


def _render_images(images) -> None:
    if not images:
        return
    st.caption("Images used")
    columns = st.columns(min(len(images), 2))
    for index, image in enumerate(images):
        with columns[index % len(columns)]:
            try:
                st.image(
                    _image_bytes(image["data_uri"]), caption=image.get("filename", "")
                )
            except Exception:
                st.caption(image.get("filename", ""))


def _render_trace(steps, sources) -> None:
    if not steps:
        return
    retrieve = next((s for s in steps if s.get("step") == "retrieve"), {})
    header = (
        f"Multimodal retrieval: {retrieve.get('text', 0)} text, "
        f"{retrieve.get('images', 0)} image"
    )
    with st.expander(header, expanded=False):
        path = ", ".join(
            _STEP_LABEL.get(step.get("step"), step.get("step", "")) for step in steps
        )
        st.caption(path)
        if sources:
            st.markdown("**Sources:** " + ", ".join(sources))


def display_chat_interface() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("images"):
                _render_images(message["images"])
            if message.get("steps"):
                _render_trace(message["steps"], message.get("sources", []))

    prompt = st.chat_input("Ask about your documents and images")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = st.session_state.get("model", "qwen2.5:7b-instruct")
        with st.spinner("Searching text and images..."):
            try:
                result = api_utils.chat(prompt, st.session_state.session_id, model)
            except Exception as exc:
                st.error(f"Request failed: {exc}")
                return
        st.session_state.session_id = result.get("session_id")
        answer = result.get("answer", "")
        st.markdown(answer)
        _render_images(result.get("images", []))
        _render_trace(result.get("steps", []), result.get("sources", []))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "images": result.get("images", []),
            "steps": result.get("steps", []),
            "sources": result.get("sources", []),
        }
    )
