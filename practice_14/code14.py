import tkinter as tk
from tkinter import messagebox


class TaskModel:
    #Модель: зберігає список завдань та бізнес-логіку.
    def __init__(self):
        self.tasks = []  # Список словників: {"title": str, "completed": bool}

    def add_task(self, title):
        if not title.strip():
            raise ValueError("Назва завдання не може бути порожньою.")
        self.tasks.append({"title": title.strip(), "completed": False})

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def get_tasks(self):
        return self.tasks


class TaskView(tk.Tk):
   # GUI
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Список завдань (MVC)")
        self.geometry("400x450")

        # Поле вводу
        self.entry_title = tk.Entry(self, font=("Arial", 12))
        self.entry_title.pack(fill=tk.X, padx=10, pady=10)

        # Кнопка додавання
        self.btn_add = tk.Button(self, text="Додати завдання", command=self.controller.handle_add)
        self.btn_add.pack(fill=tk.X, padx=10, pady=5)

        # Список (Listbox) для відображення
        self.listbox_tasks = tk.Listbox(self, font=("Arial", 11), selectmode=tk.SINGLE)
        self.listbox_tasks.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Кнопки керування
        self.btn_toggle = tk.Button(self, text="Змінити статус", command=self.controller.handle_toggle)
        self.btn_toggle.pack(fill=tk.X, padx=10, pady=5)

        self.btn_delete = tk.Button(self, text="Видалити", command=self.controller.handle_delete)
        self.btn_delete.pack(fill=tk.X, padx=10, pady=10)

    def get_input_title(self):
        return self.entry_title.get()

    def clear_input(self):
        self.entry_title.delete(0, tk.END)

    def get_selected_index(self):
        selection = self.listbox_tasks.curselection()
        return selection[0] if selection else None

    def update_view(self, tasks):
        self.listbox_tasks.delete(0, tk.END)
        for task in tasks:
            status = "Виконано" if task["completed"] else "Не виконано"
            self.listbox_tasks.insert(tk.END, f"«{task['title']}» — {status}")

    @staticmethod
    def show_error(message):
        messagebox.showerror("Помилка", message)


class TaskController:
    """Контролер: зв'язує Model та View, обробляє дії користувача."""
    def __init__(self, model):
        self.model = model
        self.view = TaskView(self)

    def run(self):
        self.view.mainloop()

    def handle_add(self):
        title = self.view.get_input_title()
        try:
            self.model.add_task(title)
            self.view.clear_input()
            self.view.update_view(self.model.get_tasks())
        except ValueError as e:
            self.view.show_error(str(e))

    def handle_toggle(self):
        index = self.view.get_selected_index()
        if index is not None:
            self.model.toggle_task(index)
            self.view.update_view(self.model.get_tasks())

    def handle_delete(self):
        index = self.view.get_selected_index()
        if index is not None:
            self.model.delete_task(index)
            self.view.update_view(self.model.get_tasks())


if __name__ == "__main__":
    model = TaskModel()
    controller = TaskController(model)
    controller.run()
