from dataclasses import dataclass
from uuid import uuid4, UUID
from passlib.context import CryptContext
from libs.entity import Entity

@dataclass
class User(Entity):
    id: UUID
    name: str
    email: str
    password: str

    @classmethod
    def create(
        cls, name: str, email: str, password: str
    ) -> "User":
        return cls(
            id=uuid4(),
            name=name,
            email=email,
            password=cls.generate_password_hash(senha=password),
        )

    def verify_password(self, senha: str) -> bool:
        return self.verify_password_hash(senha)

    def verify_password_hash(self, senha_em_texto: str) -> bool:
        bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return bcrypt.verify(senha_em_texto, self.password)

    @staticmethod
    def generate_password_hash(senha: str) -> str:
        bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return bcrypt.hash(senha)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"