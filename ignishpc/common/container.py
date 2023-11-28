import docker
import os
from spython.main import Client
from ignishpc.common import configuration


def _get_provider():
    try:
        return configuration.props["ignis"]["container"]["provider"]
    except:
        pass

    try:
        test_singularity()
        return "singularity"
    except:
        pass

    try:
        test_docker()
        return "docker"
    except:
        pass
    return "none"


def test_docker():
    docker.from_env().ping()


def test_singularity():
    Client.version()


provider = _get_provider()


def default_container():
    try:
        return configuration.props["ignis"]["container"]["image"]
    except:
        if provider == "singularity":
            path = "~/.ignis/ignis.sif"
            if os.path.exists(path):
                return path
            else:
                return "docker://ignishpc/ignishpc"
        elif provider == "docker":
            return "ignishpc/ignishpc"
        else:
            return "none"
