from functools import wraps


class ValidationError(Exception):
    ...


def validatedclass(cls=None, **validators):
    """Decorate dataclasses to set validators

    from dataclass_validator import validatedclass, ValidationError
    @validatedclass(
        name=lambda self: self.value != "Bruno"
    )
    @dataclass
    class Person:
        name: str
        age: int

        def _validate_age(self, email):
            if age < 18:
                raise ValidationError("Age must be > 18")
    """

    def validate(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        errors = {}
        for field in cls.__annotations__:
            if validator := getattr(instance, f"_validate_{field}", None):
                try:
                    validator()
                except ValidationError as e:
                    errors[field] = e
            if validator := validators.get(field):
                if not validator(instance):
                    errors[field] = ValidationError(
                        f"{field} did not pass validation."
                    )
        if errors:
            raise ValidationError(errors)

        return instance

    def decorator(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            return validate(cls, *args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":
    from dataclasses import dataclass

    @validatedclass(name=lambda self: self.name != "Bruno")
    @dataclass
    class Person:
        name: str
        age: int

        def _validate_age(self):
            if self.age < 18:
                raise ValidationError("Age must be >= 18")

    p = Person(name="Bruno", age=15)

    print(p.name)
    print(p.age)
    print(p)
    print(type(p))
    print(p.__dict__)
