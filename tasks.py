"""Tasks for Pipenv."""

from invoke import task


@task
def fmt(c):  # type: ignore
    """Run formatters."""
    c.run("black .")
    c.run("isort -y")


@task
def lint(c):  # type: ignore
    """Run linters."""
    c.run("black --check --diff .")
    c.run("isort --check-only --diff")
    c.run("flake8 donuts setup.py tasks.py")
    c.run("mypy donuts setup.py tasks.py")


@task
def test(c):  # type: ignore
    """Run tests."""
    c.run("pytest --cov=donuts")


@task
def output_dev_only_requirements(c):  # type: ignore
    """Write dev-only-requirements.txt."""
    with open("dev-only-requirements.txt", "w") as f:
        c.run("pipenv lock -r -d", out_stream=f)
