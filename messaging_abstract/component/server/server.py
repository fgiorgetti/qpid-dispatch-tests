from iqa_common.executor import Executor

from messaging_abstract.component.component import Component
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node


class Server(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """
    def __init__(self, name: str, node: Node, executor: Executor, service: Service):
        super(Server, self).__init__(name, node, executor)
        self.service = service
