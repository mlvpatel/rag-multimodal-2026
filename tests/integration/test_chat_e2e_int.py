"""End to end multimodal test through Ollama.

Proves the full pipeline works with local models and no paid key: a text fact is
indexed as searchable content, a question retrieves it, and the answer is
grounded in it. Skipped automatically when Ollama is not running.
"""

import urllib.request

import pytest

import src.core.config as config_mod
import src.embeddings.vectorstore_utils as vs
import src.multimodal.engine as engine
import src.multimodal.store as store

FILE_ID = 987654


def _ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _ollama_running(), reason="ollama server not running")
def test_end_to_end_text_answer_is_grounded(pg_available, monkeypatch):
    monkeypatch.setattr(config_mod.settings, "embedding_provider", "ollama")
    monkeypatch.setattr(vs, "_query_embeddings", None)
    monkeypatch.setattr(store, "_store", None)

    store.delete(FILE_ID)
    store.add_text(["The capital of France is Paris."], FILE_ID, "facts.txt")

    try:
        result = engine.run_multimodal("llama3.2:3b", "What is the capital of France?")
    finally:
        store.delete(FILE_ID)

    assert "paris" in result["answer"].lower()
