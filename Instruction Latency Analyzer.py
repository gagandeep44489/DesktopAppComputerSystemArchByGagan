# Instruction Latency Analyzer - Desktop App in Python
# Purpose:
# Analyze instruction execution latency based on predefined CPU instruction cycles
# Useful for computer architecture, performance analysis, and education

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Instruction Latency Data ----------------
# Example latency values in CPU cycles (simplified model)
INSTRUCTION_LATENCY = {
    "ADD": 1,
    "SUB": 1,
    "MUL": 3,
    "DIV": 5,
    "LOAD": 4,
    "STORE": 4,
    "AND": 1,
    "OR": 1,
    "XOR": 1,
    "JUMP": 2
}

# ---------------- Core Logic ----------------

def analyze_latency():
    instructions = text_input.get("1.0", tk.END).strip().upper().split("\n")
    if not instructions or instructions == ['']:
        messagebox.showerror("Error", "Please enter instructions")
        return

    output_box.delete("1.0", tk.END)
    total_latency = 0

    for instr in instructions:
        instr = instr.strip()
        if instr in INSTRUCTION_LATENCY:
            latency = INSTRUCTION_LATENCY[instr]
            output_box.insert(tk.END, f"{instr}: {latency} cycles\n")
            total_latency += latency
        else:
            output_box.insert(tk.END, f"{instr}: Unknown instruction\n")

    output_box.insert(tk.END, f"\nTotal Latency: {total_latency} cycles")

# ---------------- Main Window ----------------

root = tk.Tk()
root.title("Instruction Latency Analyzer")
root.geometry("700x500")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

# ---------------- Layout ----------------

frame = ttk.Frame(root, padding=15)
frame.pack(fill=tk.BOTH, expand=True)

header = ttk.Label(frame, text="Instruction Latency Analyzer", font=("Segoe UI", 14, "bold"))
header.pack(pady=5)

input_label = ttk.Label(frame, text="Enter CPU Instructions (one per line)")
input_label.pack(anchor="w")

text_input = tk.Text(frame, height=10, width=70)
text_input.pack(pady=8)

analyze_btn = ttk.Button(frame, text="Analyze Latency", command=analyze_latency)
analyze_btn.pack(pady=5)

output_label = ttk.Label(frame, text="Latency Analysis Output")
output_label.pack(anchor="w", pady=5)

output_box = tk.Text(frame, height=10, width=70)
output_box.pack()

root.mainloop()
