# models/user.py

class Person:
    """Base class to demonstrate inheritance."""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Email must contain '@'.")
        self._email = value


class User(Person):
    """User inherits from Person."""

    def __init__(self, user_id, name, email):
        super().__init__(name, email)
        self.id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["email"])
