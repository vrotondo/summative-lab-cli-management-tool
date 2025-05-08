#!/usr/bin/env python3
# main.py
import argparse
import sys
from datetime import datetime
from dateutil import parser

from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import load_users, save_users, load_projects, save_projects, load_tasks, save_tasks
from utils.cli_helpers import (
    print_title, print_success, print_error, print_warning,
    print_users_table, print_projects_table, print_tasks_table
)

def get_user_by_name_or_id(users, identifier):
    # Try to get by ID
    try:
        user_id = int(identifier)
        for user in users:
            if user.id == user_id:
                return user
    except ValueError:
        # Try to get by name
        for user in users:
            if user.name.lower() == identifier.lower():
                return user
    
    return None

def get_project_by_title_or_id(projects, identifier):
    # Try to get by ID
    try:
        project_id = int(identifier)
        for project in projects:
            if project.id == project_id:
                return project
    except ValueError:
        # Try to get by title
        for project in projects:
            if project.title.lower() == identifier.lower():
                return project
    
    return None

def get_task_by_title_or_id(tasks, identifier):
    # Try to get by ID
    try:
        task_id = int(identifier)
        for task in tasks:
            if task.id == task_id:
                return task
    except ValueError:
        # Try to get by title
        for task in tasks:
            if task.title.lower() == identifier.lower():
                return task
    
    return None

def handle_add_user(args):
    users = load_users()
    
    # Check if user with the same name already exists
    for user in users:
        if user.name.lower() == args.name.lower():
            print_error(f"User with name '{args.name}' already exists.")
            return
    
    user = User(args.name, args.email)
    users.append(user)
    save_users(users)
    
    print_success(f"User '{args.name}' added successfully with ID {user.id}.")

def handle_list_users(args):
    users = load_users()
    
    if args.id:
        # Filter by ID
        users = [user for user in users if user.id == args.id]
    
    print_users_table(users)

def handle_add_project(args):
    users = load_users()
    projects = load_projects()
    
    # Find the user
    user = get_user_by_name_or_id(users, args.user)
    if not user:
        print_error(f"User '{args.user}' not found.")
        return
    
    # Check if project with the same title already exists
    for project in projects:
        if project.title.lower() == args.title.lower():
            print_error(f"Project with title '{args.title}' already exists.")
            return
    
    # Parse due date
    try:
        due_date = parser.parse(args.due_date) if args.due_date else datetime.now()
    except ValueError:
        print_error(f"Invalid due date format: '{args.due_date}'.")
        return
    
    # Create project
    project = Project(args.title, args.description or "", due_date, user.id)
    projects.append(project)
    save_projects(projects)
    
    # Update user's projects
    user.add_project(project.id)
    save_users(users)
    
    print_success(f"Project '{args.title}' added successfully with ID {project.id}.")

def handle_list_projects(args):
    users = load_users()
    projects = load_projects()
    
    if args.user:
        # Find the user
        user = get_user_by_name_or_id(users, args.user)
        if not user:
            print_error(f"User '{args.user}' not found.")
            return
        
        # Filter projects by user
        projects = [project for project in projects if project.user_id == user.id]
    
    if args.id:
        # Filter by ID
        projects = [project for project in projects if project.id == args.id]
    
    print_projects_table(projects, users)

def handle_add_task(args):
    users = load_users()
    projects = load_projects()
    tasks = load_tasks()
    
    # Find the project
    project = get_project_by_title_or_id(projects, args.project)
    if not project:
        print_error(f"Project '{args.project}' not found.")
        return
    
    # Check if task with the same title already exists in the project
    for task in tasks:
        if task.project_id == project.id and task.title.lower() == args.title.lower():
            print_error(f"Task with title '{args.title}' already exists in project '{project.title}'.")
            return
    
    # Find the assigned user if provided
    assigned_user_id = None
    if args.assign:
        assigned_user = get_user_by_name_or_id(users, args.assign)
        if not assigned_user:
            print_error(f"User '{args.assign}' not found.")
            return
        assigned_user_id = assigned_user.id
    
    # Create task
    task = Task(args.title, args.description or "", project.id, assigned_user_id)
    tasks.append(task)
    save_tasks(tasks)
    
    # Update project's tasks
    project.add_task(task.id)
    save_projects(projects)
    
    print_success(f"Task '{args.title}' added successfully with ID {task.id}.")

