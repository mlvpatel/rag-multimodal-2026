"""Unit tests for the multimodal engine helpers (no model, no database)."""

from src.multimodal.engine import is_image


def test_is_image_recognizes_image_extensions():
    assert is_image("chart.png")
    assert is_image("photo.JPG")
    assert is_image("diagram.jpeg")


def test_is_image_rejects_text_documents():
    assert not is_image("notes.txt")
    assert not is_image("report.pdf")
    assert not is_image("page.html")
