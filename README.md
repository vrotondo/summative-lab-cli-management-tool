# summative-lab-cli-management-tool

Summative Lab: Python Project Management CLI Tool 
You will build a Python-based Command-Line Interface (CLI) application that manages a simulated multi-user project tracker system. The CLI should allow users to:

Create and manage users, projects, and tasks.
Display and search projects assigned to specific users.
Use file IO to persist data locally.
Use pip to manage external packages (e.g., for pretty printing, date formatting, or input validation).
Structure code using modules, classes, and object relationships.
Document, test, and debug your solution.
The Scenario: Create a Command-Line Project Management Tool 
You are tasked with creating a command-line project management tool for a team of developers. The tool should allow administrators to manage users, projects, and tasks through structured CLI commands. The system must support:

Creating and listing users via the command line.
Adding projects to specific users and displaying their associated projects.
Assigning tasks to projects and marking them as complete.
Editing and persisting project/task data using file I/O.
Navigating the tool with clear, user-friendly CLI commands.
Managing data relationships like one-to-many (users to projects) and many-to-many (projects to tasks with contributors).
Create and manage users, projects, and tasks.

Tools and Resources

PythonLinks to an external site. 3.10+
VS CodeLinks to an external site. (or IDE of your choice)
Git + GitHubLinks to an external site.
Python Standard LibraryLinks to an external site. (argparse, os, json, etc.
Optional: External packages such as rich or python-dateutil

Instructions

Task 1: Define the Problem
Design a CLI tool that enables:
Admins to manage users and projects.
Each user to have one or more projects.
Each project to have one or more tasks.
CLI commands to add, view, and update these entities.
Example CLI Actions:
add-user --name "Alex"
add-project --user "Alex" --title "CLI Tool"
add-task --project "CLI Tool" --title "Implement add-task"

Task 2: Determine the Design
Classes: User, Project, Task
Relationships:
One-to-many: User -> Projects
One-to-many: Project -> Tasks
Attributes
Users: name, email
Projects: title, description, due_date
Tasks: title, status, assigned_to
File Structure
main.py: CLI entry point
models/: contains class definitions
data/: local JSON or CSV file storage
utils/: helper functions, custom hooks
Persistence
Use json for saving/loading users, projects, and tasks
Package Setup:
External dependencies listed in requirements.txt

Task 3: Develop the Code
Set Up CLI Entry
Use argparse to define CLI structure.
Implement subcommands like add-user, list-projects, complete-task.
Build Object Model
Use classes for User, Project, and Task.
Apply __init__, instance methods, and relationships.
Use class methods to create or retrieve object collections.
Implement __str__() or __repr__() for clean CLI output.
Add OOP Features
Use @property and setter methods to control access to attributes.
Use class attributes (e.g., ID counters).
Add inheritance where appropriate (e.g., Person → User).
Configure File IO
Save and load objects via JSON files.
Handle missing files or malformed data with try-except.
Use Python scripting best practices (if __name__ == "__main__").
Use External Packages
Install and use at least one PyPi package (e.g., rich, tabulate, typer).
Track packages in requirements.txt.

Task 4: Test and Debug
Add unit tests for your class methods and CLI logic.
Test input/output interactions using mock data.
Use print/logging/debugger to trace logic.
Refactor large files into reusable modules.

Task 5: Document and Maintain
Comment on all class methods and utility functions.
Create a README.md with:
Setup instructions
How to run CLI commands
Overview of features and known issues
Ensure all code is pushed to GitHub.
Submission and Grading Criteria
Submit a public GitHub repo that includes:
Complete source code
Data files (JSON or CSV)
A README.md with clear instructions
Requirements.txt file with dependencies
Test files, if applicable
Review the rubric below as a guide for how this lab will be graded.
Complete your assignment using your preferred IDE.
When you are ready, push your final script to GitHub.
Share the link to your GitHub repo below and submit your assignment.
