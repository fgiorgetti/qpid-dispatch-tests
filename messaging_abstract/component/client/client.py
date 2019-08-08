"""
    # TODO jstejska: Package description
"""
from iqa_common.executor import Executor, Execution

from messaging_abstract.component.component import Component
from messaging_abstract.node.node import Node


class Client(Component):
    """
    Abstract class for every messaging client
    """

    # Required variables
    supported_protocols = []
    version = ''

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(Client, self).__init__(name, node, executor)
        self.logs = None  # @TODO

    @property
    def get_supported_protocols(self):
        return self.supported_protocols

    @property
    def get_name(self):
        return self.name

    @property
    def get_version(self):
        return self.version
