from typing import Generic, TypeVar

from pydantic import BaseModel

T_ID = TypeVar("T_ID")
T = TypeVar("T")


class OutputId(BaseModel, Generic[T_ID]):
    id: T_ID


class OutputData(BaseModel, Generic[T]):
    data: T