import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    try:
        return asyncio.get_event_loop().run_until_complete(
            install_requirements()
        )
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(install_requirements())


def git():
    """
    SAFE git handler:
    - VPS/local: git repo ho to fetch/pull karega
    - Docker/Heroku: git repo na ho to silently skip karega
    - Kabhi bhi bot crash nahi karega
    """

    # agar upstream hi nahi diya to skip
    if not config.UPSTREAM_REPO:
        LOGGER(__name__).info("UPSTREAM_REPO not set, skipping git.")
        return

    try:
        # git repo detect karo
        repo = Repo(search_parent_directories=True)
        LOGGER(__name__).info("Git repository detected.")

        # origin remote check
        if "origin" not in repo.remotes:
            LOGGER(__name__).warning("No origin remote found, skipping git update.")
            return

        origin = repo.remotes.origin

        try:
            origin.fetch()
            origin.pull()
            LOGGER(__name__).info("Git updates fetched successfully.")
        except GitCommandError as e:
            LOGGER(__name__).warning(f"Git pull failed, skipping update: {e}")

    except InvalidGitRepositoryError:
        # Docker / Heroku case
        LOGGER(__name__).warning("Not a git repository. Git update skipped.")
    except Exception as e:
        LOGGER(__name__).warning(f"Git skipped due to unexpected error: {e}")
