import tkinter as tk
from tkinter import messagebox
import time
import threading

class CPUClockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Clock Speed Controller Simulator")
        self.root.geometry("700x500")
        
        self.is_running = False
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="CPU Clock Speed Controller (Simulation)", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        tk.Label(self.root, text="Enter CPU Task Name:").pack()
        self.task_entry = tk.Entry(self.root)
        self.task_entry.pack(pady=5)

        tk.Label(self.root, text="Set CPU Clock Speed (MHz):").pack()
        self.clock_entry = tk.Entry(self.root)
        self.clock_entry.pack(pady=5)
        self.clock_entry.insert(0, "2400")  # Default 2.4 GHz

        run_btn = tk.Button(self.root, text="Run Task", command=self.run_task)
        run_btn.pack(pady=10)

        tk.Label(self.root, text="Simulation Log:").pack()
        self.log_box = tk.Text(self.root, height=15, width=80, state="disabled")
        self.log_box.pack(pady=10)

    def run_task(self):
        if self.is_running:
            messagebox.showinfo("Info", "Task already running")
            return

        task_name = self.task_entry.get().strip()
        clock_speed = self.clock_entry.get().strip()

        if not task_name or not clock_speed.isdigit():
            messagebox.showerror("Error", "Enter valid task name and clock speed")
            return

        self.is_running = True
        clock_speed = int(clock_speed)
        threading.Thread(target=self.simulate_task, args=(task_name, clock_speed), daemon=True).start()

    def simulate_task(self, task_name, clock_speed):
        self.log(f"Starting CPU Task '{task_name}' at {clock_speed} MHz")

        # Simulated execution time inversely proportional to clock speed
        base_cycles = 1_000_000
        exec_time = base_cycles / (clock_speed * 1_000_000)  # seconds

        for i in range(5):
            self.log(f"Running... ({i+1}/5)")
            time.sleep(exec_time)  # simulate processing

        self.log(f"Task '{task_name}' completed in ~{exec_time*5:.6f} seconds")
        self.is_running = False

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUClockSimulator(root)
    root.mainloop()
