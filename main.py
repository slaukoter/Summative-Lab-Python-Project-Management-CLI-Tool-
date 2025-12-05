import argparse
from typing import Optional, List

from rich.console import Console
from rich.table import Table

from models import User, Project, Task
from utils import load_db, save_db, next_id

console = Console()

def find_user_by_name(name: str) -> Optional[dict]:
    db = load_db()
    for u in db["users"]:
        if u["name"].lower() == name.lower():
            return u
    return None


def find_project_by_title(title: str) -> Optional[dict]:
    db = load_db()
    for p in db["projects"]:
        if p["title"].lower() == title.lower():
            return p
    return None


def add_user(name: str, email: str) -> User:
    db = load_db()
    user_id = next_id(db["users"])
    user = User(user_id, name, email)
    db["users"].append(user.to_dict())
    save_db(db)
    console.print(f"[green]User created:[/green] {user}")
    return user


def list_users() -> None:
    db = load_db()
    table = Table(title="Users")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Email")

    if not db["users"]:
        console.print("[yellow]No users found.[/yellow]")
        return

    for u in db["users"]:
        table.add_row(str(u["id"]), u["name"], u["email"])
    console.print(table)


def add_project(user_name: str, title: str, description: str, due_date: str) -> Optional[Project]:
    db = load_db()
    user = find_user_by_name(user_name)
    if not user:
        console.print(f"[red]No user found with name '{user_name}'[/red]")
        return None
    project_id = next_id(db["projects"])
    project = Project(project_id, title, description, due_date, user["id"])
    db["projects"].append(project.to_dict())
    save_db(db)
    console.print(
        f"[green]Project created:[/green] {project.title} (Owner: {user['name']})"
    )
    return project


def list_projects(user_name: Optional[str] = None) -> None:
    db = load_db()
    projects = db["projects"]

    if user_name:
        user = find_user_by_name(user_name)
        if not user:
            console.print(f"[red]No user found with name '{user_name}'[/red]")
            return
        projects = [p for p in projects if p["user_id"] == user["id"]]

    table = Table(title="Projects")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("User ID")

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    for p in projects:
        table.add_row(
            str(p["id"]),
            p["title"],
            p.get("description", ""),
            p.get("due_date", ""),
            str(p["user_id"]),
        )
    console.print(table)


def add_task(project_title: str, title: str, assigned_to_name: Optional[str]) -> Optional[Task]:
    db = load_db()
    project = find_project_by_title(project_title)
    if not project:
        console.print(f"[red]No project found with title '{project_title}'[/red]")
        return None

    assigned_to_id = None
    if assigned_to_name:
        user = find_user_by_name(assigned_to_name)
        if not user:
            console.print(
                f"[yellow]Warning:[/yellow] no user named '{assigned_to_name}'. Task will be unassigned."
            )
        else:
            assigned_to_id = user["id"]

    task_id = next_id(db["tasks"])
    task = Task(task_id, title, project["id"], assigned_to=assigned_to_id)
    db["tasks"].append(task.to_dict())
    save_db(db)
    console.print(f"[green]Task created:[/green] {task.title} (Project: {project['title']})")
    return task


def list_tasks(project_title: Optional[str] = None) -> None:
    db = load_db()
    tasks: List[dict] = db["tasks"]

    if project_title:
        project = find_project_by_title(project_title)
        if not project:
            console.print(f"[red]No project found with title '{project_title}'[/red]")
            return
        tasks = [t for t in tasks if t["project_id"] == project["id"]]

    table = Table(title="Tasks")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("Project ID")
    table.add_column("Status")
    table.add_column("Assigned To")

    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    for t in tasks:
        assigned = str(t["assigned_to"]) if t.get("assigned_to") else "-"
        table.add_row(
            str(t["id"]),
            t["title"],
            str(t["project_id"]),
            t.get("status", "todo"),
            assigned,
        )
    console.print(table)


def complete_task(task_id: int) -> None:
    db = load_db()
    for t in db["tasks"]:
        if t["id"] == task_id:
            t["status"] = "done"
            save_db(db)
            console.print(f"[green]Task {task_id} marked as complete.[/green]")
            return
    console.print(f"[red]No task found with id {task_id}[/red]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI Project Management Tool",
        epilog="Example: python main.py add-user --name Alex --email alex@example.com",
    )
    subparsers = parser.add_subparsers(dest="command")

    # add-user
    user_parser = subparsers.add_parser("add-user", help="Create a new user")
    user_parser.add_argument("--name", required=True)
    user_parser.add_argument("--email", required=True)
    user_parser.set_defaults(func=lambda args: add_user(args.name, args.email))

    # list-users
    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.set_defaults(func=lambda args: list_users())

    # add-project
    proj_parser = subparsers.add_parser("add-project", help="Create a new project for a user")
    proj_parser.add_argument("--user", required=True, help="User name")
    proj_parser.add_argument("--title", required=True, help="Project title")
    proj_parser.add_argument("--description", default="", help="Project description")
    proj_parser.add_argument("--due-date", default="", help="Due date (YYYY-MM-DD)")
    proj_parser.set_defaults(
        func=lambda args: add_project(args.user, args.title, args.description, args.due_date)
    )

    # list-projects
    list_proj_parser = subparsers.add_parser("list-projects", help="List projects, optionally for a user")
    list_proj_parser.add_argument("--user", help="User name (optional)")
    list_proj_parser.set_defaults(func=lambda args: list_projects(args.user))

    # add-task
    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("--project", required=True, help="Project title")
    task_parser.add_argument("--title", required=True, help="Task title")
    task_parser.add_argument("--assigned-to", help="User name to assign task to")
    task_parser.set_defaults(
        func=lambda args: add_task(args.project, args.title, args.assigned_to)
    )

    # list-tasks
    list_task_parser = subparsers.add_parser("list-tasks", help="List tasks, optionally for a project")
    list_task_parser.add_argument("--project", help="Project title (optional)")
    list_task_parser.set_defaults(func=lambda args: list_tasks(args.project))

    # complete-task
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_task_parser.add_argument("--id", type=int, required=True, help="Task ID")
    complete_task_parser.set_defaults(func=lambda args: complete_task(args.id))

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
