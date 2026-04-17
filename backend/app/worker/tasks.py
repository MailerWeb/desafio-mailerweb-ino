from app.worker.celery_app import celery_app


@celery_app.task(name="process_pending_events")
def process_pending_events() -> None:
    """Processa eventos pendentes do outbox. Implementado na Fase 6."""
    pass
