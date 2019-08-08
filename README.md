# qpid-dispatch-system-tests

Qpid Dispatch Router System Tests repository

## Introduction

The goal is to provide a standard mechanism for running
a test suite, for messaging applications, against multiple platforms.

Primary target is to have tests running in containers, so anyone can
write upstream tests and they can be executed in any machine that 
can spawn containers.

***Note:* This initial sample uses Ansible for deployment and some of our existing IQA classes, 
for evaluating purposes only.**

## Multiple platforms

This sample test suite uses pytest and it adds the "--platform" command line option for evaluation.

By default --platform is set to `docker`.

## Available platforms

In the same directory of your test module (files prefixed as "test_")
it is expected to have a deployment directory and within the deployment 
directory, the TestCase class (`tests/__init__.py`) will attempt to deploy/undeploy 
the related topology, on the selected platform, based on the descriptors available in it.

Looking at `tests/smoke/qpid-dispatch/one_interior_router`, for example, you will find the following
files:

```bash
tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_deploy.yaml
tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_undeploy.yaml
tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_inventory.yaml
tests/smoke/qpid-dispatch/one_interior_router/deployment/files/qdrouterd.conf
tests/smoke/qpid-dispatch/one_interior_router/test_one_interior_router.py
```

So for a platform to be considered as "available" to execute the **one_interior_router** tests,
we must have ALL files below:

```bash
deployment/<platform>_deploy.yaml
deployment/<platform>_undeploy.yaml
deployment/<platform>_inventory.yaml
```

If you choose to use, for example, "kubernetes" as the platform, then you must provide:

```bash
deployment/kubernetes_deploy.yaml
deployment/kubernetes_undeploy.yaml
deployment/kubernetes_inventory.yaml
```

If any of the files above is missing, then the related test suite will be skipped.

The benefits of this approach are:
1. We can focus primarily on `containers`, but it can be extended for other needs as well.
2. Deployment can be tested separately from code as you can simply use, in example:  
```bash
# To deploy
ansible-playbook -i tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_inventory.yaml tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_deploy.yaml

# To undeploy
ansible-playbook -i tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_inventory.yaml tests/smoke/qpid-dispatch/one_interior_router/deployment/docker_undeploy.yaml
```

## Setup and Teardown

Setup and teardown will be executed per test class.
If a given test class does not provide the deployment descriptors for
the selected platform, tests will be skipped.

An incomplete test has been added to demonstrate it: `one_edge_interior_router`.
As it does not provide any deployment descriptor, tests are skipped.

## Executing the sample suite

1. Create a virtual environment (needs python3.6+)  
`virtualenv -p python3.6 venv`
2. Install the requirements  
`pip install -r requirements.txt`
3. Running the testsuite  
```
. venv/bin/activate
pytest -s -vvv --platform docker tests/
```
