import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

import pytest
from models.user import User
from models.project import Project
from models.task import Task


def test_user_creation():
    user = User(1, "Alex", "alex@example.com")
    assert user.id == 1
    assert user.name == "Alex"
    assert user.email == "alex@example.com"


def test_user_email_validation():
    with pytest.raises(ValueError):
        User(2, "Sam", "not-an-email")


def test_project_title_validation():
    with pytest.raises(ValueError):
        Project(1, "", "Desc", "2025-01-01", user_id=1)


def test_task_default_status():
    task = Task(1, "Do something", project_id=1)
    assert task.status == "todo"


def test_task_status_validation():
    with pytest.raises(ValueError):
        Task(2, "Bad status", project_id=1, status="invalid")
