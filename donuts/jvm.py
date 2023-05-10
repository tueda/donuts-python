"""Interface to Java virtual machine."""

import os
from typing import Any

import pkg_resources

_JAR_FILE = pkg_resources.resource_filename("donuts", "java/donuts-all.jar")

_BACKEND = os.getenv("DONUTS_PYTHON_BACKEND", "pyjnius")


class BackendMixin:
    """Backend base.

    This mix-in implements `serialize` and `deserialize` by assuming `self` has the
    following attributes:
    - `_ByteArrayOutputStream`
    - `_ObjectOutputStream`
    - `_ByteArrayInputStream`
    - `_ObjectInputStream`
    """

    def serialize(self, java_obj: Any) -> bytes:
        """Serialize the given Java object."""
        byte_stream = self._ByteArrayOutputStream()  # type: ignore[attr-defined]
        object_stream = self._ObjectOutputStream(  # type: ignore[attr-defined]
            byte_stream
        )
        object_stream.writeObject(java_obj)
        return bytes(byte_stream.toByteArray())

    def deserialize(self, data: bytes) -> Any:
        """Deserialize a Java object."""
        byte_stream = self._ByteArrayInputStream(data)  # type: ignore[attr-defined]
        object_stream = self._ObjectInputStream(  # type: ignore[attr-defined]
            byte_stream
        )
        return object_stream.readObject()


class Py4JBackend(BackendMixin):
    """JVM wrapper with py4 backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        from py4j.java_gateway import GatewayParameters, JavaGateway, launch_gateway

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

        self._ByteArrayOutputStream = self.find_class("java.io.ByteArrayOutputStream")
        self._ObjectOutputStream = self.find_class("java.io.ObjectOutputStream")
        self._ByteArrayInputStream = self.find_class("java.io.ByteArrayInputStream")
        self._ObjectInputStream = self.find_class("java.io.ObjectInputStream")

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
        return error.java_exception.getMessage()  # type: ignore[no-any-return]


class JniusBackend(BackendMixin):
    """JVM wrapper with Pyjnius backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        import jnius_config

        # Check if the jar file exists.
        with open(_JAR_FILE, "rb"):
            pass

        jnius_config.set_classpath(_JAR_FILE)

        from jnius import autoclass

        self._autoclass = autoclass

        self._java_array_new_instance = self.find_class(
            "java.lang.reflect.Array"
        ).newInstance

        self._ByteArrayOutputStream = self.find_class("java.io.ByteArrayOutputStream")
        self._ObjectOutputStream = self.find_class("java.io.ObjectOutputStream")
        self._ByteArrayInputStream = self.find_class("java.io.ByteArrayInputStream")
        self._ObjectInputStream = self.find_class(
            "com.github.tueda.donuts.python.PythonUtils"
        ).createObjectInputStream

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
        return error.innermessage  # type: ignore[no-any-return]


class JPypeBackend(BackendMixin):
    """JVM wrapper with JPype backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        import jpype

        # Check if the jar file exists.
        with open(_JAR_FILE, "rb"):
            pass

        jpype.addClassPath(_JAR_FILE)
        jpype.startJVM()

        self._JClass = jpype.JClass
        self._JArray = jpype.JArray
        self._JInt = jpype.JInt

        self._ByteArrayOutputStream = self.find_class("java.io.ByteArrayOutputStream")
        self._ObjectOutputStream = self.find_class("java.io.ObjectOutputStream")
        self._ByteArrayInputStream = self.find_class("java.io.ByteArrayInputStream")
        self._ObjectInputStream = self.find_class(
            "com.github.tueda.donuts.python.PythonUtils"
        ).createObjectInputStream

    def find_class(self, class_name: str) -> Any:
        """Return a Java class."""
        return self._JClass(class_name)

    def new_array(self, java_class: Any, size: int) -> Any:
        """Create a Java array."""
        return self._JArray(java_class)(size)

    def new_int_array(self, size: int) -> Any:
        """Create a Java int array."""
        return self._JArray(self._JInt)(size)

    @property
    def java_error_class(self) -> Any:
        """Return the error class indicating exceptions in Java client code."""
        import jpype

        return jpype.JException

    @staticmethod
    def get_error_message(error: Any) -> str:
        """Return the error message from the given exception object."""
        return str(error.getMessage())


if _BACKEND == "py4j":
    jvm = Py4JBackend()
elif _BACKEND == "pyjnius":
    jvm = JniusBackend()  # type: ignore[assignment]
elif _BACKEND == "jpype":
    jvm = JPypeBackend()  # type: ignore[assignment]
else:
    raise ValueError(f"unknown backend: DONUTS_PYTHON_BACKEND = '{_BACKEND}'")
