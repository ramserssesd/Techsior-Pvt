import sqlite3
from datetime import datetime

# Database connection and initialization
DB_FILE = "tasks.db"

def initialize_db():
    """Initialize the SQLite database and create the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

# CRUD Operations
def add_task(description, deadline=None):
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (description, deadline, status)
        VALUES (?, ?, ?)
    """, (description, deadline, "pending"))
    conn.commit()
    conn.close()
    print("Task added successfully!")

def view_tasks(filter_status=None):
    """View all tasks or filter by status."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT id, description, deadline, status FROM tasks"
    if filter_status:
        query += f" WHERE status = '{filter_status}'"
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print(f"No {filter_status if filter_status else 'tasks'} found.")
    else:
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}")

def update_task(task_id, new_description=None, new_status=None):
    """Update a task's description or status."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    task = get_task_by_id(task_id)
    if not task:
        print("Task not found!")
        return

    description = new_description if new_description else task[1]
    status = new_status if new_status else task[3]

    cursor.execute("""
        UPDATE tasks
        SET description = ?, status = ?
        WHERE id = ?
    """, (description, status, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully!")

def delete_task(task_id):
    """Delete a task by its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    task = get_task_by_id(task_id)
    if not task:
        print("Task not found!")
        return

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

def get_task_by_id(task_id):
    """Retrieve a task by its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

# CLI Interface
def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\n--- Task Management System ---")
        print("1. Add a Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Update a Task")
        print("6. Delete a Task")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD, optional): ") or None
            add_task(description, deadline)

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            view_tasks(filter_status="pending")

        elif choice == "4":
            view_tasks(filter_status="completed")

        elif choice == "5":
            task_id = input("Enter the task ID to update: ")
            new_description = input("Enter new description (leave blank to keep current): ") or None
            new_status = input("Enter new status (pending/completed, leave blank to keep current): ") or None
            update_task(int(task_id), new_description, new_status)

        elif choice == "6":
            task_id = input("Enter the task ID to delete: ")
            delete_task(int(task_id))

        elif choice == "7":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    initialize_db()
    main_menu()