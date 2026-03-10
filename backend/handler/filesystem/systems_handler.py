import os

from config import LIBRARY_BASE_PATH
from config.config_manager import config_manager as cm

from .base_handler import FSHandler


class FSSystemsHandler(FSHandler):
    def __init__(self) -> None:
        super().__init__(base_path=LIBRARY_BASE_PATH)

    def _get_systems_base_path(self) -> str:
        cnfg = cm.get_config()
        return cnfg.SYSTEMS_FOLDER_NAME

    def get_emulators_path(self) -> str:
        return f"{self._get_systems_base_path()}/emulators"

    def get_builds_path(self) -> str:
        return f"{self._get_systems_base_path()}/builds"

    async def get_emulator_slugs(self) -> list[str]:
        """List all emulator directories (each folder = one emulator)."""
        try:
            return await self.list_directories(path=self.get_emulators_path())
        except (FileNotFoundError, ValueError):
            return []

    async def get_build_slugs(self) -> list[str]:
        """List all build directories (each folder = one build)."""
        try:
            return await self.list_directories(path=self.get_builds_path())
        except (FileNotFoundError, ValueError):
            return []

    async def get_entry_files(self, category: str, slug: str) -> list[str]:
        """Get all files inside a specific emulator or build folder.

        Args:
            category: 'emulators' or 'builds'
            slug: folder name of the entry
        Returns:
            List of filenames
        """
        entry_path = f"{self._get_systems_base_path()}/{category}/{slug}"
        try:
            return await self.list_files(path=entry_path)
        except (FileNotFoundError, ValueError):
            return []

    async def get_entry_size(self, category: str, slug: str) -> int:
        """Calculate total size of all files in an entry folder."""
        files = await self.get_entry_files(category, slug)
        total = 0
        base = f"{self._get_systems_base_path()}/{category}/{slug}"
        for f in files:
            try:
                total += await self.get_file_size(f"{base}/{f}")
            except (FileNotFoundError, ValueError):
                pass
        return total

    async def create_systems_structure(self) -> None:
        """Create the systems/emulators and systems/builds directories."""
        await self.make_directory(self.get_emulators_path())
        await self.make_directory(self.get_builds_path())
