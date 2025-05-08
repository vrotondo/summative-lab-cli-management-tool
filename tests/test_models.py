# tests/test_models.py
import unittest
from datetime import datetime
from models.user import User
from models.project import Project
from models.task import Task

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("Test User", "test@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.projects, [])
    
    def test_user_validation(self):
        user = User("Test User", "test@example.com")
        
        # Test email validation
        with self.assertRaises(ValueError):
            user.email = "invalid-email"
        
        # Test name validation
        with self.assertRaises(ValueError):
            user.name = ""
    
    def test_user_projects(self):
        user = User("Test User", "test@example.com")
        user.add_project(1)
        self.assertEqual(user.projects, [1])
        
        user.add_project(2)
        self.assertEqual(user.projects, [1, 2])
        
        # Adding a duplicate project should not change anything
        user.add_project(1)
        self.assertEqual(user.projects, [1, 2])
        
        user.remove_project(1)
        self.assertEqual(user.projects, [2])
    
    def test_user_to_dict(self):
        user = User("Test User", "test@example.com")
        user.add_project(1)
        
        user_dict = user.to_dict()
        self.assertEqual(user_dict["name"], "Test User")
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["projects"], [1])
    
    def test_user_from_dict(self):
        user_dict = {
            "id": 10,
            "name": "Test User",
            "email": "test@example.com",
            "projects": [1, 2]
        }
        
        user = User.from_dict(user_dict)
        self.assertEqual(user.id, 10)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.projects, [1, 2])

class TestProject(unittest.TestCase):
    def test_project_creation(self):
        project = Project("Test Project", "Test Description", "2023-12-31", 1)
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "Test Description")
        self.assertEqual(project.due_date.strftime("%Y-%m-%d"), "2023-12-31")
        self.assertEqual(project.user_id, 1)
        self.assertEqual(project.tasks, [])
    
    def test_project_validation(self):
        # Test title validation
        with self.assertRaises(ValueError):
            Project("", "Test Description", "2023-12-31", 1)
        
        # Test due date validation
        with self.assertRaises(ValueError):
            Project("Test Project", "Test Description", "invalid-date", 1)
    
    def test_project_tasks(self):
        project = Project("Test Project", "Test Description", "2023-12-31", 1)
        project.add_task(1)
        self.assertEqual(project.tasks, [1])
        
        project.add_task(2)
        self.assertEqual(project.tasks, [1, 2])
        
        # Adding a duplicate task should not change anything
        project.add_task(1)
        self.assertEqual(project.tasks, [1, 2])
        
        project.remove_task(1)
        self.assertEqual(project.tasks, [2])
    
    def test_project_to_dict(self):
        project = Project("Test Project", "Test Description", "2023-12-31", 1)
        project.add_task(1)
        
        project_dict = project.to_dict()
        self.assertEqual(project_dict["title"], "Test Project")
        self.assertEqual(project_dict["description"], "Test Description")
        self.assertTrue("2023-12-31" in project_dict["due_date"])
        self.assertEqual(project_dict["user_id"], 1)
        self.assertEqual(project_dict["tasks"], [1])
    
    def test_project_from_dict(self):
        project_dict = {
            "id": 10,
            "title": "Test Project",
            "description": "Test Description",
            "due_date": "2023-12-31T00:00:00",
            "user_id": 1,
            "tasks": [1, 2]
        }
        
        project = Project.from_dict(project_dict)
        self.assertEqual(project.id, 10)
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "Test Description")
        self.assertEqual(project.due_date.strftime("%Y-%m-%d"), "2023-12-31")
        self.assertEqual(project.user_id, 1)
        self.assertEqual(project.tasks, [1, 2])

class TestTask(unittest.TestCase):
    def test_task_creation(self):
        task = Task("Test Task", "Test Description", 1, 2)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.assigned_to, 2)
        self.assertEqual(task.status, "pending")
    
    def test_task_validation(self):
        # Test title validation
        with self.assertRaises(ValueError):
            Task("", "Test Description", 1)
        
        # Test status validation
        with self.assertRaises(ValueError):
            task = Task("Test Task", "Test Description", 1)
            task.status = "invalid-status"
    
    def test_task_completion(self):
        task = Task("Test Task", "Test Description", 1)
        self.assertEqual(task.status, "pending")
        
        task.mark_completed()
        self.assertEqual(task.status, "completed")
    
    def test_task_to_dict(self):
        task = Task("Test Task", "Test Description", 1, 2, "in_progress")
        
        task_dict = task.to_dict()
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["description"], "Test Description")
        self.assertEqual(task_dict["project_id"], 1)
        self.assertEqual(task_dict["assigned_to"], 2)
        self.assertEqual(task_dict["status"], "in_progress")
    
    def test_task_from_dict(self):
        task_dict = {
            "id": 10,
            "title": "Test Task",
            "description": "Test Description",
            "project_id": 1,
            "assigned_to": 2,
            "status": "in_progress"
        }
        
        task = Task.from_dict(task_dict)
        self.assertEqual(task.id, 10)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.assigned_to, 2)
        self.assertEqual(task.status, "in_progress")

if __name__ == "__main__":
    unittest.main()