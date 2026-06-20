#!/usr/bin/env python
"""Точка входа, через которую я дергаю django-команды."""

import os
import sys


def main():
    """Запускаем нужную manage.py-команду без лишней магии."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
