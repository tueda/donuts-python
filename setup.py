"""The setup script."""

import os
import os.path
import shutil
import subprocess
from distutils.command.build import build as build_  # type: ignore
from typing import List, Tuple

from setuptools import Command, find_packages, setup

VERSION = "0.0.1"
JAR_VERSION = "0.0.1-SNAPSHOT"


def readme() -> str:
    """Read the README file."""
    with open("README.rst") as f:
        return f.read()


class build(build_):  # type: ignore # noqa: N801
    """Command to build everything."""

    sub_commands = [("build_jar", None)] + build_.sub_commands


class build_jar(Command):  # type: ignore # noqa: N801
    """Command to build JAR files."""

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
        if not self.dry_run:
            setup_dir = os.path.dirname(os.path.abspath(__file__))
            java_dir = os.path.join(setup_dir, "donuts", "java")
            lib_dir = os.path.join(java_dir, "build", "libs")
            src_jar_file = os.path.join(
                lib_dir, "donuts-{}-all.jar".format(JAR_VERSION)
            )
            dest_jar_file = os.path.join(lib_dir, "donuts-all.jar")

            if os.path.isfile(os.path.join(java_dir, "build.gradle")):
                # Build the fat jar.
                if os.name == "posix":
                    gradlew_cmd = "./gradlew"
                elif os.name == "nt":
                    gradlew_cmd = "gradlew.bat"
                subprocess.run([gradlew_cmd, "shadowJar"], cwd=java_dir, check=True)
                # And then copy it.
                shutil.copyfile(src_jar_file, dest_jar_file)

            if not os.path.isfile(dest_jar_file):
                raise OSError("Failed to generate JAR files")


setup(
    name="donuts-python",
    version=VERSION,
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
    tests_require=["pytest", "pytest-benchmark", "pytest-cov", "pytest-xdist"],
    cmdclass={"build": build, "build_jar": build_jar},
)