def handle_list_tasks(args):
    users = load_users()
    projects = load_projects()
    tasks = load_tasks()
    
    if args.project:
        # Find the project
        project = get_project_by_title_or_id(projects, args.project)
        if not project:
            print_error(f"Project '{args.project}' not found.")
            return
        
        # Filter tasks by project
        tasks = [task for task in tasks if task.project_id == project.id]
    
    if args.status:
        # Validate status
        if args.status not in Task.VALID_STATUSES:
            print_error(f"Invalid status: '{args.status}'. Valid statuses are: {', '.join(Task.VALID_STATUSES)}.")
            return
        
        # Filter tasks by status
        tasks = [task for task in tasks if task.status == args.status]
    
    print_tasks_table(tasks, projects, users)

def handle_complete_task(args):
    tasks = load_tasks()
    
    # Find the task
    task = get_task_by_title_or_id(tasks, args.task)
    if not task:
        print_error(f"Task '{args.task}' not found.")
        return
    
    # Check if already completed
    if task.status == 'completed':
        print_warning(f"Task '{task.title}' is already completed.")
        return
    
    # Update task status
    task.mark_completed()
    save_tasks(tasks)
    
    print_success(f"Task '{task.title}' marked as completed.")

def handle_update_task(args):
    users = load_users()
    tasks = load_tasks()
    
    # Find the task
    task = get_task_by_title_or_id(tasks, args.task)
    if not task:
        print_error(f"Task '{args.task}' not found.")
        return
    
    # Update title if provided
    if args.title:
        task.title = args.title
    
    # Update description if provided
    if args.description:
        task.description = args.description
    
    # Update status if provided
    if args.status:
        if args.status not in Task.VALID_STATUSES:
            print_error(f"Invalid status: '{args.status}'. Valid statuses are: {', '.join(Task.VALID_STATUSES)}.")
            return
        task.status = args.status
    
    # Update assigned user if provided
    if args.assign:
        if args.assign.lower() == 'none':
            task.assigned_to = None
        else:
            assigned_user = get_user_by_name_or_id(users, args.assign)
            if not assigned_user:
                print_error(f"User '{args.assign}' not found.")
                return
            task.assigned_to = assigned_user.id
    
    save_tasks(tasks)
    
    print_success(f"Task '{task.title}' updated successfully.")

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add user command
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="User name")
    add_user_parser.add_argument("--email", required=True, help="User email")
    
    # List users command
    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.add_argument("--id", type=int, help="Filter by user ID")
    
    # Add project command
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("--user", required=True, help="User name or ID")
    add_project_parser.add_argument("--title", required=True, help="Project title")
    add_project_parser.add_argument("--description", help="Project description")
    add_project_parser.add_argument("--due-date", help="Project due date (YYYY-MM-DD)")
    
    # List projects command
    list_projects_parser = subparsers.add_parser("list-projects", help="List all projects")
    list_projects_parser.add_argument("--user", help="Filter by user name or ID")
    list_projects_parser.add_argument("--id", type=int, help="Filter by project ID")
    
    # Add task command
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_task_parser.add_argument("--project", required=True, help="Project title or ID")
    add_task_parser.add_argument("--title", required=True, help="Task title")
    add_task_parser.add_argument("--description", help="Task description")
    add_task_parser.add_argument("--assign", help="Assign to user (name or ID)")
    
    # List tasks command
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List all tasks")
    list_tasks_parser.add_argument("--project", help="Filter by project title or ID")
    list_tasks_parser.add_argument("--status", help="Filter by status")
    
    # Complete task command
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as completed")
    complete_task_parser.add_argument("--task", required=True, help="Task title or ID")
    
    # Update task command
    update_task_parser = subparsers.add_parser("update-task", help="Update a task")
    update_task_parser.add_argument("--task", required=True, help="Task title or ID")
    update_task_parser.add_argument("--title", help="New task title")
    update_task_parser.add_argument("--description", help="New task description")
    update_task_parser.add_argument("--status", help="New task status")
    update_task_parser.add_argument("--assign", help="Assign to user (name or ID, or 'none' to unassign)")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "add-user":
        handle_add_user(args)
    elif args.command == "list-users":
        handle_list_users(args)
    elif args.command == "add-project":
        handle_add_project(args)
    elif args.command == "list-projects":
        handle_list_projects(args)
    elif args.command == "add-task":
        handle_add_task(args)
    elif args.command == "list-tasks":
        handle_list_tasks(args)
    elif args.command == "complete-task":
        handle_complete_task(args)
    elif args.command == "update-task":
        handle_update_task(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()