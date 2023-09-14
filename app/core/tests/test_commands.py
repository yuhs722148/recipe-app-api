"""
Test custom django management commands.
"""
# To mock the database behavior
from unittest.mock import patch
# The error we might get when try to connect to db before db is ready
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mocking the 'check' method to simulate the response
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""
    # Because we add @patch,
    # we have to add a new argument to catch the return value
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if databse ready."""
        patched_check.return_value = True
        # Call 'wait_for_db' command, execute the code inside wait_for_db.py
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # 因為PostgreSQL在初始化階段還不能接受連線，所以會先出現psycopg2錯誤
        # 再來因為沒有資料故產生OperationalError，第6次會回傳正常，這裡的次數可以任意修改模擬情況
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
