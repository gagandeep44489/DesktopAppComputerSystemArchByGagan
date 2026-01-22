import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Instruction:
    def __init__(self, name, type_, latency):
        self.name = name
        self.type = type_
        self.latency = latency
        self.issue_cycle = 0
        self.execute_cycle = 0
        self.writeback_cycle = 0

class OutOfOrderSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Out-of-Order Execution Simulator")
        self.root.geometry("1000x600")

        self.instructions = []

        # Top Frame - Instruction Entry
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Instruction Name").grid(row=0, column=0)
        tk.Label(top_frame, text="Type (ALU/Load/Store/Branch)").grid(row=0, column=1)
        tk.Label(top_frame, text="Latency (cycles)").grid(row=0, column=2)

        self.entry_name = tk.Entry(top_frame, width=15)
        self.entry_name.grid(row=1, column=0)
        self.entry_type = tk.Entry(top_frame, width=15)
        self.entry_type.grid(row=1, column=1)
        self.entry_latency = tk.Entry(top_frame, width=10)
        self.entry_latency.grid(row=1, column=2)

        tk.Button(top_frame, text="Add Instruction", command=self.add_instruction).grid(row=1, column=3, padx=10)
        tk.Button(top_frame, text="Load from File", command=self.load_file).grid(row=1, column=4, padx=10)
        tk.Button(top_frame, text="Simulate Execution", command=self.simulate).grid(row=1, column=5, padx=10)

        # Middle Frame - Instruction List
        mid_frame = tk.Frame(root)
        mid_frame.pack(pady=10)
        tk.Label(mid_frame, text="Instruction Queue:").pack()
        self.listbox = tk.Listbox(mid_frame, width=80)
        self.listbox.pack()

        # Bottom Frame - Pipeline Visualization
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10)
        tk.Label(bottom_frame, text="Pipeline Visualization (Issue → Execute → Write-back):").pack()
        self.fig, self.ax = plt.subplots(figsize=(8,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=bottom_frame)
        self.canvas.get_tk_widget().pack()

    def add_instruction(self):
        name = self.entry_name.get().strip()
        type_ = self.entry_type.get().strip()
        latency = self.entry_latency.get().strip()

        if not name or not type_ or not latency.isdigit():
            messagebox.showerror("Error", "Enter valid instruction data")
            return

        instr = Instruction(name, type_, int(latency))
        self.instructions.append(instr)
        self.listbox.insert(tk.END, f"{name} | {type_} | {latency} cycles")

        self.entry_name.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_latency.delete(0, tk.END)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        name, type_, latency = parts
                        if latency.isdigit():
                            instr = Instruction(name.strip(), type_.strip(), int(latency))
                            self.instructions.append(instr)
                            self.listbox.insert(tk.END, f"{name} | {type_} | {latency} cycles")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def simulate(self):
        if not self.instructions:
            messagebox.showerror("Error", "No instructions to simulate")
            return

        # Simplified out-of-order simulation:
        # Issue instructions as soon as possible respecting previous instruction's write-back
        current_cycle = 0
        for instr in self.instructions:
            instr.issue_cycle = current_cycle
            instr.execute_cycle = instr.issue_cycle + 1  # execute starts next cycle
            instr.writeback_cycle = instr.execute_cycle + instr.latency
            current_cycle = instr.issue_cycle + 1  # next instruction can issue next cycle

        self.visualize_pipeline()

    def visualize_pipeline(self):
        self.ax.clear()
        for idx, instr in enumerate(self.instructions):
            # Issue stage
            self.ax.broken_barh([(instr.issue_cycle, 1)], (idx*10, 3), facecolors='tab:orange')
            # Execute stage
            self.ax.broken_barh([(instr.execute_cycle, instr.latency)], (idx*10, 3), facecolors='tab:blue')
            # Write-back stage
            self.ax.broken_barh([(instr.writeback_cycle, 1)], (idx*10, 3), facecolors='tab:green')
            self.ax.text(instr.issue_cycle + 0.5, idx*10 + 1.5, instr.name,
                         ha='center', va='center', color='white', fontsize=8)

        self.ax.set_xlabel("Cycle")
        self.ax.set_yticks([i*10 + 1.5 for i in range(len(self.instructions))])
        self.ax.set_yticklabels([instr.name for instr in self.instructions])
        self.ax.set_title("Out-of-Order Execution Timeline")
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = OutOfOrderSimulatorApp(root)
    root.mainloop()
