from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_hash: str

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password_hash": self.password_hash,
        }
