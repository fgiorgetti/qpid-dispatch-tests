import os
import inspect

from iqa_common.executor import Command, ExecutorLocal
from pytest_iqa import logger

log = logger.get_logger(__name__)


def pytest_addoption(parser):
    """Platform related options."""
    log.debug("pytest_addoption() called")

    group = parser.getgroup('common')
    group.addoption('--platform',
                    action='store',
                    dest='platform',
                    required=False,
                    default="docker",
                    choices=["docker", "ssh", "kubernetes"],
                    metavar='PLATFORM',
                    help='Platform to use for deployment')


def pytest_configure(config):
    config.deployer = Deployer(platform=config.getvalue('platform'))


class Deployer(object):
    def __init__(self, platform: str):
        self.platform = platform

    def can_deploy(self, obj) -> bool:
        resources = [
            self._get_deployment_playbook(obj, True),
            self._get_deployment_playbook(obj, False),
            self.get_inventory(obj)
        ]
        for res in resources:
            if not os.path.exists(res):
                log.warning("Resources unavailable to deploy topology: %s", resources)
                return False
        return True

    def _get_path(self, obj):
        path = os.path.dirname(os.path.abspath(inspect.getfile(obj.__class__)))
        return "%s/deployment" % path

    def _get_deployment_descriptor(self, obj, descriptor):
        return "%s/%s_%s.yaml" % (self._get_path(obj), self.platform, descriptor)

    def _get_deployment_playbook(self, obj, deploy: bool = True):
        return "%s" % self._get_deployment_descriptor(obj, "deploy" if deploy else "undeploy")

    def get_inventory(self, obj):
        return "%s" % self._get_deployment_descriptor(obj, "inventory")

    def deploy(self, test_obj):
        command = Command(["ansible-playbook", "-i",
                           self.get_inventory(test_obj),
                           self._get_deployment_playbook(test_obj, deploy=True)],
                          stdout=True, stderr=True)
        ex = ExecutorLocal(name="Deployer")
        deployment = ex.execute(command)
        deployment.wait()
        assert deployment.completed_successfully() or log.error(deployment.read_stdout())
        return deployment

    def undeploy(self, test_obj):
        command = Command(["ansible-playbook", "-i",
                           self.get_inventory(test_obj),
                           self._get_deployment_playbook(test_obj, deploy=False)],
                          stdout=True, stderr=True)
        ex = ExecutorLocal(name="Undeployer")
        undeployment = ex.execute(command)
        undeployment.wait()
        assert undeployment.completed_successfully() or log.error(undeployment.read_stdout())
        return undeployment
