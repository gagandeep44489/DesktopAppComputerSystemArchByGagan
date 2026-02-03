import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Define pipeline stages
stages = ['IF', 'ID', 'EX', 'MEM', 'WB']

def parse_instructions(text):
    lines = text.strip().split('\n')
    instructions = [line.strip() for line in lines if line.strip()]
    return instructions

def detect_data_hazards(instr_list):
    hazards = []
    reg_write = {}
    for i, instr in enumerate(instr_list):
        parts = instr.split()
        op = parts[0]
        dest = parts[1] if len(parts) > 1 else None
        src = parts[2:] if len(parts) > 2 else []

        # Check RAW hazard
        for s in src:
            if s in reg_write and reg_write[s] >= i:
                hazards.append(f"Data Hazard (RAW) at instruction {i+1}: {instr}")
        if dest:
            reg_write[dest] = i + 2  # assume write occurs at EX stage

    return hazards

def simulate_pipeline():
    instr_text = entry_instructions.get("1.0", tk.END)
    instructions = parse_instructions(instr_text)
    if not instructions:
        messagebox.showerror("Error", "Enter instructions")
        return

    hazards = detect_data_hazards(instructions)

    # Create simple pipeline table
    table = pd.DataFrame(index=instructions, columns=stages)
    for idx, instr in enumerate(instructions):
        for j, stage in enumerate(stages):
            if j + idx < len(stages) + len(instructions):
                table.at[instr, stage] = f"{stage}"

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Pipeline Table:\n")
    result_text.insert(tk.END, table.to_string())
    result_text.insert(tk.END, "\n\nDetected Hazards:\n")
    if hazards:
        for h in hazards:
            result_text.insert(tk.END, h + "\n")
    else:
        result_text.insert(tk.END, "No hazards detected.\n")

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("CPU Hazard Detection Simulator")
root.geometry("700x500")

tk.Label(root, text="Enter Instructions (one per line, e.g., ADD R1 R2 R3)").pack(pady=5)
entry_instructions = tk.Text(root, height=10, width=80)
entry_instructions.pack(pady=5)

tk.Button(root, text="Simulate Pipeline", command=simulate_pipeline, bg="#4CAF50", fg="white").pack(pady=10)

result_text = tk.Text(root, height=15, width=80)
result_text.pack(pady=5)

root.mainloop()
