from dataclasses import dataclass


@dataclass(frozen=True)
class AiMetadata:
    is_ai_generated: bool

    @classmethod
    def create_non_ai_generated(cls) -> "AiMetadata":
        return cls(is_ai_generated=False)

    @classmethod
    def create_ai_generated(cls) -> "AiMetadata":
        return cls(is_ai_generated=True)

    @classmethod
    def from_dict(cls, data: dict) -> "AiMetadata":
        return cls(is_ai_generated=data["is_ai_generated"])

    def to_dict(self) -> dict:
        return {"is_ai_generated": self.is_ai_generated}
