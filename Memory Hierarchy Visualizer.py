import tkinter as tk
import matplotlib.pyplot as plt

def show_visualization():
    # Memory hierarchy data (relative scale)
    levels = ["Registers", "L1 Cache", "L2 Cache", "L3 Cache", "RAM", "SSD/HDD"]
    access_time = [1, 2, 5, 10, 50, 200]  # Relative latency
    capacity = [1, 2, 4, 8, 32, 128]  # Relative size

    plt.figure()
    plt.plot(levels, access_time)
    plt.title("Memory Hierarchy - Access Time (Relative)")
    plt.xlabel("Memory Level")
    plt.ylabel("Access Time (Lower is Faster)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(levels, capacity)
    plt.title("Memory Hierarchy - Storage Capacity (Relative)")
    plt.xlabel("Memory Level")
    plt.ylabel("Capacity (Higher is Larger)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Memory Hierarchy Visualizer")
root.geometry("500x350")

tk.Label(root, text="Memory Hierarchy Visualizer", font=("Arial", 16)).pack(pady=10)

description = """
Memory Hierarchy Levels:

Registers → Cache → RAM → Secondary Storage

As we move down:
✔ Capacity Increases
✔ Cost per bit Decreases
✘ Access Speed Decreases
"""

tk.Label(root, text=description, justify="left").pack(pady=20)

tk.Button(root, text="Visualize Memory Hierarchy", command=show_visualization).pack(pady=20)

root.mainloop()
