from unittest import TestCase

from akahu.decorators import on_cooldown

import time


class TestDecorators(TestCase):
    def setUp(self):
        pass

    def test_cooldown_allows_first_call(self):
        @on_cooldown(seconds=2)
        def func():
            return None

        self.assertIsNone(func())

    def test_cooldown_raises_exception(self):
        @on_cooldown(seconds=2)
        def func():
            return None

        self.assertIsNone(func())

        with self.assertRaises(Exception):
            func()

    def test_cooldown_allows_call_after_cooldown(self):
        @on_cooldown(seconds=1)
        def func():
            return None

        self.assertIsNone(func())
        time.sleep(1.5)
        self.assertIsNone(func())

    def test_cooldown_is_stateful(self):
        @on_cooldown(seconds=10)
        def func_one():
            return None

        @on_cooldown(seconds=10)
        def func_two():
            return None

        self.assertIsNone(func_one())
        self.assertIsNone(func_two())
