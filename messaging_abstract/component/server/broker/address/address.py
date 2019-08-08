from typing import List
from messaging_abstract.component.server.broker.route import RoutingType


class Address:
    """
    Address class
    """
    def __init__(self, name: str, routing_type: RoutingType):
        self.name = name
        self.routing_type = routing_type
        self._queues: List = list()

    @property
    def queues(self) -> List:
        return self._queues
