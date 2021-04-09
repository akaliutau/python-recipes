#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # these  two blocks of code are needed in order to setup the correct module search paths during runtime
    # in order to avoid 'no module found' error

    # add current top-level directory
    current_dir = os.path.abspath(os.curdir)
    print(f'current directory {current_dir}')
    sys.path.append(current_dir)

    # add base directory of order microservice
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)

    print(f'system paths {sys.path}')

    # location of settings.py file
    # NOTE: FQN modules path relatively run directory must be provided
    os.environ['DJANGO_SETTINGS_MODULE'] = 'soa.microservices.order.order.settings'
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soa.microservices.order.order.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
