import unittest

from dataclasses_ext import dataclass, field, DuplicatedValidatorError


class TestBase(unittest.TestCase):
    def test_base(self):
        @dataclass
        class Dummy:
            some_attr: str = field(default_factory=str)

        d = Dummy(some_attr="text")
        self.assertEqual("text", d.some_attr)

    def test_validator(self):
        def validate_email(value: str) -> str:
            if "@" not in value:
                raise ValueError("An must contain '@'")
            return value

        @dataclass
        class Dummy:
            email: str = field(validator=validate_email)

        d = Dummy(email="text@text.com")
        self.assertEqual("text@text.com", d.email)

    def test_validator_exception(self):
        def validate_email(value: str) -> str:
            if "@" not in value:
                raise ValueError("An must contain '@'")
            return value

        @dataclass
        class Dummy:
            email: str = field(validator=validate_email)

        with self.assertRaises(ValueError):
            Dummy(email="not_an_email")

    def test_validator_converter(self):
        def validate_age(value: int) -> str:
            return f"{value} years old"

        @dataclass
        class Dummy:
            age_str: str = field(validator=validate_age)

        d = Dummy(12)
        self.assertEqual("12 years old", d.age_str)

    def test_duplicate_validator(self):
        def lenlongenough(x: int):
            def validator(value: list):
                if len(value) < x:
                    raise ValueError("Not long enough")

            return validator

        def lenshortenough(x: int):
            def validator(value: list):
                if len(value) > x:
                    raise ValueError("Not long enough")

            return validator

        with self.assertRaises(DuplicatedValidatorError):
            @dataclass
            class Dummy:
                v1: list = field(validator=lenshortenough(10))
                v2: list = field(validator=lenlongenough(10))

    def test_best_practice_validator(self):
        def mini(x: int):
            def mini(value: int):
                return max(x, value)

            return mini

        def maxi(x: int):
            def maxi(value: int):
                return min(value, x)

            return maxi

        @dataclass
        class Dummy:
            v1: int = field(validator=mini(12))
            v2: int = field(validator=maxi(8))

        d = Dummy(5, 52)
        self.assertEqual(12, d.v1)
        self.assertEqual(8, d.v2)
