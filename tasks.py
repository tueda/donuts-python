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
def test(c, keyword=None, verbose=False):  # type: ignore
    """Run tests."""
    args = ""
    if keyword:
        args += f" -k '{keyword}'"
    if verbose:
        args += " -vv"
    c.run("pytest --benchmark-skip --cov=donuts" + args, pty=True)


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
