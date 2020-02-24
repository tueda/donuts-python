"""The setup script."""

from distutils.command.build import build  # type: ignore
from typing import List, Tuple

from setuptools import Command, find_packages, setup


def readme() -> str:
    """Read the README file."""
    with open("README.rst") as f:
        return f.read()


class BuildCommand(build):  # type: ignore
    """Command to build everything."""

    sub_commands = [("build_jar", None)] + build.sub_commands


class BuildJarCommand(Command):  # type: ignore
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

        if not self.dry_run:
            build_jar()


setup(
    name="donuts-python",
    version="0.0.1",
    description="Python binding to Donuts",
    long_description=readme(),
    author="Takahiro Ueda",
    author_email="tueda@st.seikei.ac.jp",
    url="https://github.com/tueda/donuts-python",
    license="MIT",
    keywords="computer algebra, multivariate polynomial arithmetic",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    packages=find_packages(),
    package_data={"donuts": ["py.typed", "java/build/libs/donuts-all.jar"]},
    python_requires=">=3.7",
    install_requires=["py4j"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-benchmark", "pytest-cov"],
    cmdclass={"build": BuildCommand, "build_jar": BuildJarCommand},
)
