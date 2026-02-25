import tkinter as tk
from tkinter import ttk
import time
import random
import numpy as np

class RAMLatencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAM Latency Measurement Tool")
        self.root.geometry("600x450")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="RAM Latency Measurement Tool",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Memory Size Input
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Array Size (in MB): ").grid(row=0, column=0)
        self.size_entry = tk.Entry(frame)
        self.size_entry.insert(0, "50")
        self.size_entry.grid(row=0, column=1)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Sequential Access Test",
                  command=self.sequential_test, width=25).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Random Access Test",
                  command=self.random_test, width=25).grid(row=0, column=1, padx=5)

        # Output Box
        self.output = tk.Text(self.root, height=15, width=70)
        self.output.pack(pady=10)

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def create_array(self):
        size_mb = int(self.size_entry.get())
        num_elements = (size_mb * 1024 * 1024) // 8
        return np.zeros(num_elements, dtype=np.float64)

    def sequential_test(self):
        self.output.delete(1.0, tk.END)
        arr = self.create_array()
        self.log("Running Sequential Access Test...")

        start = time.perf_counter_ns()
        for i in range(len(arr)):
            arr[i] += 1
        end = time.perf_counter_ns()

        total_time = end - start
        avg_latency = total_time / len(arr)

        self.log(f"Total Time: {total_time / 1e6:.2f} ms")
        self.log(f"Average Access Latency: {avg_latency:.2f} ns")

    def random_test(self):
        self.output.delete(1.0, tk.END)
        arr = self.create_array()
        self.log("Running Random Access Test...")

        indices = list(range(len(arr)))
        random.shuffle(indices)

        start = time.perf_counter_ns()
        for i in indices:
            arr[i] += 1
        end = time.perf_counter_ns()

        total_time = end - start
        avg_latency = total_time / len(arr)

        self.log(f"Total Time: {total_time / 1e6:.2f} ms")
        self.log(f"Average Access Latency: {avg_latency:.2f} ns")

if __name__ == "__main__":
    root = tk.Tk()
    app = RAMLatencyApp(root)
    root.mainloop()