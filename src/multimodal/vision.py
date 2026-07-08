"""Vision helpers for UltimateRAG, using a local Ollama vision model.

At index time a vision model reads each image and writes a detailed caption, so
images become first class, searchable content alongside text. Keyless: the model
runs on Ollama, no paid key.
"""

import logging

logger = logging.getLogger(__name__)

_CAPTION_PROMPT = (
    "Describe this image in detail for search and question answering. Include "
    "any title, labels, numbers, and what the image shows."
)


def caption_image(image_path: str, model: str, base_url: str) -> str:
    """Return a detailed text caption for an image, produced by the vision model."""
    import ollama

    client = ollama.Client(host=base_url)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": _CAPTION_PROMPT, "images": [image_path]}],
    )
    return response["message"]["content"].strip()
