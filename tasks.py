"""Developers' daily tasks."""

import os

from invoke import task


@task
def fmt(c):  # type: ignore
    """Run formatters."""
    c.run("black .", pty=True)
    c.run("seed-isort-config", pty=True)
    c.run("isort -y", pty=True)


@task
def lint(c):  # type: ignore
    """Run linters."""
    c.run("black --check --diff .", pty=True)
    c.run("isort --check-only --diff", pty=True)
    c.run("flake8", pty=True)
    c.run("mypy .", pty=True)


@task
def test(c):  # type: ignore
    """Run tests."""
    c.run("pytest --benchmark-skip --cov=donuts", pty=True)


@task
def bench(c, save=False, compare=None):  # type: ignore
    """Run benchmark tests."""
    args = ""
    if save:
        args += " --benchmark-autosave"
    if compare:
        args += f" --benchmark-group-by=func --benchmark-compare={compare}"
    c.run("pytest --benchmark-only" + args, pty=True)


@task
def doc(c):  # type: ignore
    """Generate documents."""
    with c.cd("docs"):
        c.run("make html" if os.name != "nt" else "make.bat html", pty=True)


@task
def build(c):  # type: ignore
    """Build the JAR file."""
    from build import build_jar

    build_jar()


@task
def build_sdist(c):  # type: ignore
    """Build the sdist."""
    c.run("python setup.py sdist", pty=True)
