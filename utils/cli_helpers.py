# utils/cli_helpers.py
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

def print_title(title):
    console.print(f"\n[bold blue]{title}[/bold blue]")

def print_success(message):
    console.print(f"[bold green]✓[/bold green] {message}")

def print_error(message):
    console.print(f"[bold red]✗[/bold red] {message}")

def print_warning(message):
    console.print(f"[bold yellow]![/bold yellow] {message}")

def print_users_table(users):
    if not users:
        print_warning("No users found.")
        return
    
    table = Table(title="Users")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Email")
    table.add_column("Projects", justify="right")
    
    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )
    
    console.print(table)

def print_projects_table(projects, users=None):
    if not projects:
        print_warning("No projects found.")
        return
    
    table = Table(title="Projects")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold")
    table.add_column("Owner")
    table.add_column("Due Date")
    table.add_column("Tasks", justify="right")
    
    user_dict = {}
    if users:
        user_dict = {user.id: user.name for user in users}
    
    for project in projects:
        owner_name = user_dict.get(project.user_id, f"User {project.user_id}")
        due_date = project.due_date.strftime("%Y-%m-%d")
        
        # Highlight due dates
        now = datetime.now()
        if project.due_date < now:
            due_date_str = f"[bold red]{due_date}[/bold red]"
        elif (project.due_date - now).days <= 7:
            due_date_str = f"[bold yellow]{due_date}[/bold yellow]"
        else:
            due_date_str = due_date
        
        table.add_row(
            str(project.id),
            project.title,
            owner_name,
            due_date_str,
            str(len(project.tasks))
        )
    
    console.print(table)

def print_tasks_table(tasks, projects=None, users=None):
    if not tasks:
        print_warning("No tasks found.")
        return
    
    table = Table(title="Tasks")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold")
    table.add_column("Project")
    table.add_column("Assigned To")
    table.add_column("Status")
    
    project_dict = {}
    if projects:
        project_dict = {project.id: project.title for project in projects}
    
    user_dict = {}
    if users:
        user_dict = {user.id: user.name for user in users}
    
    for task in tasks:
        project_name = project_dict.get(task.project_id, f"Project {task.project_id}")
        
        if task.assigned_to:
            assigned_name = user_dict.get(task.assigned_to, f"User {task.assigned_to}")
        else:
            assigned_name = "Unassigned"
        
        # Color status
        if task.status == 'completed':
            status_str = f"[bold green]{task.status}[/bold green]"
        elif task.status == 'in_progress':
            status_str = f"[bold blue]{task.status}[/bold blue]"
        elif task.status == 'cancelled':
            status_str = f"[bold red]{task.status}[/bold red]"
        else:
            status_str = f"[bold yellow]{task.status}[/bold yellow]"
        
        table.add_row(
            str(task.id),
            task.title,
            project_name,
            assigned_name,
            status_str
        )
    
    console.print(table)