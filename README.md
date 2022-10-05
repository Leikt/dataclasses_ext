# dataclasses_ext

This package extend the builtin dataclasses package to add validation feature.

## Usage

Use the validator parameter of the field function to specify which function/method should be used to validate the value passed to the attribute.

```python
from dataclasses_ext import dataclass, field

def validate_email(value: str) -> str:
    if '@' not in value:
        raise ValueError(f"'{value}' is not a valid email address. It should contain a @ character.")
    return value

@dataclass
class Foo:
    email: str = field(validator=validate_email)

foo1 = Foo('valid@validemail.com') #> Works
foo2 = Foo('not_a_valid_email') #> Raise an error
```