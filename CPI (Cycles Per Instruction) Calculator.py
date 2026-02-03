import tkinter as tk
from tkinter import messagebox

def calculate_cpi():
    try:
        instr_counts_text = entry_instr.get().strip()
        cycles_text = entry_cycles.get().strip()

        instr_counts = [int(x) for x in instr_counts_text.split(',')]
        cycles_per_instr = [float(x) for x in cycles_text.split(',')]

        if len(instr_counts) != len(cycles_per_instr):
            messagebox.showerror("Error", "Counts and cycles lists must be of same length")
            return

        total_instructions = sum(instr_counts)
        total_cycles = sum([instr_counts[i] * cycles_per_instr[i] for i in range(len(instr_counts))])

        avg_cpi = total_cycles / total_instructions

        result_label.config(text=f"Average CPI: {avg_cpi:.2f}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("CPI (Cycles Per Instruction) Calculator")
root.geometry("500x300")

tk.Label(root, text="Enter instruction counts (comma-separated)").pack(pady=5)
entry_instr = tk.Entry(root, width=40)
entry_instr.pack(pady=5)

tk.Label(root, text="Enter cycles per instruction (comma-separated)").pack(pady=5)
entry_cycles = tk.Entry(root, width=40)
entry_cycles.pack(pady=5)

tk.Button(root, text="Calculate CPI", command=calculate_cpi, bg="#4CAF50", fg="white").pack(pady=15)

result_label = tk.Label(root, text="Average CPI: ", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
