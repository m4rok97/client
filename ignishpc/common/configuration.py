import os
from ruamel.yaml import YAML, CommentedMap
from ruamel.yaml.parser import MarkedYAMLError
from ruamel.yaml.comments import CommentedBase

USER_CONFIG = os.path.expanduser("~/.ignis/ignis.yaml")
SYSTEM_CONFIG = "/etc/ignis/ignis.yaml"
yaml = YAML()
props = CommentedMap()


def get_property(key):
    names = key.split(".")
    entry = props
    for name in names:
        if name not in entry:
            return None
        entry = entry[name]
    return entry


def format_image(name):
    if "/" not in name:
        namespace = get_property("ignis.container.namespace") or "ignishpc"
        if len(namespace) > 0 and namespace[-1] != "/":
            namespace += "/"
        name = namespace + name

    if name.count("/") == 1:
        registry = get_property("ignis.container.registry") or ""
        if len(registry) > 0 and registry[-1] != "/":
            registry += "/"
        name = registry + name

    if ":" not in name or name.rindex(":") > name.rindex("/"):
        tag = get_property("ignis.container.tag") or ""
        if len(tag) > 0 and tag[0] != ':':
            tag = ":" + tag
        name = name + tag

    return name


def working_directory():
    try:
        return os.path.expanduser(yaml["ignis"]["wdir"])
    except:
        return os.getcwd()


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
        return yaml.load(file)


def read_sys_config():
    return read_file_config(SYSTEM_CONFIG)


def read_user_config():
    return read_file_config(USER_CONFIG)


def read_cli_config(path):
    return read_file_config(path)


def load_config(path):
    ok = True
    try:
        yaml_merge(props, read_sys_config())
    except FileNotFoundError:
        pass
    except:
        ok = False
    try:
        yaml_merge(props, read_user_config())
    except FileNotFoundError:
        pass
    except:
        ok = False
    if path is not None:
        try:
            yaml_merge(props, read_cli_config(path))
        except:
            ok = False
    return ok
