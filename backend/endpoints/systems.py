from typing import Annotated

from fastapi import Body, HTTPException, Request, status
from fastapi import Path as PathVar

from decorators.auth import protected_route
from endpoints.responses.system import BuildSchema, EmulatorSchema
from handler.auth.constants import Scope
from handler.database import db_system_handler
from logger.formatter import BLUE
from logger.formatter import highlight as hl
from logger.logger import log
from utils.router import APIRouter

router = APIRouter(
    prefix="/systems",
    tags=["systems"],
)


# ── Emulators ──────────────────────────────────────────────────


@protected_route(router.get, "/emulators", [Scope.SYSTEMS_READ])
def get_emulators(request: Request) -> list[EmulatorSchema]:
    """List all emulators."""
    return [
        EmulatorSchema.model_validate(e)
        for e in db_system_handler.list_emulators()
    ]


@protected_route(
    router.get,
    "/emulators/{id}",
    [Scope.SYSTEMS_READ],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_emulator(
    request: Request,
    id: Annotated[int, PathVar(description="Emulator id.", ge=1)],
) -> EmulatorSchema:
    """Get a single emulator by ID."""
    emulator = db_system_handler.get_emulator(id)
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emulator with id {id} not found",
        )
    return EmulatorSchema.model_validate(emulator)


@protected_route(
    router.put,
    "/emulators/{id}",
    [Scope.SYSTEMS_WRITE],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def update_emulator(
    request: Request,
    id: Annotated[int, PathVar(description="Emulator id.", ge=1)],
    summary: Annotated[str | None, Body(description="Description text.")] = None,
) -> EmulatorSchema:
    """Update an emulator's metadata."""
    emulator = db_system_handler.get_emulator(id)
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emulator with id {id} not found",
        )

    data = {}
    if summary is not None:
        data["summary"] = summary

    if data:
        emulator = db_system_handler.update_emulator(id, data)

    return EmulatorSchema.model_validate(emulator)


@protected_route(
    router.delete,
    "/emulators/{id}",
    [Scope.SYSTEMS_WRITE],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def delete_emulator(
    request: Request,
    id: Annotated[int, PathVar(description="Emulator id.", ge=1)],
) -> None:
    """Delete an emulator by ID."""
    emulator = db_system_handler.get_emulator(id)
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emulator with id {id} not found",
        )

    log.info(f"Deleting emulator {hl(emulator.name, color=BLUE)} from database")
    db_system_handler.delete_emulator(id)


# ── Builds ─────────────────────────────────────────────────────


@protected_route(router.get, "/builds", [Scope.SYSTEMS_READ])
def get_builds(request: Request) -> list[BuildSchema]:
    """List all builds."""
    return [
        BuildSchema.model_validate(b) for b in db_system_handler.list_builds()
    ]


@protected_route(
    router.get,
    "/builds/{id}",
    [Scope.SYSTEMS_READ],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_build(
    request: Request,
    id: Annotated[int, PathVar(description="Build id.", ge=1)],
) -> BuildSchema:
    """Get a single build by ID."""
    build = db_system_handler.get_build(id)
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with id {id} not found",
        )
    return BuildSchema.model_validate(build)


@protected_route(
    router.put,
    "/builds/{id}",
    [Scope.SYSTEMS_WRITE],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def update_build(
    request: Request,
    id: Annotated[int, PathVar(description="Build id.", ge=1)],
    summary: Annotated[str | None, Body(description="Description text.")] = None,
) -> BuildSchema:
    """Update a build's metadata."""
    build = db_system_handler.get_build(id)
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with id {id} not found",
        )

    data = {}
    if summary is not None:
        data["summary"] = summary

    if data:
        build = db_system_handler.update_build(id, data)

    return BuildSchema.model_validate(build)


@protected_route(
    router.delete,
    "/builds/{id}",
    [Scope.SYSTEMS_WRITE],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def delete_build(
    request: Request,
    id: Annotated[int, PathVar(description="Build id.", ge=1)],
) -> None:
    """Delete a build by ID."""
    build = db_system_handler.get_build(id)
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Build with id {id} not found",
        )

    log.info(f"Deleting build {hl(build.name, color=BLUE)} from database")
    db_system_handler.delete_build(id)
