aws-ctl
=======

.. image:: https://travis-ci.org/darkowlzz/aws-ctl.svg?branch=master
    :target: https://travis-ci.org/darkowlzz/aws-ctl

AWS Controller.

Develop
-------

Start development by cloning the repo and creating a new virtual env.
Running ``python setup.py develop`` would install all the dependencies and 
graylog-py in development mode. Changes to source are instantly reflected
in the installed package.

Install pre-commit git hook:

``flake8 --install-hook``

Lint
----

``python setup.py flake8``

Tests
-----

``python setup.py test``
