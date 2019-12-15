"""Interface to Java virtual machine."""

from typing import Any

import pkg_resources

_JAR_FILE = pkg_resources.resource_filename("donuts", "java/build/libs/donuts-all.jar")


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

    @property
    def java_error_class(self) -> Any:
        """Return the error class indicating exceptions in Java client code."""
        from py4j.protocol import Py4JJavaError

        return Py4JJavaError

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


jvm = Py4JBackend()
