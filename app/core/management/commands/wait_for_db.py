"""
Django command to wait db to be available.
"""

from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db"""
    
    def handle(self, *args, **options):
        pass