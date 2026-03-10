from datetime import datetime

from .base import BaseModel


class EmulatorSchema(BaseModel):
    id: int
    name: str
    slug: str

    file_name: str
    file_name_no_tags: str
    file_name_no_ext: str
    file_extension: str
    file_path: str
    file_size_bytes: int

    summary: str | None = ""
    path_cover_small: str
    path_cover_large: str
    merged_screenshots: list[str]

    platform_ids: list[int]
    missing_from_fs: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BuildSchema(BaseModel):
    id: int
    name: str
    slug: str

    file_name: str
    file_name_no_tags: str
    file_name_no_ext: str
    file_extension: str
    file_path: str
    file_size_bytes: int

    summary: str | None = ""
    path_cover_small: str
    path_cover_large: str
    merged_screenshots: list[str]

    missing_from_fs: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
