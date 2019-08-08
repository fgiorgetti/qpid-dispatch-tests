import time

from proton import ConnectionException

from messaging_abstract.component import ServiceStatus, Sender, Receiver
from messaging_abstract.message import Message
from messaging_components.clients import SenderJava, ReceiverJava, JavaReceiverClientCommand
from messaging_components.routers import Dispatch
from messaging_components.routers.dispatch.management import RouterQuery
from pytest_iqa.instance import IQAInstance
from tests import TestCase

TIMEOUT_SECS = 30
DELAY_SECS = 5
MAX_ATTEMPTS = 3

SAMPLE_MESSAGE_BODY = "sample message body"
MESSAGE_COUNT = 100


class TestOneInteriorRouter(TestCase):
    def test_network(self, iqa: IQAInstance):
        assert iqa

        # Expected router from inventory is available
        router_i1: Dispatch = iqa.get_routers("one_interior_router.Router.I1")[0]
        assert router_i1

        # Querying router network
        query = RouterQuery(router_i1.node.get_ip(), router_i1.port)
        nodes = []
        for attempt in range(MAX_ATTEMPTS):
            try:
                nodes = query.node()
                break
            except ConnectionException:
                time.sleep(DELAY_SECS)
                pass

        # Assert only one node in the network (from $management)
        assert len(nodes) == 1

    def test_router_status(self, iqa):
        router_i1: Dispatch = iqa.get_routers("one_interior_router.Router.I1")[0]
        assert router_i1.service.status() == ServiceStatus.RUNNING

    def test_stop_router(self, iqa):
        router_i1: Dispatch = iqa.get_routers("one_interior_router.Router.I1")[0]
        router_i1.service.stop()
        assert router_i1.service.status() == ServiceStatus.STOPPED

    def test_start_router(self, iqa):
        router_i1: Dispatch = iqa.get_routers("one_interior_router.Router.I1")[0]
        router_i1.service.start()
        assert router_i1.service.status() == ServiceStatus.RUNNING

    def test_anycast_messages(self, iqa: IQAInstance):
        router_i1: Dispatch = iqa.get_routers("one_interior_router.Router.I1")[0]
        sender_java: SenderJava = iqa.get_clients(Sender, 'java')[0]
        receiver_java: ReceiverJava = iqa.get_clients(Receiver, 'java')[0]
        assert sender_java
        assert receiver_java

        # URL to communicate
        url = "amqp://%s:%s/anycast/address" % (router_i1.node.get_ip(), router_i1.port)

        # Receiver
        receiver_java.set_url(url)
        receiver_java.command.stdout = True
        receiver_java.command.logging.log_msgs = 'dict'
        receiver_java.command.control.count = MESSAGE_COUNT
        receiver_java.command.control.timeout = TIMEOUT_SECS

        # Sender
        msg = Message(body=SAMPLE_MESSAGE_BODY)
        sender_java.set_url(url)
        sender_java.command.control.count = MESSAGE_COUNT
        sender_java.command.control.timeout = TIMEOUT_SECS

        # Starting
        receiver_java.receive()
        sender_java.send(msg)

        # Wait for clients
        sender_java.execution.wait()
        receiver_java.execution.wait()

        # Assert messages have been exchanged
        assert sender_java.execution.completed_successfully()
        assert receiver_java.execution.completed_successfully()

        # Assert all messages received
        assert len(receiver_java.execution.read_stdout(lines=True)) == MESSAGE_COUNT
