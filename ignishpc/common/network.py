import socket
import subprocess


def get_hostname():
    try:
        return subprocess.check_output(['hostname', '-s']).decode("utf-8").strip()
    except subprocess.CalledProcessError as ex:
        return socket.gethostname()


def get_ip(hostname):
    return socket.gethostbyname(hostname)


def get_local_ip():
    try:
        return subprocess.check_output(['hostname', '--all-ip-addresses'], encoding='utf-8').split(" ")[0]
    except:
        return get_ip(get_hostname())

