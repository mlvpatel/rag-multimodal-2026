"""Unit tests for the indexing task (no broker, no database)."""

import src.worker.tasks as tasks


def test_process_document_inserts_record_before_indexing(monkeypatch):
    order = []
    monkeypatch.setattr(
        tasks, "insert_document_record", lambda filename: order.append("insert") or 5
    )
    monkeypatch.setattr(
        tasks,
        "index_document",
        lambda path, file_id, filename: order.append(("index", file_id)) or True,
    )

    result = tasks.process_document("/tmp/chart.png", "chart.png")

    assert order == ["insert", ("index", 5)]
    assert result == {"status": "completed", "file_id": 5}


def test_process_document_rolls_back_the_record_when_indexing_fails(monkeypatch):
    deleted = []
    monkeypatch.setattr(tasks, "insert_document_record", lambda filename: 9)
    monkeypatch.setattr(tasks, "index_document", lambda path, file_id, filename: False)
    monkeypatch.setattr(
        tasks, "delete_document_record", lambda file_id: deleted.append(file_id) or True
    )

    result = tasks.process_document("/tmp/chart.png", "chart.png")

    assert result == {"status": "failed", "file_id": 9}
    assert deleted == [9]
