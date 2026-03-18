import time
import logging
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import OutboxEventDB
from app.schemas import OutboxEventStatus

logger = logging.getLogger(__name__)

MAX_RETRIES = 5


def process_outbox_events():
    logger.info("Iniciando Worker...")

    while True:
        db: Session = SessionLocal()
        try:
            events = (
                db.query(OutboxEventDB)
                .filter(OutboxEventDB.status == OutboxEventStatus.PENDING)
                .limit(10)
                .all()
            )

            for event in events:
                logger.info(f"Pocessando envento {event.id} | {event.event_type}")

                try:
                    logger.info(
                        f"Enviando e-mails para: {event.payload.get('participants')}"
                    )

                    event.status = OutboxEventStatus.PROCESSED

                except Exception as e:
                    logger.error(f"Erro ao enviar e-mail do envento {event.id}")
                    event.retries += 1

                    if event.retries >= MAX_RETRIES:
                        event.status = OutboxEventStatus.FAILED
                        logger.error(
                            f"Número máximo de tentativas excedida! Abortando permanentemente envio do envento {event.id}!"
                        )
                        raise e
            if events:
                db.commit()

        except Exception as e:
            logger.error("Erro no banco de dados!")
            db.rollback()

            raise e
        finally:
            db.close()

        time.sleep(5)


if __name__ == "__main__":
    process_outbox_events()
