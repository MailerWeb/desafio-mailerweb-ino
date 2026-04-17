from datetime import datetime, timedelta

from app.domain.exceptions import BookingDurationError, InvalidDateError

MIN_DURATION = timedelta(minutes=15)
MAX_DURATION = timedelta(hours=8)


def validate_booking_dates(start_at: datetime, end_at: datetime) -> None:
    """
    Garante que:
    - Ambas as datas possuem timezone (ISO 8601)
    - start_at < end_at
    """
    if start_at.tzinfo is None or end_at.tzinfo is None:
        raise InvalidDateError("As datas devem conter timezone (ISO 8601).")
    if start_at >= end_at:
        raise InvalidDateError("start_at deve ser anterior a end_at.")


def validate_booking_duration(start_at: datetime, end_at: datetime) -> None:
    """
    Garante que a duração da reserva está entre 15 minutos e 8 horas.
    """
    duration = end_at - start_at
    if duration < MIN_DURATION:
        raise BookingDurationError(
            f"Duração mínima é de {int(MIN_DURATION.total_seconds() // 60)} minutos."
        )
    if duration > MAX_DURATION:
        raise BookingDurationError(
            f"Duração máxima é de {int(MAX_DURATION.total_seconds() // 3600)} horas."
        )


def validate_booking(start_at: datetime, end_at: datetime) -> None:
    """Executa todas as validações de data/duração em sequência."""
    validate_booking_dates(start_at, end_at)
    validate_booking_duration(start_at, end_at)
