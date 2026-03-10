from abc import abstractmethod, ABC
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy import and_, or_
from datetime import datetime

from context.booking.domain.entity.booking import Booking, BookingStatus
from libs.repo import Repository


class BookingRepoAbstrato(Repository, ABC):
    @abstractmethod
    def search_by_id(self, id: UUID) -> Optional[Booking]:
        pass

    @abstractmethod
    def list(self) -> Optional[List[Booking]]:
        pass

    @abstractmethod
    def add(self, booking: Booking) -> Optional[Booking]:
        pass

    @abstractmethod
    def put(self, booking: Booking) -> Optional[Booking]:
        pass

    @abstractmethod
    def check_overlap(self, room_id: UUID, start_at: datetime, end_at: datetime, exclude_id: UUID = None) -> bool:
        pass


class BookingRepo(BookingRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def add(self, booking: Booking) -> Optional[Booking]:
        self.session.add(booking)
        return booking

    def put(self, booking: Booking) -> Optional[Booking]:
        self.session.merge(booking)
        return booking

    def search_by_id(self, id: UUID) -> Optional[Booking]:
        query = self.session.query(Booking)
        query = query.filter(Booking.id == id)
        booking = query.first()
        return booking

    def list(self) -> Optional[List[Booking]]:
        consulta = self.session.query(Booking)
        bookings = consulta.all()
        return bookings

    def check_overlap(self, room_id: UUID, start_at: datetime, end_at: datetime, exclude_id: UUID = None) -> bool:
        query = self.session.query(Booking).filter(
            and_(
                Booking.room_id == room_id,
                Booking.status == BookingStatus.ACTIVE,
                or_(
                    and_(Booking.start_at < end_at, Booking.end_at > start_at),
                )
            )
        )
        if exclude_id:
            query = query.filter(Booking.id != exclude_id)
        return query.first() is not None