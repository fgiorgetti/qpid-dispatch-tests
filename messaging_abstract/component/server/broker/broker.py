from iqa_common.executor import Executor

from messaging_abstract.component.server.broker.address import Address
from messaging_abstract.component.server.server import Server
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node
from .queue import Queue
from typing import List
import abc
import logging


class Broker(Server, abc.ABC):
    """
    Abstract broker class
    """
    supported_protocols = []

    def __init__(self, name: str, node: Node, executor: Executor, service: Service, **kwargs):
        super(Broker, self).__init__(name, node, executor, service)

        # Log missing arguments
        required_fields = ['broker_name', 'broker_path']
        for field in required_fields:
            if field not in kwargs:
                logging.error("Missing requirement broker parameter: %s" % field)

        self.broker_name = kwargs.get('broker_name')
        self.broker_path = kwargs.get('broker_path')
        self.web_port = kwargs.get('broker_web_port', 8161)
        self.user = kwargs.get('broker_user', 'admin')
        self.password = kwargs.get('broker_password', 'admin')
        self.cluster_member = None
        self.ha_member = None

    def set_cluster_member(self, cluster_component):
        self.cluster_member = cluster_component

    def set_ha_member(self, ha_component):
        self.ha_member = ha_component

    @abc.abstractmethod
    def queues(self, refresh: bool=True) -> List[Queue]:
        """
        Must return existing queues
        :return:
        """
        pass

    @abc.abstractmethod
    def addresses(self, refresh: bool=True) -> List[Address]:
        """
        Must return existing addresses
        :return:
        """

    @abc.abstractmethod
    def create_address(self, address: Address):
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param address:
        :return:
        """
        pass

    @abc.abstractmethod
    def create_queue(self, queue: Queue, address: Address, durable: bool=True):
        """
        Creates a queue using its name and specialized type, nested to the given address.
        :param queue:
        :param address:
        :param durable:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_address(self, name: str, force: bool = False):
        """
        Deletes a given address.
        :param name:
        :param force:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a given queue.
        :param name:
        :param remove_consumers:
        :return:
        """
        pass
