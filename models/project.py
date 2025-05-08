# models/project.py
from datetime import datetime
from dateutil import parser

class Project:
    # Class attribute to keep track of project IDs
    _next_id = 1
    
    def __init__(self, title, description, due_date, user_id):
        self._id = Project._next_id
        Project._next_id += 1
        self._title = title
        self._description = description
        self._user_id = user_id
        self._tasks = []

        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        
        # Handle due_date as string or datetime
        if isinstance(due_date, str):
            try:
                self._due_date = parser.parse(due_date)
            except ValueError:
                raise ValueError("Invalid due date format")
        elif isinstance(due_date, datetime):
            self._due_date = due_date
        else:
            raise TypeError("Due date must be a string or datetime object")
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value
    
    @property
    def due_date(self):
        return self._due_date
    
    @due_date.setter
    def due_date(self, value):
        if isinstance(value, str):
            try:
                self._due_date = parser.parse(value)
            except ValueError:
                raise ValueError("Invalid due date format")
        elif isinstance(value, datetime):
            self._due_date = value
        else:
            raise TypeError("Due date must be a string or datetime object")
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def tasks(self):
        return self._tasks
    
    def add_task(self, task_id):
        if task_id not in self._tasks:
            self._tasks.append(task_id)
    
    def remove_task(self, task_id):
        if task_id in self._tasks:
            self._tasks.remove(task_id)
    
    def to_dict(self):
        return {
            'id': self._id,
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date.isoformat(),
            'user_id': self._user_id,
            'tasks': self._tasks
        }
    
    @classmethod
    def from_dict(cls, data):
        project = cls(
            data['title'],
            data['description'],
            data['due_date'],
            data['user_id']
        )
        project._id = data['id']
        project._tasks = data['tasks']
        
        # Update next_id to avoid ID collisions
        if project._id >= cls._next_id:
            cls._next_id = project._id + 1
            
        return project
    
    def __str__(self):
        return f"Project(id={self._id}, title={self._title}, due_date={self._due_date.strftime('%Y-%m-%d')}, tasks={len(self._tasks)})"
    
    def __repr__(self):
        return f"Project(id={self._id}, title={self._title}, description={self._description}, due_date={self._due_date}, user_id={self._user_id}, tasks={self._tasks})"