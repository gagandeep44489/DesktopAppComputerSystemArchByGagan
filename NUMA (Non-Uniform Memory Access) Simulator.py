import tkinter as tk
from tkinter import ttk
import random
import time

class NUMASimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("NUMA (Non-Uniform Memory Access) Simulator")
        self.root.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="NUMA Simulator",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Node configuration
        tk.Label(frame, text="Number of NUMA Nodes:").grid(row=0, column=0, sticky="w")
        self.node_entry = tk.Entry(frame)
        self.node_entry.insert(0, "2")
        self.node_entry.grid(row=0, column=1)

        tk.Label(frame, text="Local Memory Latency (ns):").grid(row=1, column=0, sticky="w")
        self.local_latency = tk.Entry(frame)
        self.local_latency.insert(0, "80")
        self.local_latency.grid(row=1, column=1)

        tk.Label(frame, text="Remote Memory Latency (ns):").grid(row=2, column=0, sticky="w")
        self.remote_latency = tk.Entry(frame)
        self.remote_latency.insert(0, "150")
        self.remote_latency.grid(row=2, column=1)

        tk.Label(frame, text="Number of Memory Accesses:").grid(row=3, column=0, sticky="w")
        self.access_entry = tk.Entry(frame)
        self.access_entry.insert(0, "100000")
        self.access_entry.grid(row=3, column=1)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Run Simulation",
                  command=self.run_simulation, width=20).pack()

        self.output = tk.Text(self.root, height=15, width=80)
        self.output.pack(pady=10)

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def run_simulation(self):
        self.output.delete(1.0, tk.END)

        nodes = int(self.node_entry.get())
        local_ns = int(self.local_latency.get())
        remote_ns = int(self.remote_latency.get())
        accesses = int(self.access_entry.get())

        self.log("Starting NUMA Simulation...\n")

        total_latency = 0
        local_count = 0
        remote_count = 0

        for _ in range(accesses):
            accessing_node = random.randint(0, nodes - 1)
            memory_node = random.randint(0, nodes - 1)

            if accessing_node == memory_node:
                total_latency += local_ns
                local_count += 1
            else:
                total_latency += remote_ns
                remote_count += 1

        avg_latency = total_latency / accesses

        self.log(f"Total Memory Accesses: {accesses}")
        self.log(f"Local Accesses: {local_count}")
        self.log(f"Remote Accesses: {remote_count}")
        self.log(f"Total Simulated Latency: {total_latency / 1e6:.2f} ms")
        self.log(f"Average Access Latency: {avg_latency:.2f} ns")

if __name__ == "__main__":
    root = tk.Tk()
    app = NUMASimulator(root)
    root.mainloop()