import os
import json

# Define the file to save the tasks
TASKS_FILE = 'tasks.json'

# Define a class for tasks
class Task:
    def __init__(self, title, description):
        self.id = None
        self.title = title
        self.description = description
        self.completed = False

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(task_dict):
        task = Task(task_dict['title'], task_dict['description'])
        task.id = task_dict['id']
        task.completed = task_dict['completed']
        return task

# Define a class for the to-do list
class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description):
        task = Task(title, description)
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            for task in self.tasks:
                status = 'Completed' if task.completed else 'Not completed'
                print(f"ID: {task.id}, Title: {task.title}, Description: {task.description}, Status: {status}")

    def mark_task(self, task_id, completed=True):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = completed
                self.save_tasks()
                return
        print(f"No task found with ID {task_id}.")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        # Reassign IDs after deletion
        for i, task in enumerate(self.tasks):
            task.id = i + 1
        self.save_tasks()

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, file, indent=4)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as file:
                tasks_dict = json.load(file)
                self.tasks = [Task.from_dict(task_dict) for task_dict in tasks_dict]
        else:
            self.tasks = []

# Define a function to display the menu
def display_menu():
    print("To-Do List Application")
    print("=======================")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Task as Complete")
    print("4. Mark Task as Incomplete")
    print("5. Delete Task")
    print("6. Exit")

# Main function to run the application
def main():
    todo_list = ToDoList()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            todo_list.add_task(title, description)
        elif choice == '2':
            todo_list.list_tasks()
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as complete: "))
            todo_list.mark_task(task_id, completed=True)
        elif choice == '4':
            task_id = int(input("Enter task ID to mark as incomplete: "))
            todo_list.mark_task(task_id, completed=False)
        elif choice == '5':
            task_id = int(input("Enter task ID to delete: "))
            todo_list.delete_task(task_id)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
