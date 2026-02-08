from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainException(Exception):
    message: str
    stack_trace: str = ""
    code: UUID = field(default_factory=uuid4)

    def to_dict(self):
        return {
            "message": self.message,
            "stack_trace": self.stack_trace,
            "code": str(self.code),
        }
