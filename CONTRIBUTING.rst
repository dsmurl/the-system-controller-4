Contributing to The System Controller 4
=======================================

Developing
----------

Prerequisites
^^^^^^^^^^^^^

The instructions assume that you have ``docker``, ``docker-machine`` and ``docker-compose`` installed and configured properly on your machine. Please refer to the official installation guides if needed:

* Installing docker: https://docs.docker.com/installation/
* Installing docker-machine: https://docs.docker.com/machine/install-machine/
* Installing docker-compose: https://docs.docker.com/compose/install/

To verify your installation run:

.. code-block:: bash

    docker run hello-world

The result should be a message similar to this one:

.. code-block:: bash

    Hello from Docker.
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker Hub account:
    https://hub.docker.com

    For more examples and ideas, visit:
    https://docs.docker.com/userguide/

Finding information about your docker daemon
""""""""""""""""""""""""""""""""""""""""""""

Run the following command:

.. code-block:: bash

    docker-machine env  $(docker-machine ls --filter state=Running -q)

Running the application
^^^^^^^^^^^^^^^^^^^^^^^

To start the application using docker-compose:

.. code-block:: bash

    docker-compose up -d

<<<<<<< HEAD
Then launch your web browser and go to the URL that you discovered in the previous section, with the port 8080. For example on a mac, where toolbox would be installed, the URL would be http://192.168.99.100:8080.

Deploying the application
^^^^^^^^^^^^^^^^^^^^^^^^^

Deploying the application is done via Ansible. A playbook and the required roles are stored in the ``ansible`` directory at the root of the project.

This part assumes the you have Vagrant setup on your machine. Please refer to the official installation guide if needed:

* Installing Vagrant: http://docs.vagrantup.com/v2/installation/

Running ``vagrant up`` will automatically provision the virtual machine.

In case you need to update or redeploy, you can simply run the ansible playbook again.

.. code-block:: bash

    ansible-playbook --user=vagrant --connection=ssh --timeout=30 --limit='thesystemcontroller' --inventory-file=.vagrant/provisioners/ansible/inventory --sudo -v ansible/provision.yml
