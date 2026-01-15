# Opcode Frequency Analyzer - Desktop App in Python
# Purpose:
# Analyze frequency of CPU opcodes from an instruction list
# Useful for computer architecture learning, compiler analysis, and performance study

import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

# ---------------- Core Logic ----------------

def analyze_opcodes():
    instructions = text_input.get("1.0", tk.END).strip().upper().split("\n")
    if not instructions or instructions == ['']:
        messagebox.showerror("Error", "Please enter instructions")
        return

    # Extract opcode (first word of instruction line)
    opcodes = []
    for instr in instructions:
        instr = instr.strip()
        if instr:
            opcode = instr.split()[0]
            opcodes.append(opcode)

    freq = Counter(opcodes)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Opcode Frequency Analysis:\n\n")

    for opcode, count in freq.most_common():
        output_box.insert(tk.END, f"{opcode}: {count}\n")

    output_box.insert(tk.END, f"\nTotal Instructions: {sum(freq.values())}")

# ---------------- Main Window ----------------

root = tk.Tk()
root.title("Opcode Frequency Analyzer")
root.geometry("700x500")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

# ---------------- Layout ----------------

frame = ttk.Frame(root, padding=15)
frame.pack(fill=tk.BOTH, expand=True)

header = ttk.Label(frame, text="Opcode Frequency Analyzer", font=("Segoe UI", 14, "bold"))
header.pack(pady=5)

input_label = ttk.Label(frame, text="Enter Instructions (one per line)")
input_label.pack(anchor="w")

text_input = tk.Text(frame, height=10, width=70)
text_input.pack(pady=8)

analyze_btn = ttk.Button(frame, text="Analyze Opcodes", command=analyze_opcodes)
analyze_btn.pack(pady=5)

output_label = ttk.Label(frame, text="Analysis Output")
output_label.pack(anchor="w", pady=5)

output_box = tk.Text(frame, height=10, width=70)
output_box.pack()

root.mainloop()
