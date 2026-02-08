from enum import Enum


class MatureRating(str, Enum):
    PG = "pg"
    PG_13 = "pg-13"
    R = "r"
    X = "x"
    XXX = "xxx"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"
