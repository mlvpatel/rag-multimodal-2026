"""Background task: asynchronously index a document or image for UltimateRAG."""

import logging

from src.api.db_utils import delete_document_record, insert_document_record
from src.multimodal.engine import index_document
from src.worker.celery_app import celery_app

logger = logging.getLogger("ultimaterag")


@celery_app.task(name="process_document")
def process_document(file_path: str, filename: str) -> dict:
    """Index a text document or an image.

    Ordering matters: the database record is inserted first so we get a real
    integer file_id, which tags every chunk or image stored for it. If indexing
    fails, the record is rolled back so we never list a document with nothing
    behind it.
    """
    file_id = insert_document_record(filename)
    indexed = index_document(file_path, file_id, filename)
    if not indexed:
        delete_document_record(file_id)
        logger.error("Indexing failed for %s, rolled back record %s", filename, file_id)
        return {"status": "failed", "file_id": file_id}
    return {"status": "completed", "file_id": file_id}
