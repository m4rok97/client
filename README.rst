
===============
IgnisHPC Client
===============

IgnisHPC is a computing framework that operates within containers. These containers can be launched using Docker or Singularity. The IgnisHPC client serves as the user interface for interacting with the framework, streamlining all the tasks and configurations required for the containers.

The IgnisHPC client has 4 main functions:

1. **Configure Environment**: The IgnisHPC Client has four main functions, starting with environment configuration. By default, when no configuration is present, the Client prepares containers to run in the local environment using Docker or Singularity. Singularity is preferred over Docker if both are installed, as it is more secure and does not require superuser permissions for installation. The ``ignishpc config`` command allows users to define custom configurations in system mode ``-s`` and user mode. System mode enables administrators to establish a common configuration for all users, while user mode affects only the individual user. For example, system mode could configure job launches on a multi-node cluster or specify data storage locations, while users can define the default image for their job launches.

2. **Image Management**: IgnisHPC images, available for amd64, arm64, and ppc64le architectures, are stored on `Dockerhub <https://hub.docker.com/u/ignishpc>`_. These Docker-based images can be listed, deleted, pulled, and built easily using the Client. The ``ignishpc images build`` command allows users to generate their own images or combine existing ones to create a customized environment. The construction system is Docker-based, and the generated images can be used directly in Singularity or saved to disk in their native format.

3. **Start Services**: The Client defines multiple services to simplify IgnisHPC installation on an scratch cluster. These services include a resource manager (Nomad), a local image registry, and a self-discovery service (etcd). Additionally, the Submitter container can be launched as a service.

4. **Job Management**: The main function of the client is job management ``ignishpc job``. Users can run, cancel, list, or retrieve information about current jobs. Jobs can be launched using ``ignishpc job run`` or the simplified version ``ignishpc run``, utilizing the current configuration. This flexibility allows users to launch jobs with the same parameters on a personal computer or a supercomputing cluster.

For more details and usage instructions, please refer to the `full documentation <https://ignishpc.readthedocs.io>`_.

-------
Install
-------

You can install IgnisHPC Client using pip::

 $ pip install ignishpc

or::

 $ pip install git+https://github.com/ignishpc/client


External requirements
"""""""""""""""""""""
- IgnisHPC runs inside containers, so *Docker* or *Singularity* must be available.
- The command *git* is required to build IgnisHPC images from repository sources.
- Openssl is required if you want encrypt some property before running the job.
