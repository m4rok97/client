import os
import string
import random
import subprocess

from ruamel.yaml import YAML, CommentedMap
from ruamel.yaml.parser import MarkedYAMLError
from ruamel.yaml.comments import CommentedBase

USER_CONFIG = os.getenv("IGNIS_USER_CONFIG", default=os.path.expanduser("~/.ignis/etc/ignis.yaml"))
SYSTEM_CONFIG = os.getenv("IGNIS_SYSTEM_CONFIG", default="/etc/ignis/ignis.yaml")
yaml = YAML()
props = yaml.load("""
ignis:
  container:
    docker:
      registry: ""
      namespace: "ignishpc"
      default: "ignishpc"
      tag: "latest"
      root: false
      network: "default"
    singularity:
      source: "~/.ignis/images"
      default: "ignishpc.sif"
      network: "default"
    writable: false
    #provider: ""
""")


def get_property(key, default=None):
    names = key.split(".")
    entry = props
    for name in names:
        if name not in entry:
            return default
        entry = entry[name]
    return entry


def has_property(key):
    names = key.split(".")
    entry = props
    for name in names:
        if name not in entry:
            return False
        entry = entry[name]
    return True


def set_property(key, value):
    names = key.split(".")
    entry = props
    for name in names[:-1]:
        if name not in entry:
            entry[name] = CommentedMap()
        entry = entry[name]
    entry[names[-1]] = value


def format_image(name):
    if "/" not in name:
        namespace = get_property("ignis.container.docker.namespace", default="ignishpc")
        if len(namespace) > 0 and namespace[-1] != "/":
            namespace += "/"
        name = namespace + name

    if name.count("/") == 1:
        registry = get_property("ignis.container.docker.registry", default="")
        if len(registry) > 0 and registry[-1] != "/":
            registry += "/"
        name = registry + name

    if ":" not in name or name.rindex(":") > name.rindex("/"):
        tag = get_property("ignis.container.docker.tag", default="")
        if len(tag) > 0 and tag[0] != ':':
            tag = ":" + tag
        name = name + tag

    return name


def default_image():
    prefix = ""
    if get_property("ignis.container.provider") == "singularity":
        source = os.path.expanduser(get_property("ignis.container.singularity.source"))
        image = source + ("" if source.endswith("/") else "/") + get_property("ignis.container.singularity.default")
        if os.path.exists(image) or ":" in image:
            return image
        prefix = "docker://"

    return prefix + format_image(get_property("ignis.container.docker.default"))


def network():
    if get_property("ignis.container.provider") == "singularity":
        return get_property("ignis.container.singularity.network")
    else:
        return get_property("ignis.container.docker.network")


def yaml_merge(target, source):
    target.ca.items.update(source.ca.items)
    target.ca.comment = source.ca.comment or target.ca.comment
    target.ca.pre = source.ca.pre or target.ca.pre
    target.ca.end = source.ca.end or target.ca.end
    for key, value in source.items():
        if key in target and isinstance(value, CommentedMap) and isinstance(target[key], CommentedMap):
            yaml_merge(target[key], value)
        else:
            target[key] = value


def read_file_config(path):
    with open(path) as file:
        data = file.read()
        data = os.path.expandvars(data)
        return yaml.load(data)


def _check_singularity():
    try:
        return subprocess.run(["singularity", "version"], capture_output=True).returncode == 0
    except:
        return False


def load_config(path):
    ok = True
    for file in [SYSTEM_CONFIG, USER_CONFIG, path]:
        if file is not None and os.path.exists(file):
            try:
                yaml_merge(props, read_file_config(file))
            except:
                ok = False

    if not has_property("ignis.container.provider"):
        set_property("ignis.container.provider", "singularity" if _check_singularity() else "docker")

    if not has_property("ignis.wdir"):
        set_property("ignis.wdir", os.getcwd())

    return ok or (path is not None and os.path.exists(path))


def random_password(k=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
