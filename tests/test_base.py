import unittest

from dataclasses_ext import dataclass, field


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

    def test_best_practice_validator(self):
        def mini(x: int):
            def _mini(value: int):
                return max(x, value)

            return _mini

        def maxi(x: int):
            def _maxi(value: int):
                return min(value, x)

            return _maxi

        @dataclass
        class Dummy:
            v1: int = field(validator=mini(12))
            v2: int = field(validator=maxi(8))

        d = Dummy(5, 52)
        self.assertEqual(12, d.v1)
        self.assertEqual(8, d.v2)

    def test_same_validator(self):
        @dataclass
        class Dummy:
            v1: int = field(validator=str)
            v2: int = field(validator=str)
        # Should not raise any error

    def test_same_validator_with_parameters(self):
        def validate_mini(x: int):
            def _validate_mini(value: int) -> int:
                return max(x, value)

            return _validate_mini

        @dataclass
        class Dummy:
            v1: int = field(validator=validate_mini(10))
            v2: int = field(validator=validate_mini(100))

        # Should not raise any exception

        d = Dummy(0, 0)
        self.assertEqual(10, d.v1)
        self.assertEqual(100, d.v2)

    def test_object_method_validator(self):
        class Validator:
            def string_is_five_long(self, value: str) -> str:
                if len(value) != 5:
                    raise ValueError(f"String '{value}' is not 10 characters long.")
                return value

        @dataclass
        class Dummy:
            string: str = field(validator=Validator().string_is_five_long)

        with self.assertRaises(ValueError):
            Dummy("too long string")

        Dummy("12345")  # > Should be okay

    def test_classmethod_validator(self):
        class Validators:
            @classmethod
            def string_is_five_long(cls, value: str) -> str:
                if len(value) != 5:
                    raise ValueError(f"String '{value}' is not 10 characters long.")
                return value

        @dataclass
        class Dummy:
            string: str = field(validator=Validators.string_is_five_long)

        with self.assertRaises(ValueError):
            Dummy("too long string")

        Dummy("12345")  # > Should be okay

    def test_no_field_init(self):
        with self.assertRaises(ValueError):
            @dataclass
            class Dummy:
                a1: str
                a2: str = field(init=False, validator=str)

    def test_no_class_init(self):
        with self.assertRaises(ValueError):
            @dataclass(init=False)
            class Dummy:
                a1: str = field(validator=str)

    def test_partial_init(self):
        @dataclass
        class Dummy:
            v1: int = field(validator=int)
            v2: int = field(init=False)

    def test_default_value(self):
        @dataclass
        class Dummy:
            v: int = field(default=10, validator=int)

        d = Dummy()
        self.assertEqual(10, d.v)

    def test_default_factory(self):
        def validate_list(value: list) -> list:
            if len(value) == 0:
                raise ValueError("List cannot be empty.")
            return value

        @dataclass
        class Dummy:
            v: int = field(default_factory=list, validator=validate_list)

        with self.assertRaises(ValueError):
            Dummy()