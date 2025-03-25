"""Kubernetes handler."""

import json

import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from kubernetes import client, config

from ...__version__ import __version__


config.load_kube_config()


# pylint: disable=W0223
class PodsHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the Kubernetes pods."""

    @tornado.web.authenticated
    def get(self):
        """Returns the Kubernetes pods."""

        k8s_core_v1 = client.CoreV1Api()
        pods = k8s_core_v1.list_pod_for_all_namespaces(watch=False)
        result = map(lambda pod: pod.to_dict(), pods.items)
        res = json.dumps({
            "success": True,
            "message": "List of Kubernetes pods.",
            "pods": list(result),
        }, default=str)
        self.finish(res)


# pylint: disable=W0223
class ServicesHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the Kubernetes services."""

    @tornado.web.authenticated
    def get(self):
        """Returns the Kubernetes services."""

        k8s_core_v1 = client.CoreV1Api()
        services = k8s_core_v1.list_service_for_all_namespaces(watch=False)
        result = map(lambda service: service.to_dict(), services.items)
        res = json.dumps({
            "success": True,
            "message": "List of Kubernetes services.",
            "services": list(result),
        }, default=str)
        self.finish(res)
