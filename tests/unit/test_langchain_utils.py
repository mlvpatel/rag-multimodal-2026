"""Unit tests for the LLM helpers (no network)."""

from langchain_core.messages import AIMessage, HumanMessage

import src.core.langchain_utils as lu


def test_make_llm_routes_local_models_to_ollama(monkeypatch):
    monkeypatch.setattr(lu.settings, "ollama_base_url", "http://localhost:11434")
    monkeypatch.setattr(lu.settings, "ollama_num_ctx", 8192)
    llm = lu._make_llm("llama3.2:3b")
    assert llm.__class__.__name__ == "ChatOllama"


def test_to_lc_messages_maps_roles_to_message_types():
    history = [
        {"role": "human", "content": "hi"},
        {"role": "ai", "content": "hello"},
        {"role": "assistant", "content": "again"},
    ]
    messages = lu._to_lc_messages(history)
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert isinstance(messages[2], AIMessage)
    assert messages[0].content == "hi"


def test_to_lc_messages_empty_history_is_empty_list():
    assert lu._to_lc_messages(None) == []
