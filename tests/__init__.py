import pytest

from iqa_common.executor import Execution
from pytest_iqa import logger
from pytest_iqa.instance import IQAInstance

log = logger.get_logger(__name__)


@pytest.mark.usefixtures('pytestconfig')
class TestCase:

    @pytest.fixture(scope="class", autouse=True)
    def deployer(self, pytestconfig):
        res: Execution = None
        d = pytestconfig.deployer

        if not d.can_deploy(self):
            pytest.skip("Missing deployment resources")
        else:
            log.debug("Deploying topology")
            res = d.deploy(self)
            log.error(res.read_stderr())
            assert res.completed_successfully()

        yield d

        if d.can_deploy(self):
            log.debug("Undeploying topology")
            res = d.undeploy(self)
            assert res.completed_successfully()

    @pytest.fixture(scope="class", autouse=True)
    def iqa(self, deployer):
        inventory_file = deployer.get_inventory(self)
        iqa = IQAInstance(inventory=inventory_file)
        yield iqa
