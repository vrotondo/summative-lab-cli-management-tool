# models/task.py
class Task:
    # Class attribute to keep track of task IDs
    _next_id = 1
    
    # Valid status values
    VALID_STATUSES = ['pending', 'in_progress', 'completed', 'cancelled']
    
    def __init__(self, title, description, project_id, assigned_to=None, status='pending'):
        self._id = Task._next_id
        Task._next_id += 1
        self._title = title
        self._description = description
        self._project_id = project_id
        self._assigned_to = assigned_to
        self._status = status
        
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(Task.VALID_STATUSES)}")
    
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
    def project_id(self):
        return self._project_id
    
    @property
    def assigned_to(self):
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value):
        self._assigned_to = value
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(Task.VALID_STATUSES)}")
        self._status = value
    
    def mark_completed(self):
        self._status = 'completed'
    
    def to_dict(self):
        return {
            'id': self._id,
            'title': self._title,
            'description': self._description,
            'status': self._status,
            'project_id': self._project_id,
            'assigned_to': self._assigned_to
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(
            data['title'],
            data['description'],
            data['project_id'],
            data['assigned_to'],
            data['status']
        )
        task._id = data['id']
        
        # Update next_id to avoid ID collisions
        if task._id >= cls._next_id:
            cls._next_id = task._id + 1
            
        return task
    
    def __str__(self):
        return f"Task(id={self._id}, title={self._title}, status={self._status})"
    
    def __repr__(self):
        return f"Task(id={self._id}, title={self._title}, description={self._description}, status={self._status}, project_id={self._project_id}, assigned_to={self._assigned_to})"