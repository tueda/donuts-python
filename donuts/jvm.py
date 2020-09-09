"""Interface to Java virtual machine."""

import os
from typing import Any

import pkg_resources

_JAR_FILE = pkg_resources.resource_filename("donuts", "java/donuts-all.jar")

_BACKEND = os.getenv("DONUTS_PYTHON_BACKEND", "pyjnius")


class Py4JBackend:
    """JVM with py4 backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        from py4j.java_gateway import (
            GatewayParameters,
            JavaGateway,
            launch_gateway,
        )

        # Check if the jar file exists.
        with open(_JAR_FILE, "rb"):
            pass

        (port, token) = launch_gateway(
            classpath=_JAR_FILE, enable_auth=True, die_on_exit=True
        )

        gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=port, auth_token=token),
        )

        self._gateway = gateway
        self._jvm = gateway.jvm

    def find_class(self, class_name: str) -> Any:
        """Return a Java class."""
        return self._jvm.__getattr__(class_name)

    def new_array(self, java_class: Any, size: int) -> Any:
        """Create a Java array."""
        return self._gateway.new_array(java_class, size)

    def new_int_array(self, size: int) -> Any:
        """Create a Java int array."""
        return self._gateway.new_array(self._gateway.jvm.int, size)

    @property
    def java_error_class(self) -> Any:
        """Return the error class indicating exceptions in Java client code."""
        from py4j.protocol import Py4JJavaError

        return Py4JJavaError

    @staticmethod
    def get_error_message(error: Any) -> str:
        """Return the error message from the given exception object."""
        return error.java_exception.getMessage()  # type: ignore

    def serialize(self, java_obj: Any) -> bytes:
        """Serialize the given Java object."""
        byte_stream = self._jvm.java.io.ByteArrayOutputStream()
        object_stream = self._jvm.java.io.ObjectOutputStream(byte_stream)
        object_stream.writeObject(java_obj)
        return byte_stream.toByteArray()  # type: ignore

    def deserialize(self, data: bytes) -> Any:
        """Deserialize a Java object."""
        byte_stream = self._jvm.java.io.ByteArrayInputStream(data)
        object_stream = self._jvm.java.io.ObjectInputStream(byte_stream)
        return object_stream.readObject()


class JniusBackend:
    """JVM with Pyjnius backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        import jnius_config

        # Check if the jar file exists.
        with open(_JAR_FILE, "rb"):
            pass

        jnius_config.set_classpath(_JAR_FILE)

        from jnius import autoclass

        self._autoclass = autoclass
        self._java_array_new_instance = autoclass("java.lang.reflect.Array").newInstance

    def find_class(self, class_name: str) -> Any:
        """Return a Java class."""
        return self._autoclass(class_name)

    def new_array(self, java_class: Any, size: int) -> Any:
        """Create a Java array."""
        return self._java_array_new_instance(java_class, size)

    def new_int_array(self, size: int) -> Any:
        """Create a Java int array."""
        return [0] * size

    @property
    def java_error_class(self) -> Any:
        """Return the error class indicating exceptions in Java client code."""
        from jnius import JavaException

        return JavaException

    @staticmethod
    def get_error_message(error: Any) -> str:
        """Return the error message from the given exception object."""
        return error.innermessage  # type: ignore

    def serialize(self, java_obj: Any) -> bytes:
        """Serialize the given Java object."""
        byte_stream = self._autoclass("java.io.ByteArrayOutputStream")()
        object_stream = self._autoclass("java.io.ObjectOutputStream")(byte_stream)
        object_stream.writeObject(java_obj)
        return byte_stream.toByteArray().tostring()  # type: ignore

    def deserialize(self, data: bytes) -> Any:
        """Deserialize a Java object."""
        byte_stream = self._autoclass("java.io.ByteArrayInputStream")(data)
        object_stream = self._autoclass(
            "com.github.tueda.donuts.python.PythonUtils"
        ).createObjectInputStream(byte_stream)
        return object_stream.readObject()


if _BACKEND == "py4j":
    jvm = Py4JBackend()
elif _BACKEND == "pyjnius":
    jvm = JniusBackend()  # type: ignore
