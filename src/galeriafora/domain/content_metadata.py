from dataclasses import dataclass
from typing import TypedDict

from galeriafora.domain.content_type import ContentType


class Dimensions(TypedDict):
    width: int
    height: int


@dataclass(frozen=True)
class ContentMetadata:
    content_type: ContentType
    dimensions: Dimensions
    file_size_bytes: int

    @property
    def aspect_ratio(self) -> float:
        return self.dimensions["width"] / self.dimensions["height"]

    @property
    def is_portrait(self) -> bool:
        return self.dimensions["height"] > self.dimensions["width"]

    @property
    def is_landscape(self) -> bool:
        return self.dimensions["width"] > self.dimensions["height"]

    @property
    def is_square(self) -> bool:
        return self.dimensions["width"] == self.dimensions["height"]

    @property
    def file_size_kb(self) -> float:
        return self.file_size_bytes / 1024

    @property
    def file_size_mb(self) -> float:
        return self.file_size_bytes / (1024 * 1024)

    @property
    def file_extension(self) -> str:
        match self.content_type:
            case ContentType.IMAGE_JPEG:
                return "jpg"
            case ContentType.IMAGE_PNG:
                return "png"
            case ContentType.GIF:
                return "gif"
            case ContentType.VIDEO_MP4:
                return "mp4"
            case _:
                return ""

    @classmethod
    def from_dict(cls, data: dict) -> "ContentMetadata":
        return cls(
            content_type=ContentType(data["content_type"]),
            dimensions=data["dimensions"],
            file_size_bytes=data["file_size_bytes"],
        )

    def to_dict(self) -> dict:
        return {
            "content_type": self.content_type.value,
            "dimensions": self.dimensions,
            "file_size_bytes": self.file_size_bytes,
        }
