#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from core.settings import HOSTNAME,PORT


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    os.system(f'python manage.py runserver {HOSTNAME}:{PORT} --noreload')


if __name__ == '__main__':
    main()
