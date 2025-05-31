import tkinter as tk
from tkinter import messagebox
import json
import os
import customtkinter as ctk
import tkinter.font as tkFont

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to read tasks. Corrupted file.")
            return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.tasks = load_tasks()
        self.task_vars = []
        self.task_var = tk.StringVar()

        self.default_font = tkFont.Font(family="Helvetica", size=14)
        self.strike_font = tkFont.Font(family="Helvetica", size=14, overstrike=1)

        self.entry = ctk.CTkEntry(root, textvariable=self.task_var, width=300)
        self.entry.pack(pady=10, padx=10)

        self.add_button = ctk.CTkButton(root, text="Add ➕", command=self.add_task, corner_radius=10)
        self.add_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(root, text="Delete 🗑️", command=self.delete_task, corner_radius=10)
        self.delete_button.pack(pady=5)

        self.heading = ctk.CTkLabel(root, text="Tasks", font=("Helvetica", 16, "bold"))
        self.heading.pack(pady=10)

        self.tasks_frame = tk.Frame(root, bg="#242424")  # fallback dark background
        self.tasks_frame.pack(expand=True, fill="both", padx=10)

        self.refresh_task_list()

    def refresh_task_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        self.task_vars = []

        for index, task in enumerate(self.tasks):
            var = tk.BooleanVar(value=task.get("completed", False))
            font = self.strike_font if var.get() else self.default_font
            cb = tk.Checkbutton(
                self.tasks_frame,
                text=task["description"],
                variable=var,
                font=font,
                fg="white",
                bg="#242424",
                activebackground="#242424",
                activeforeground="white",
                selectcolor="#242424",
                command=lambda idx=index, v=var: self.toggle_task(idx, v)
            )
            cb.pack(anchor='w')
            self.task_vars.append(var)

    def add_task(self):
        description = self.task_var.get().strip()
        if description:
            self.tasks.append({'description': description, 'completed': False})
            save_tasks(self.tasks)
            self.task_var.set("")
            self.refresh_task_list()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def delete_task(self):
        indices_to_delete = [i for i, var in enumerate(self.task_vars) if var.get()]
        if not indices_to_delete:
            messagebox.showwarning("Selection Error", "No tasks selected for deletion.")
            return
        for index in reversed(indices_to_delete):
            del self.tasks[index]
        save_tasks(self.tasks)
        self.refresh_task_list()

    def toggle_task(self, index, var):
        self.tasks[index]['completed'] = var.get()
        save_tasks(self.tasks)
        self.refresh_task_list()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = ToDoApp(root)
    root.mainloop()
