"""Developers' daily tasks."""

import os

from invoke import task


@task
def prepare(c):  # type: ignore
    """prepare the repository for development."""
    c.run("pre-commit install", pty=True)


@task
def fmt(c):  # type: ignore
    """Run formatters."""
    from build import run_gradle

    c.run("pre-commit run black --all-files", pty=True)
    c.run("pre-commit run isort --all-files", pty=True)

    run_gradle("donuts-python:spotlessApply")


@task
def lint(c):  # type: ignore
    """Run linters."""
    from build import run_gradle

    c.run("pre-commit run black --all-files", pty=True)
    c.run("pre-commit run isort --all-files", pty=True)
    c.run("pre-commit run flake8 --all-files", pty=True)
    c.run("pre-commit run mypy --all-files", pty=True)

    run_gradle("donuts-python:spotlessCheck")


@task
def test(c, keyword=None, verbose=False):  # type: ignore
    """Run tests."""
    from build import run_gradle

    args = ""
    if keyword:
        args += f" -k '{keyword}'"
    if verbose:
        args += " -vv"
    c.run("pytest --benchmark-skip --cov=donuts" + args, pty=True)

    run_gradle("donuts-python:test")


@task
def bench(c, save=False, compare=None, keyword=None):  # type: ignore
    """Run benchmark tests."""
    args = ""
    if save:
        args += " --benchmark-autosave"
    if compare:
        args += f" --benchmark-group-by=func --benchmark-compare={compare}"
    if keyword:
        args += f" -k '{keyword}'"
    c.run("pytest --benchmark-only" + args, pty=True)


@task
def doc(c):  # type: ignore
    """Generate documents."""
    with c.cd("docs"):
        c.run("make html" if os.name != "nt" else "make.bat html", pty=True)


@task
def build(c, sdist=False, wheel=False):  # type: ignore
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
