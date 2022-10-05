# dataclasses_ext

This package extend the builtin dataclasses package to add validation feature.

## Usage

Use the validator parameter of the field function to specify which function/method should be used to validate the value passed to the attribute.


(disclaimer: these are not real life examples)
```python
from dataclasses_ext import dataclass, field

def validate_email(value: str) -> str:
    if '@' not in value:
        raise ValueError(f"'{value}' is not a valid email address. It should contain a @ character.")
    return value

def validate_list_is_not_empty(value: list) -> list:
    if len(value) == 0:
        raise ValueError("List cannot be empty.")
    return value

@dataclass
class Foo:
    email: str = field(validator=validate_email)
    addresses: list = field(validator=validate_list_is_not_empty, default_factory=list)

foo1 = Foo('valid@validemail.com', ['some_address']) #> Works
foo2 = Foo('not_a_valid_email', ['some_address']) #> Raise a ValueError "'not_a_valid_email' is not a valid email address. It should contain a @ character."
foo3 = Foo('valid@validemail.com') #> Raise a ValueError "List cannot be empty"
```

## When no init

Since the validation is only applied on the object creation through the __init__ method, you cannot use validation when init is disable:

```python
from dataclasses_ext import dataclass, field

@dataclass(init=False)
class Foo:
    value: str = field(validator=str)

Foo("test") #> Will raise a ValueError because validator are not allowed when the init is disabled

@dataclass
class Goo:
    value: str = field(validator=str, init=False)

Goo("Test") #> Will raise the same error for the same reason.

@dataclass
class Hoo:
    value1: str = field(validator=str)
    value2: str = field(init=False)

Hoo("Test") #> This work because the init is only disable for the field value2
```