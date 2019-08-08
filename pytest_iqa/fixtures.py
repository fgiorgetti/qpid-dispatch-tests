"""PyTest fixtures."""

import pytest
import logging
from pytest_iqa.logger import get_logger
from messaging_abstract.component import *
from messaging_components.brokers import BrokerFactory
from messaging_components.clients import ClientFactory
from messaging_components.routers import RouterFactory


log = get_logger(__name__)


@pytest.fixture()
def logger():
    return log


@pytest.fixture()
def iqa(request):
    return request.config.iqa


def first_or_none(components: list):
    """
    Returns first component provided or None
    :param components:
    :return:
    """
    if components:
        return components[0]
    return None


@pytest.fixture()
def router(iqa):
    """
    Returns the first Router instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_routers())


@pytest.fixture()
def java_receiver(iqa):
    """
    Returns the first Java Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Receiver, 'java'))


@pytest.fixture()
def java_sender(iqa):
    """
    Returns the first Java Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Sender, 'java'))


@pytest.fixture()
def python_receiver(iqa):
    """
    Returns the first Python Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Receiver, 'python'))


@pytest.fixture()
def python_sender(iqa):
    """
    Returns the first Python Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Sender, 'python'))


@pytest.fixture()
def nodejs_receiver(iqa):
    """
    Returns the first NodeJS Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Receiver, 'nodejs'))


@pytest.fixture()
def nodejs_sender(iqa):
    """
    Returns the first NodeJS Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(Sender, 'nodejs'))

