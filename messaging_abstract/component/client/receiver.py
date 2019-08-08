"""
    # TODO jstejska: Package description
"""
from iqa_common.executor import Executor
from messaging_abstract.message import Message
from messaging_abstract.node.node import Node
from .client import Client


class Receiver(Client):
    """Abstract class of client's receivers."""

    def __init__(self, name: str, node: Node, executor: Executor, message_buffer=True, **kwargs):
        super(Receiver, self).__init__(name, node, executor, **kwargs)

        # Sender settings
        self.message_buffer = message_buffer  # type: bool
        self.messages = []  # type: list
        self.received_messages = 0  # type: int

    @property
    def last_message(self):
        """Method for pickup last received message.
        :return: Last message received or None
        :rtype: messaging_abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    def receive_messages(self, message: Message=None):
        """Method for receive message.
        :param message: Received message to be stored
        :type message: messaging_abstract.message.Message
        """
        if self.message_buffer:
            self.messages.append(message)
        else:
            self.messages = [message]

        self.received_messages += 1

    def receive(self):
        raise NotImplementedError
