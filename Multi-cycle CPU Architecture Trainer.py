import tkinter as tk
import time

CYCLES = [
    "Fetch Instruction",
    "Decode Instruction",
    "Execute Operation",
    "Memory Access",
    "Write Back"
]

def run_trainer():
    output_box.delete("1.0", tk.END)
    instructions = instruction_box.get("1.0", tk.END).strip().split("\n")

    cycle_delay = delay_var.get()
    total_cycles = 0

    for instr in instructions:
        output_box.insert(tk.END, f"\nInstruction: {instr}\n")
        for cycle in CYCLES:
            output_box.insert(tk.END, f"  → {cycle}\n")
            output_box.update()
            time.sleep(cycle_delay)
            total_cycles += 1

    output_box.insert(tk.END, f"\nTotal Cycles Executed: {total_cycles}")

# GUI Setup
root = tk.Tk()
root.title("Multi-cycle CPU Architecture Trainer")
root.geometry("650x500")

tk.Label(root, text="Enter Instructions (one per line):").pack(pady=5)

instruction_box = tk.Text(root, height=8, width=70)
instruction_box.pack()

delay_var = tk.DoubleVar(value=0.7)
tk.Label(root, text="Cycle Delay (seconds):").pack()
tk.Entry(root, textvariable=delay_var).pack()

tk.Button(root, text="Run Multi-cycle Execution", command=run_trainer).pack(pady=10)

tk.Label(root, text="Execution Cycles:").pack()
output_box = tk.Text(root, height=18, width=70)
output_box.pack()

root.mainloop()
