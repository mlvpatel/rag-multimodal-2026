"""rag-multimodal-2026 Streamlit application entry point."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st  # noqa: E402

from frontend.chat_interface import display_chat_interface  # noqa: E402
from frontend.sidebar import display_sidebar  # noqa: E402


def main() -> None:
    st.set_page_config(page_title="rag-multimodal-2026", layout="wide")
    st.title("rag-multimodal-2026")
    st.caption(
        "Multimodal RAG, 2026. Retrieves across text and images at once, and "
        "shows the images it used to answer."
    )
    display_sidebar()
    display_chat_interface()


if __name__ == "__main__":
    main()
