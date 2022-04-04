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

    # for when `@validatedclass` is used
    @wraps(cls)
    def no_arguments_wrapper(*args, **kwargs):
        return validate(cls, *args, **kwargs)

    if cls:
        return no_arguments_wrapper

    # for when `@validatedclass(**options)` is used
    def decorator(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            return validate(cls, *args, **kwargs)

        return wrapper

    return decorator


def computedclass(cls=None, **computations):
    """Decorate dataclasses to set computations

    from dataclass_validator import computedclass
    @computedclass(
        name=lambda self: self.name.upper()
    )
    @dataclass
    class Person:
        name: str
        age: int

        def _compute_age(self):
            self.age * = 2
    """

    def compute(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        for field in cls.__annotations__:
            if computation := getattr(instance, f"_compute_{field}", None):
                computation()
            if computation := computations.get(field):
                setattr(instance, field, computation(instance))
        return instance

    # for when `@computedclass` is used
    @wraps(cls)
    def no_arguments_wrapper(*args, **kwargs):
        return compute(cls, *args, **kwargs)

    if cls:
        return no_arguments_wrapper

    # for when `@computedclass(**options)` is used
    def decorator(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            return compute(cls, *args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":
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

    print(p.name)
    print(p.age)
    print(p)
    print(type(p))
    print(p.__dict__)

    @validatedclass(name=lambda self: self.name != "Bruno")
    @validatedclass
    @dataclass
    class Person:
        name: str
        age: int

        def _validate_age(self):
            if self.age < 18:
                raise ValidationError("Age must be >= 18")

    q = Person(name="Bruno", age=15)

    print(q.name)
    print(q.age)
    print(q)
    print(type(q))
    print(q.__dict__)
