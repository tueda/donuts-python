"""Developers' daily tasks."""

import os

from invoke import task


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
    from build import build_jar

    if not wheel:
        build_jar()

    if sdist:
        c.run("python setup.py sdist", pty=True)

    if wheel:
        c.run("python setup.py bdist_wheel", pty=True)
