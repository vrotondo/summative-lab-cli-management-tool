# utils/file_handler.py
import json
import os
from models.user import User
from models.project import Project
from models.task import Task

# Define data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_users(users):
    ensure_data_dir()
    users_data = [user.to_dict() for user in users]
    with open(os.path.join(DATA_DIR, 'users.json'), 'w') as f:
        json.dump(users_data, f, indent=2)

def load_users():
    ensure_data_dir()
    try:
        with open(os.path.join(DATA_DIR, 'users.json'), 'r') as f:
            users_data = json.load(f)
            return [User.from_dict(user_data) for user_data in users_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_projects(projects):
    ensure_data_dir()
    projects_data = [project.to_dict() for project in projects]
    with open(os.path.join(DATA_DIR, 'projects.json'), 'w') as f:
        json.dump(projects_data, f, indent=2)

def load_projects():
    ensure_data_dir()
    try:
        with open(os.path.join(DATA_DIR, 'projects.json'), 'r') as f:
            projects_data = json.load(f)
            return [Project.from_dict(project_data) for project_data in projects_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    ensure_data_dir()
    tasks_data = [task.to_dict() for task in tasks]
    with open(os.path.join(DATA_DIR, 'tasks.json'), 'w') as f:
        json.dump(tasks_data, f, indent=2)

def load_tasks():
    ensure_data_dir()
    try:
        with open(os.path.join(DATA_DIR, 'tasks.json'), 'r') as f:
            tasks_data = json.load(f)
            return [Task.from_dict(task_data) for task_data in tasks_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []