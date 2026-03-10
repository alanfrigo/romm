from collections.abc import Sequence

from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import Session

from decorators.database import begin_session
from models.system import Build, Emulator

from .base_handler import DBBaseHandler


class DBSystemsHandler(DBBaseHandler):
    # ── Emulators ──────────────────────────────────────────────

    @begin_session
    def add_emulator(
        self,
        emulator: Emulator,
        session: Session = None,  # type: ignore
    ) -> Emulator:
        return session.merge(emulator)

    @begin_session
    def get_emulator(
        self,
        id: int,
        *,
        session: Session = None,  # type: ignore
    ) -> Emulator | None:
        return session.scalar(select(Emulator).filter_by(id=id).limit(1))

    @begin_session
    def list_emulators(
        self,
        *,
        session: Session = None,  # type: ignore
    ) -> Sequence[Emulator]:
        return session.scalars(
            select(Emulator).order_by(Emulator.name.asc())
        ).all()

    @begin_session
    def get_emulator_by_slug(
        self,
        slug: str,
        session: Session = None,  # type: ignore
    ) -> Emulator | None:
        return session.scalar(
            select(Emulator).filter_by(slug=slug).limit(1)
        )

    @begin_session
    def update_emulator(
        self,
        id: int,
        data: dict,
        session: Session = None,  # type: ignore
    ) -> Emulator:
        session.execute(
            update(Emulator)
            .where(Emulator.id == id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
        return session.query(Emulator).filter_by(id=id).one()

    @begin_session
    def delete_emulator(
        self,
        id: int,
        session: Session = None,  # type: ignore
    ) -> None:
        session.execute(
            delete(Emulator)
            .where(Emulator.id == id)
            .execution_options(synchronize_session="evaluate")
        )

    @begin_session
    def mark_missing_emulators(
        self,
        fs_slugs_to_keep: list[str],
        session: Session = None,  # type: ignore
    ) -> Sequence[Emulator]:
        missing = (
            session.scalars(
                select(Emulator)
                .where(Emulator.slug.not_in(fs_slugs_to_keep))
            )
            .unique()
            .all()
        )
        session.execute(
            update(Emulator)
            .where(Emulator.slug.not_in(fs_slugs_to_keep))
            .values(missing_from_fs=True)
            .execution_options(synchronize_session="evaluate")
        )
        return missing

    # ── Builds ─────────────────────────────────────────────────

    @begin_session
    def add_build(
        self,
        build: Build,
        session: Session = None,  # type: ignore
    ) -> Build:
        return session.merge(build)

    @begin_session
    def get_build(
        self,
        id: int,
        *,
        session: Session = None,  # type: ignore
    ) -> Build | None:
        return session.scalar(select(Build).filter_by(id=id).limit(1))

    @begin_session
    def list_builds(
        self,
        *,
        session: Session = None,  # type: ignore
    ) -> Sequence[Build]:
        return session.scalars(
            select(Build).order_by(Build.name.asc())
        ).all()

    @begin_session
    def get_build_by_slug(
        self,
        slug: str,
        session: Session = None,  # type: ignore
    ) -> Build | None:
        return session.scalar(
            select(Build).filter_by(slug=slug).limit(1)
        )

    @begin_session
    def update_build(
        self,
        id: int,
        data: dict,
        session: Session = None,  # type: ignore
    ) -> Build:
        session.execute(
            update(Build)
            .where(Build.id == id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
        return session.query(Build).filter_by(id=id).one()

    @begin_session
    def delete_build(
        self,
        id: int,
        session: Session = None,  # type: ignore
    ) -> None:
        session.execute(
            delete(Build)
            .where(Build.id == id)
            .execution_options(synchronize_session="evaluate")
        )

    @begin_session
    def mark_missing_builds(
        self,
        fs_slugs_to_keep: list[str],
        session: Session = None,  # type: ignore
    ) -> Sequence[Build]:
        missing = (
            session.scalars(
                select(Build)
                .where(Build.slug.not_in(fs_slugs_to_keep))
            )
            .unique()
            .all()
        )
        session.execute(
            update(Build)
            .where(Build.slug.not_in(fs_slugs_to_keep))
            .values(missing_from_fs=True)
            .execution_options(synchronize_session="evaluate")
        )
        return missing
