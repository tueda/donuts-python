"""Developers' daily tasks."""

import os
from typing import Optional

from invoke import Context, task


@task  # type: ignore[misc]
def prepare(c: Context) -> None:
    """prepare the repository for development."""
    c.run("pre-commit install", pty=True)


@task  # type: ignore[misc]
def fmt(c: Context) -> None:
    """Run formatters."""
    from build import run_gradle

    c.run("pre-commit run black --all-files", pty=True)
    c.run("pre-commit run isort --all-files", pty=True)

    run_gradle("donuts-python:spotlessApply")


@task  # type: ignore[misc]
def lint(c: Context) -> None:
    """Run linters."""
    from build import run_gradle

    c.run("pre-commit run black --all-files", pty=True)
    c.run("pre-commit run isort --all-files", pty=True)
    c.run("pre-commit run flake8 --all-files", pty=True)
    c.run("pre-commit run mypy --all-files", pty=True)

    run_gradle("donuts-python:spotlessCheck")


@task  # type: ignore[misc]
def test(c: Context, keyword: Optional[str] = None, verbose: bool = False) -> None:
    """Run tests."""
    from build import run_gradle

    args = ""
    if keyword:
        args += f" -k '{keyword}'"
    if verbose:
        args += " -vv"
    c.run("pytest --benchmark-skip --cov=donuts" + args, pty=True)

    run_gradle("donuts-python:test")


@task  # type: ignore[misc]
def bench(
    c: Context,
    save: bool = False,
    compare: Optional[str] = None,
    keyword: Optional[str] = None,
) -> None:
    """Run benchmark tests."""
    args = ""
    if save:
        args += " --benchmark-autosave"
    if compare:
        args += f" --benchmark-group-by=func --benchmark-compare={compare}"
    if keyword:
        args += f" -k '{keyword}'"
    c.run("pytest --benchmark-only" + args, pty=True)


@task  # type: ignore[misc]
def doc(c: Context) -> None:
    """Generate documents."""
    with c.cd("docs"):
        c.run("make html" if os.name != "nt" else "make.bat html", pty=True)


@task  # type: ignore[misc]
def build(c: Context, sdist: bool = False, wheel: bool = False) -> None:
    """Build the JAR file/distribution."""
    import shutil
    from pathlib import Path

    from build import build_jar

    if not wheel:
        # Ensure that the jar file is built.
        build_jar()

    if sdist:
        c.run("python setup.py sdist", pty=True)
        # Poetry 1.2.2 normalizes the sdist name.
        # https://github.com/python-poetry/poetry/issues/6915
        for f in Path("dist").glob("donuts-python-*.tar.gz"):
            src = str(f)
            dst = f.parent / f.name.replace("donuts-python-", "donuts_python-")
            shutil.move(src, dst)

    if wheel:
        c.run("python setup.py bdist_wheel", pty=True)
