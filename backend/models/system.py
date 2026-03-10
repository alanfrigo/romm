from __future__ import annotations

import enum
from functools import cached_property
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import FRONTEND_RESOURCES_PATH
from models.base import (
    FILE_EXTENSION_MAX_LENGTH,
    FILE_NAME_MAX_LENGTH,
    FILE_PATH_MAX_LENGTH,
    BaseModel,
)
from utils.database import CustomJSON

if TYPE_CHECKING:
    from models.platform import Platform


class SystemType(enum.StrEnum):
    EMULATOR = "emulator"
    BUILD = "build"


class EmulatorPlatform(BaseModel):
    __tablename__ = "emulator_platforms"

    emulator_id: Mapped[int] = mapped_column(
        ForeignKey("emulators.id", ondelete="CASCADE"), primary_key=True
    )
    platform_id: Mapped[int] = mapped_column(
        ForeignKey("platforms.id", ondelete="CASCADE"), primary_key=True
    )


class Emulator(BaseModel):
    __tablename__ = "emulators"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=400))
    slug: Mapped[str] = mapped_column(String(length=200), unique=True)

    file_name: Mapped[str] = mapped_column(String(length=FILE_NAME_MAX_LENGTH))
    file_name_no_tags: Mapped[str] = mapped_column(
        String(length=FILE_NAME_MAX_LENGTH), default=""
    )
    file_name_no_ext: Mapped[str] = mapped_column(
        String(length=FILE_NAME_MAX_LENGTH), default=""
    )
    file_extension: Mapped[str] = mapped_column(
        String(length=FILE_EXTENSION_MAX_LENGTH), default=""
    )
    file_path: Mapped[str] = mapped_column(String(length=FILE_PATH_MAX_LENGTH))
    file_size_bytes: Mapped[int] = mapped_column(BigInteger(), default=0)

    summary: Mapped[str | None] = mapped_column(Text, default="")
    path_cover_s: Mapped[str | None] = mapped_column(Text, default="")
    path_cover_l: Mapped[str | None] = mapped_column(Text, default="")
    path_screenshots: Mapped[list[str] | None] = mapped_column(
        CustomJSON(), default=[]
    )

    missing_from_fs: Mapped[bool] = mapped_column(default=False, nullable=False)

    platforms: Mapped[list[Platform]] = relationship(
        "Platform",
        secondary="emulator_platforms",
        lazy="joined",
    )

    @cached_property
    def full_path(self) -> str:
        return f"{self.file_path}/{self.file_name}"

    @property
    def path_cover_small(self) -> str:
        return (
            f"{FRONTEND_RESOURCES_PATH}/{self.path_cover_s}?ts={self.updated_at}"
            if self.path_cover_s
            else ""
        )

    @property
    def path_cover_large(self) -> str:
        return (
            f"{FRONTEND_RESOURCES_PATH}/{self.path_cover_l}?ts={self.updated_at}"
            if self.path_cover_l
            else ""
        )

    @cached_property
    def merged_screenshots(self) -> list[str]:
        if self.path_screenshots:
            return [f"{FRONTEND_RESOURCES_PATH}/{s}" for s in self.path_screenshots]
        return []

    @property
    def platform_ids(self) -> list[int]:
        return [p.id for p in self.platforms]

    def __repr__(self) -> str:
        return f"Emulator: {self.name} ({self.slug}) ({self.id})"


class Build(BaseModel):
    __tablename__ = "builds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=400))
    slug: Mapped[str] = mapped_column(String(length=200), unique=True)

    file_name: Mapped[str] = mapped_column(String(length=FILE_NAME_MAX_LENGTH))
    file_name_no_tags: Mapped[str] = mapped_column(
        String(length=FILE_NAME_MAX_LENGTH), default=""
    )
    file_name_no_ext: Mapped[str] = mapped_column(
        String(length=FILE_NAME_MAX_LENGTH), default=""
    )
    file_extension: Mapped[str] = mapped_column(
        String(length=FILE_EXTENSION_MAX_LENGTH), default=""
    )
    file_path: Mapped[str] = mapped_column(String(length=FILE_PATH_MAX_LENGTH))
    file_size_bytes: Mapped[int] = mapped_column(BigInteger(), default=0)

    summary: Mapped[str | None] = mapped_column(Text, default="")
    path_cover_s: Mapped[str | None] = mapped_column(Text, default="")
    path_cover_l: Mapped[str | None] = mapped_column(Text, default="")
    path_screenshots: Mapped[list[str] | None] = mapped_column(
        CustomJSON(), default=[]
    )

    missing_from_fs: Mapped[bool] = mapped_column(default=False, nullable=False)

    @cached_property
    def full_path(self) -> str:
        return f"{self.file_path}/{self.file_name}"

    @property
    def path_cover_small(self) -> str:
        return (
            f"{FRONTEND_RESOURCES_PATH}/{self.path_cover_s}?ts={self.updated_at}"
            if self.path_cover_s
            else ""
        )

    @property
    def path_cover_large(self) -> str:
        return (
            f"{FRONTEND_RESOURCES_PATH}/{self.path_cover_l}?ts={self.updated_at}"
            if self.path_cover_l
            else ""
        )

    @cached_property
    def merged_screenshots(self) -> list[str]:
        if self.path_screenshots:
            return [f"{FRONTEND_RESOURCES_PATH}/{s}" for s in self.path_screenshots]
        return []

    def __repr__(self) -> str:
        return f"Build: {self.name} ({self.slug}) ({self.id})"
