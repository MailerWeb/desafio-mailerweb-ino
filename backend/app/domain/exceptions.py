class DomainError(Exception):
    """Base para todas as exceções de domínio."""


class InvalidDateError(DomainError):
    """start_at >= end_at ou ausência de timezone."""


class BookingDurationError(DomainError):
    """Duração fora do intervalo permitido (15min–8h)."""


class OverlapError(DomainError):
    """Conflito de horário com reserva existente."""


class RoomNotFoundError(DomainError):
    """Sala não encontrada."""


class BookingNotFoundError(DomainError):
    """Reserva não encontrada."""


class BookingAlreadyCancelledError(DomainError):
    """Tentativa de cancelar uma reserva já cancelada."""


class UnauthorizedError(DomainError):
    """Usuário sem permissão para a operação."""
