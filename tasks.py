"""Tasks for Pipenv."""

from invoke import task


@task
def fmt(c):  # type: ignore
    """Run formatters."""
    c.run("black .", pty=True)
    c.run("isort -y", pty=True)


@task
def lint(c):  # type: ignore
    """Run linters."""
    c.run("black --check --diff .", pty=True)
    c.run("isort --check-only --diff", pty=True)
    c.run("flake8 donuts setup.py tasks.py", pty=True)
    c.run("mypy donuts setup.py tasks.py", pty=True)


@task
def test(c):  # type: ignore
    """Run tests."""
    c.run("pytest --cov=donuts", pty=True)


@task
def output_dev_only_requirements(c):  # type: ignore
    """Write dev-only-requirements.txt."""
    with open("dev-only-requirements.txt", "w") as f:
        c.run("pipenv lock -r -d", out_stream=f)