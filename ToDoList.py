import tkinter as tk
import sqlite3

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        
        self.conn = sqlite3.connect("todo.db")
        self.create_table()
        
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)
        
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()
        
        self.task_listbox = tk.Listbox(root, width=80)
        self.task_listbox.pack(pady=10)
        
        self.update_button = tk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.pack()
        
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()
        
        self.load_tasks()
        
    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL);''')
        self.conn.commit()
        
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.conn.execute("SELECT * FROM tasks").fetchall()
        for task in tasks:
            self.task_listbox.insert(tk.END, task[1])
            
    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            new_task = self.task_entry.get()
            if new_task:
                task_id = self.conn.execute("SELECT id FROM tasks LIMIT 1 OFFSET ?", (selected_index[0],)).fetchone()[0]
                self.conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
                self.conn.commit()
                self.load_tasks()
        
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = self.conn.execute("SELECT id FROM tasks LIMIT 1 OFFSET ?", (selected_index[0],)).fetchone()[0]
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            self.load_tasks()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
