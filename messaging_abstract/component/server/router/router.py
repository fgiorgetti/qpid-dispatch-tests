from iqa_common.executor import Executor

from messaging_abstract.component.server.server import Server
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

import abc


class Router(Server, abc.ABC):
    """
    Abstract messaging Router
    """

    def __init__(self, name: str, node: Node, executor: Executor, service: Service,
                 port=5672, config=None, **kwargs):
        super(Router, self).__init__(name, node, executor, service)
        self.port = kwargs.get('router_port', port)
        self.config = kwargs.get('router_config', config)
        self.user = None
        self.password = None
        self.pem_file = None
        self.key_file = None
        self.key_password = None

        # initializing client from kwargs
        for func in [self.set_credentials, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    def set_credentials(self, user: str=None, password: str=None):
        """
        Stores user and password that must be used to communicate with the router instance
        through the main port defined in constructor method.
        :param user:
        :param password:
        :return:
        """
        self.user = user
        self.password = password

    def set_ssl_auth(self, pem_file: str=None, key_file: str=None, key_password: str=None):
        """
        Defines SSL credentials that must be used to communicate with this router instance
        through its main port.
        :param pem_file:
        :param key_file:
        :param key_password:
        :return:
        """
        self.pem_file = pem_file
        self.key_file = key_file
        # Set to None when empty as well
        self.key_password = None if not key_password else key_password

    def has_credentials(self) -> bool:
        return self.user and self.password

    def has_ssl_keys(self):
        return self.pem_file and self.key_file
