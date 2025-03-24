"""API for accessing various OS and filesystem functions."""

import os

from click import ClickException

from .lang.base import BaseLanguageInterface
from .lang.c import CLanguageInterface
from .lang.golang import GoLanguageInterface
from .lang.java import JavaLanguageInterface
from .lang.javascript import JavaScriptLanguageInterface
from .lang.python import PythonLanguageInterface
from .lang.python3 import Python3LanguageInterface
from .lang.typescript import TypeScriptLanguageInterface

LANGUAGE_INTERFACES: dict[str, BaseLanguageInterface] = {
    "c": CLanguageInterface(),
    "golang": GoLanguageInterface(),
    "java": JavaLanguageInterface(),
    "javascript": JavaScriptLanguageInterface(),
    "typescript": TypeScriptLanguageInterface(),
    "python": PythonLanguageInterface(),
    "python3": Python3LanguageInterface(),
}


def create_project_directory(project_path: str, force: bool):
    """Creates the project directory. If it already exists, throws a `ClickException`."""
    try:
        os.makedirs(project_path, exist_ok=force)
    except FileExistsError as error:
        raise ClickException(
            f"Cannot create project with path '{project_path}' as it already exists."
        ) from error
    except OSError as error:
        print(error)
        raise ClickException(f"Invalid project path '{project_path}'") from error
    return project_path


def create_project(
    project_name: str,
    project_directory: str,
    template_data: dict[str, str],
    force: bool,
):
    """Creates the entire project. Returns the path that it was created in."""

    language_code = template_data["langSlug"]
    language_name = template_data["lang"]
    template = template_data["code"]

    project_path = os.path.join(
        os.path.expanduser(project_directory.format(language_name=language_name)),
        project_name,
    )
    create_project_directory(project_path, force)
    os.chdir(project_path)

    interface = LANGUAGE_INTERFACES.get(language_code)
    if interface is None:
        raise ClickException(f"Unsupported language {language_name}.")
    interface.create_project(template)
    return project_path
