class Project:

    def __init__(self, project_id, title, description, due_date, user_id):
        self.id = project_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Project title must be a non-empty string.")
        self._title = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data.get("description", ""),
            data.get("due_date", ""),
            data["user_id"],
        )
