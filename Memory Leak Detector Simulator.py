import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Memory simulation variables
allocations = []
memory_history = []

# -----------------------------
# Simulate memory allocation
# -----------------------------
def allocate_memory():
    # Allocate random bytes (simulate memory usage)
    mem = random.randint(10, 100)  # bytes
    allocations.append(mem)
    update_memory_history()
    
# -----------------------------
# Simulate memory deallocation
# -----------------------------
def deallocate_memory():
    if allocations:
        allocations.pop(0)  # Free oldest allocation
    update_memory_history()

# -----------------------------
# Update memory usage history
# -----------------------------
def update_memory_history():
    total_mem = sum(allocations)
    memory_history.append(total_mem)
    memory_text.delete("1.0", tk.END)
    memory_text.insert(tk.END, f"Current Allocated Memory: {total_mem} bytes\n")
    memory_text.insert(tk.END, f"Number of allocations: {len(allocations)}\n")

# -----------------------------
# Plot memory usage
# -----------------------------
def plot_memory():
    if not memory_history:
        messagebox.showwarning("No Data", "No memory usage data to plot.")
        return
    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(memory_history, marker='o', linestyle='-', color='blue')
    ax.set_title("Memory Usage Over Time")
    ax.set_xlabel("Simulation Step")
    ax.set_ylabel("Allocated Memory (bytes)")
    plt.show()

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Memory Leak Detector Simulator")
root.geometry("550x400")

tk.Label(root, text="Memory Leak Detector Simulator",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Allocate Memory", command=allocate_memory,
          bg="green", fg="white", width=20).pack(pady=5)

tk.Button(root, text="Deallocate Memory", command=deallocate_memory,
          bg="red", fg="white", width=20).pack(pady=5)

tk.Button(root, text="Plot Memory Usage", command=plot_memory,
          bg="blue", fg="white", width=20).pack(pady=5)

tk.Label(root, text="Memory Status:", font=("Arial", 12, "bold")).pack(pady=5)

memory_text = tk.Text(root, height=8, width=60, bg="#f4f4f4")
memory_text.pack(padx=10, pady=5)

root.mainloop()