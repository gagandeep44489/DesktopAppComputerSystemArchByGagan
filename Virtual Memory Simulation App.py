import tkinter as tk
from tkinter import messagebox

def fifo_simulation(pages, frames_count):
    frames = []
    page_faults = 0
    result = []

    for page in pages:
        if page not in frames:
            page_faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
        result.append(frames.copy())

    return result, page_faults


def lru_simulation(pages, frames_count):
    frames = []
    page_faults = 0
    recent = []
    result = []

    for page in pages:
        if page not in frames:
            page_faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                lru_page = recent.pop(0)
                frames.remove(lru_page)
                frames.append(page)
        else:
            recent.remove(page)

        recent.append(page)
        result.append(frames.copy())

    return result, page_faults


def simulate():
    pages_input = entry_pages.get().strip()
    frames_input = entry_frames.get().strip()

    if not pages_input or not frames_input:
        messagebox.showerror("Input Error", "Please enter pages and frame count.")
        return

    pages = pages_input.split(",")
    frames_count = int(frames_input)

    algorithm = algo_var.get()

    if algorithm == "FIFO":
        result, faults = fifo_simulation(pages, frames_count)
    else:
        result, faults = lru_simulation(pages, frames_count)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Algorithm: {algorithm}\n")
    output_text.insert(tk.END, f"Frames: {frames_count}\n\n")

    for i, state in enumerate(result):
        output_text.insert(tk.END, f"Step {i+1}: {state}\n")

    output_text.insert(tk.END, f"\nTotal Page Faults: {faults}\n")


# GUI Setup
root = tk.Tk()
root.title("Virtual Memory Simulation App")
root.geometry("700x500")

title_label = tk.Label(root, text="Virtual Memory Simulation", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

tk.Label(root, text="Enter Page Reference String (comma-separated):").pack()
entry_pages = tk.Entry(root, width=60)
entry_pages.pack(pady=5)

tk.Label(root, text="Enter Number of Frames:").pack()
entry_frames = tk.Entry(root, width=10)
entry_frames.pack(pady=5)

algo_var = tk.StringVar(value="FIFO")
tk.Radiobutton(root, text="FIFO", variable=algo_var, value="FIFO").pack()
tk.Radiobutton(root, text="LRU", variable=algo_var, value="LRU").pack()

simulate_button = tk.Button(root, text="Simulate", command=simulate)
simulate_button.pack(pady=10)

output_text = tk.Text(root, height=15, width=80)
output_text.pack(pady=10)

root.mainloop()
