import os
import subprocess
import io
import base64

import docker
import docker.types
import docker.errors
from spython.main import Client

from ignishpc.common import configuration


def _run(args):
    if args.cmd == "run":
        _job_run(args)
    else:
        return {
            "run": _job_run,
            "list": _list,
            "info": _info,
            "cancel": _cancel,
        }[args.action](args)


def _container_job(args, wdir, files):
    writable = configuration.get_property("ignis.container.writable")
    network = configuration.network()
    if configuration.get_property("ignis.container.provider") == "singularity":
        options = ["--cleanenv"]
        if wdir is not None:
            options.extend(["--workdir", wdir])

        if writable:
            options.append("--writable-tmpfs")

        if network != "default":
            options.extend(["--net", "--network", network])

        output = Client.execute(
            image=configuration.default_image(),
            command=["bash", "-c", "ignis-job"] + args,
            sudo=False,
            bind=files,
            stream=True,
            quiet=False,
            stream_type="both",
            options=options,
        )

        try:
            for line in output:
                print(line, end="", flush=True)
        except subprocess.CalledProcessError as ex:
            raise RuntimeError(str(ex.returncode))

    else:
        root = configuration.get_property("ignis.container.docker.root")
        other_args = {}

        if network in ("host", "bridge", "none"):
            other_args["network_mode"] = network
        elif network != "default":
            other_args["network"] = network

        if wdir is not None:
            other_args["working_dir"] = wdir

        container = None
        try:
            container = docker.from_env().containers.create(
                image=configuration.default_image(),
                command=["bash", "-c", "ignis-job"] + args,
                environment={},
                mounts=[docker.types.Mount(f, f, type="bind") for f in files],
                read_only=not writable,
                user="root" if root else "{}:{}".format(os.getuid(), os.getgid()),
                **other_args
            )
            container.start()
            output = container.logs(stdout=True, stderr=True, stream=True, follow=True)
            for line in output:
                print(line.decode("utf-8"), end="", flush=True)

        finally:
            if container is not None:
                container.remove(force=True)


def _set_property(args, arg, key):
    if getattr(args, arg) is not None:
        configuration.set_property(key, getattr(args, arg))


def _job_run(args):
    _set_property(args, "cores", "ignis.executor.cores")
    _set_property(args, "instances", "ignis.executor.instances")
    _set_property(args, "mem", "ignis.executor.memory")
    _set_property(args, "gpu", "ignis.executor.gpu")
    _set_property(args, "img", "ignis.executor.image")
    _set_property(args, "driver_cores", "ignis.driver.cores")
    _set_property(args, "driver_mem", "ignis.driver.memory")
    _set_property(args, "driver_img", "ignis.driver.image")

    for entry in args.property:
        if "=" not in entry:
            raise RuntimeError("Bad property variable")
        configuration.set_property(*entry.split("=", 1))

    buffer = io.BytesIO()
    configuration.yaml.dump(configuration.props, buffer)

    env_props = base64.b64encode(buffer.getvalue()).decode("utf-8")
    wdir = os.path.expanduser(configuration.get_property("ignis.wdir"))

    job = ["run"]
    files = [os.path.abspath(wdir)]

    if args.name is not None:
        job.append(args.name)

    for entry in args.env:
        job += ["--env", entry]

    job += ["--env", env_props]

    if args.interactive:
        job.append("--interactive")

    if args.time is not None:
        job += ["--time", args.time]

    if args.static is not None:
        job += ["--static", args.static]

    if args.scheduler_args is not None:
        job += ["--scheduler-args", args.scheduler_args]
        if args.scheduler_args != '-' and os.path.exists(args.scheduler_args):
            files.append(os.path.abspath(args.scheduler_args))

    job.append(args.command)

    _container_job(job + args.args, wdir, files)


def _list(args):
    _container_job(["list"], None, [])


def _info(args):
    _container_job(["info", args.id], None, [])


def _cancel(args):
    _container_job(["cancel", args.id], None, [])
