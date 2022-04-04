# dataclass-validator

```
pip install dataclass_validator
```

## Validation

Validates dataclasses by running methods named `_validade_<field>` or
named decorator lambda expressions.


```python
from dataclass_validator import validatedclass, ValidationError
from dataclasses import dataclass


@validatedclass(
    name=lambda self: self.name != "Bruno"
    # Lambda expression validator must return True
)
@dataclass
class Person:
    name: str
    age: int

    def _validate_age(self) -> None:
        """Method validator must raise ValidationError"""
        if self.age < 18:
            raise ValidationError("Age must be >= 18")

p = Person(name="Bruno", age=15)
```
```python
ValidationError: {'name': ValidationError('name did not pass validation.'), 'age': ValidationError('Age must be >= 18')}
```


## Computed fields

```python
from dataclass_validator import validatedclass
from dataclasses import dataclass

@computedclass(name=lambda self: self.name.upper())
@dataclass
class Person2:
    name: str
    age: int

    def _compute_age(self):
        self.age *= 2

p = Person2(name="Bruno", age=15)
assert p.name == "BRUNO"
assert p.age == 30
```
