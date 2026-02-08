from enum import Enum


class ContentType(str, Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    VIDEO_MP4 = "video/mp4"
    VIDEO_WEBM = "video/webm"
    GIF = "image/gif"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"
