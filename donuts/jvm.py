"""Interface to Java virtual machine."""

from typing import Any

import pkg_resources

_JAR_FILE = pkg_resources.resource_filename("donuts", "java/build/libs/donuts-all.jar")


class Py4JBackend:
    """JVM with py4 backend."""

    def __init__(self) -> None:
        """Create a JVM."""
        from py4j.java_gateway import (
            CallbackServerParameters,
            GatewayParameters,
            is_instance_of,
            JavaGateway,
            launch_gateway,
        )

        # Check if the jar file exists.
        with open(_JAR_FILE, "rb"):
            pass

        (port, token) = launch_gateway(classpath=_JAR_FILE, enable_auth=True)

        gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=port, auth_token=token),
            callback_server_parameters=CallbackServerParameters(port=0),
        )

        python_port = gateway.get_callback_server().get_listening_port()

        gateway.java_gateway_server.resetCallbackClient(
            gateway.java_gateway_server.getCallbackClient().getAddress(), python_port
        )

        gateway.close()

        self._gateway = gateway
        self._is_instance_of = is_instance_of

    def find_class(self, class_name: str) -> Any:
        """Return a Java class."""
        return self._gateway.jvm.__getattr__(class_name)


jvm = Py4JBackend()
