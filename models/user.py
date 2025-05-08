# models/user.py
class User:
    # Class attribute to keep track of user IDs
    _next_id = 1
    
    def __init__(self, name, email):
        self._id = User._next_id
        User._next_id += 1
        self._name = name
        self._email = email
        self._projects = []
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str) or '@' not in value:
            raise ValueError("Email must be a valid email address")
        self._email = value
    
    @property
    def projects(self):
        return self._projects
    
    def add_project(self, project_id):
        if project_id not in self._projects:
            self._projects.append(project_id)
    
    def remove_project(self, project_id):
        if project_id in self._projects:
            self._projects.remove(project_id)
    
    def to_dict(self):
        return {
            'id': self._id,
            'name': self._name,
            'email': self._email,
            'projects': self._projects
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(data['name'], data['email'])
        user._id = data['id']
        user._projects = data['projects']
        
        # Update next_id to avoid ID collisions
        if user._id >= cls._next_id:
            cls._next_id = user._id + 1
            
        return user
    
    def __str__(self):
        return f"User(id={self._id}, name={self._name}, email={self._email}, projects={len(self._projects)})"
    
    def __repr__(self):
        return f"User(id={self._id}, name={self._name}, email={self._email}, projects={self._projects})"