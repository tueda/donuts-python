"""The build script."""

import os
import os.path
import subprocess


def build_jar() -> None:
    """Generate the JAR file."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    java_dir = os.path.join(root_dir, "donuts", "java")
    jar_file = os.path.join(java_dir, "build", "libs", "donuts-all.jar")

    if os.path.isfile(os.path.join(java_dir, "build.gradle")):
        # Build the fat JAR file by Gradle.
        if os.name == "posix":
            gradlew_cmd = "./gradlew"
        elif os.name == "nt":
            gradlew_cmd = "gradlew.bat"
        subprocess.run(
            [gradlew_cmd, "-Dorg.gradle.project.version=", "shadowJar"],
            cwd=java_dir,
            check=True,
        )

    if not os.path.isfile(jar_file):
        raise OSError("Failed to generate the JAR file")


if __name__ == "__main__":
    build_jar()