import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
import time

class Interrupt:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority  # Lower number = higher priority

    def __lt__(self, other):
        return self.priority < other.priority

class InterruptSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interrupt Handling Simulator")
        self.root.geometry("700x500")
        
        self.interrupt_queue = PriorityQueue()
        self.create_widgets()
        self.task_running = False

    def create_widgets(self):
        title = tk.Label(self.root, text="Interrupt Handling Simulator", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        instruction = tk.Label(self.root, text="Enter CPU Task and Interrupts (Priority: 1=Highest)", font=("Arial", 11))
        instruction.pack(pady=5)

        # CPU Task Input
        tk.Label(self.root, text="CPU Task Name:").pack()
        self.task_entry = tk.Entry(self.root)
        self.task_entry.pack(pady=5)

        tk.Label(self.root, text="Interrupt Name:").pack()
        self.interrupt_entry = tk.Entry(self.root)
        self.interrupt_entry.pack(pady=5)

        tk.Label(self.root, text="Interrupt Priority (1-10):").pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack(pady=5)

        add_btn = tk.Button(self.root, text="Add Interrupt", command=self.add_interrupt)
        add_btn.pack(pady=10)

        run_btn = tk.Button(self.root, text="Run CPU Task", command=self.run_task)
        run_btn.pack(pady=5)

        self.log_box = tk.Text(self.root, height=15, width=80, state="disabled")
        self.log_box.pack(pady=10)

    def add_interrupt(self):
        name = self.interrupt_entry.get().strip()
        priority = self.priority_entry.get().strip()

        if not name or not priority.isdigit():
            messagebox.showerror("Error", "Enter valid interrupt name and priority")
            return

        priority = int(priority)
        interrupt = Interrupt(name, priority)
        self.interrupt_queue.put(interrupt)
        self.log(f"Interrupt '{name}' with priority {priority} added.")

    def run_task(self):
        if self.task_running:
            messagebox.showinfo("Info", "CPU Task already running")
            return

        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showerror("Error", "Enter CPU Task name")
            return

        self.task_running = True
        self.log(f"Starting CPU Task: {task_name}")
        self.root.update()
        time.sleep(1)

        # Check interrupts
        while not self.interrupt_queue.empty():
            interrupt = self.interrupt_queue.get()
            self.log(f"Interrupt '{interrupt.name}' occurred (Priority {interrupt.priority})")
            self.root.update()
            time.sleep(1)
            self.log(f"Handling Interrupt '{interrupt.name}' completed")
            self.root.update()
            time.sleep(0.5)

        self.log(f"CPU Task '{task_name}' completed")
        self.task_running = False

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterruptSimulator(root)
    root.mainloop()
