# models/task.py

class Task:
    """Represents a task inside a project."""

    VALID_STATUSES = ("todo", "in-progress", "done")

    def __init__(self, task_id, title, project_id, status="todo", assigned_to=None):
        self.id = task_id
        self.title = title
        self.project_id = project_id
        self.status = status
        self.assigned_to = assigned_to

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Task title cannot be empty.")
        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}.")
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "status": self.status,
            "assigned_to": self.assigned_to
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["project_id"],
            data.get("status", "todo"),
            data.get("assigned_to")
        )
