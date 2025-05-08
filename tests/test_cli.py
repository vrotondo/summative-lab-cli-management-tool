# tests/test_cli.py
import unittest
import os
import json
import tempfile
import shutil
import sys
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from models.project import Project
from models.task import Task
import main  

@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for data files
        self.temp_dir = tempfile.mkdtemp()
        
        # Patch DATA_DIR in file_handler
        self.patcher = patch('utils.file_handler.DATA_DIR', self.temp_dir)
        self.patcher.start()
        
        # Create a test user
        self.test_user = User("Test User", "test@example.com")
        
        # Create a test project
        self.test_project = Project("Test Project", "Test Description", "2023-12-31", self.test_user.id)
        
        # Create a test task
        self.test_task = Task("Test Task", "Test Description", self.test_project.id, self.test_user.id)
        
        # Save test data
        with open(os.path.join(self.temp_dir, 'users.json'), 'w') as f:
            json.dump([self.test_user.to_dict()], f)
        
        with open(os.path.join(self.temp_dir, 'projects.json'), 'w') as f:
            json.dump([self.test_project.to_dict()], f)
        
        with open(os.path.join(self.temp_dir, 'tasks.json'), 'w') as f:
            json.dump([self.test_task.to_dict()], f)
    
    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.temp_dir)
    
    def test_add_user(self):
        with patch('sys.argv', ['main.py', 'add-user', '--name', 'New User', '--email', 'new@example.com']):
            with capture_output() as (out, err):
                main.main()
        
        # Check that the user was added
        with open(os.path.join(self.temp_dir, 'users.json'), 'r') as f:
            users_data = json.load(f)
        
        self.assertEqual(len(users_data), 2)
        self.assertTrue(any(user['name'] == 'New User' for user in users_data))
        self.assertTrue(any(user['email'] == 'new@example.com' for user in users_data))
    
    def test_add_project(self):
        with patch('sys.argv', ['main.py', 'add-project', 
                              '--user', 'Test User', 
                              '--title', 'New Project', 
                              '--description', 'New Description', 
                              '--due-date', '2024-12-31']):
            with capture_output() as (out, err):
                main.main()
        
        # Check that the project was added
        with open(os.path.join(self.temp_dir, 'projects.json'), 'r') as f:
            projects_data = json.load(f)
        
        self.assertEqual(len(projects_data), 2)
        self.assertTrue(any(project['title'] == 'New Project' for project in projects_data))
        self.assertTrue(any(project['description'] == 'New Description' for project in projects_data))
    
    def test_add_task(self):
        with patch('sys.argv', ['main.py', 'add-task', 
                              '--project', 'Test Project', 
                              '--title', 'New Task', 
                              '--description', 'New Description', 
                              '--assign', 'Test User']):
            with capture_output() as (out, err):
                main.main()
        
        # Check that the task was added
        with open(os.path.join(self.temp_dir, 'tasks.json'), 'r') as f:
            tasks_data = json.load(f)
        
        self.assertEqual(len(tasks_data), 2)
        self.assertTrue(any(task['title'] == 'New Task' for task in tasks_data))
        self.assertTrue(any(task['description'] == 'New Description' for task in tasks_data))
    
    def test_complete_task(self):
        with patch('sys.argv', ['main.py', 'complete-task', '--task', 'Test Task']):
            with capture_output() as (out, err):
                main.main()
        
        # Check that the task was completed
        with open(os.path.join(self.temp_dir, 'tasks.json'), 'r') as f:
            tasks_data = json.load(f)
        
        self.assertEqual(len(tasks_data), 1)
        self.assertEqual(tasks_data[0]['status'], 'completed')
    
    def test_update_task(self):
        with patch('sys.argv', ['main.py', 'update-task', 
                              '--task', 'Test Task', 
                              '--title', 'Updated Task', 
                              '--description', 'Updated Description', 
                              '--status', 'in_progress']):
            with capture_output() as (out, err):
                main.main()
        
        # Check that the task was updated
        with open(os.path.join(self.temp_dir, 'tasks.json'), 'r') as f:
            tasks_data = json.load(f)
        
        self.assertEqual(len(tasks_data), 1)
        self.assertEqual(tasks_data[0]['title'], 'Updated Task')
        self.assertEqual(tasks_data[0]['description'], 'Updated Description')
        self.assertEqual(tasks_data[0]['status'], 'in_progress')

if __name__ == "__main__":
    unittest.main()