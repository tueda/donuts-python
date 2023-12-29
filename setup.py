"""The setup script."""

from distutils.command.build import build
from typing import List, Tuple

from setuptools import Command, find_packages, setup


def readme() -> str:
    """Read the README file."""
    with open("README.rst") as f:
        return f.read()


class BuildCommand(build):
    """Command to build everything."""

    sub_commands = [("build_jar", None)] + build.sub_commands


class BuildJarCommand(Command):
    """Command to build the JAR file."""

    description = "build JAR archives"
    user_options: List[Tuple[str, str, str]] = []

    def initialize_options(self) -> None:
        """Initialize options."""
        pass

    def finalize_options(self) -> None:
        """Finalize options."""
        pass

    def run(self) -> None:
        """Run the command."""
        from build import build_jar

        if not self.dry_run:  # type: ignore[attr-defined]
            build_jar()


setup(
    name="donuts-python",
    version="0.0.3",
    description="Python binding to Donuts",
    long_description=readme(),
    author="Takahiro Ueda",
    author_email="t.ueda.od@juntendo.ac.jp",
    url="https://github.com/tueda/donuts-python",
    license="MIT",
    keywords="computer algebra, multivariate polynomial arithmetic",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    packages=find_packages(),
    package_data={"donuts": ["py.typed", "java/donuts-all.jar"]},
    python_requires=">=3.7",
    install_requires=["pyjnius"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-benchmark", "pytest-cov"],
    cmdclass={
        "build": BuildCommand,  # type: ignore[dict-item]
        "build_jar": BuildJarCommand,
    },
)
