import tkinter as tk
from tkinter import ttk

class CPUPipelineViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Pipeline Stage Viewer")
        self.root.geometry("800x500")

        # Top frame for input
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Enter Instructions (comma-separated, e.g., ADD, SUB, MUL, DIV)").pack()
        self.instr_entry = tk.Entry(top_frame, width=80)
        self.instr_entry.pack(pady=5)

        tk.Label(top_frame, text="Pipeline Stages (comma-separated, e.g., IF, ID, EX, MEM, WB)").pack()
        self.stage_entry = tk.Entry(top_frame, width=80)
        self.stage_entry.pack(pady=5)

        simulate_btn = tk.Button(top_frame, text="Simulate Pipeline", command=self.simulate_pipeline)
        simulate_btn.pack(pady=10)

        # Treeview frame
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = None

    def simulate_pipeline(self):
        instr_text = self.instr_entry.get().strip()
        stages_text = self.stage_entry.get().strip()

        if not instr_text or not stages_text:
            tk.messagebox.showwarning("Input Error", "Please enter both instructions and stages")
            return

        instructions = [i.strip() for i in instr_text.split(',')]
        stages = [s.strip() for s in stages_text.split(',')]

        # Create pipeline table
        num_cycles = len(instructions) + len(stages) - 1

        table = []
        for i, instr in enumerate(instructions):
            row = [''] * num_cycles
            for j, stage in enumerate(stages):
                if i + j < num_cycles:
                    row[i + j] = stage
            table.append([instr] + row)

        # Clear previous tree
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        columns = ['Instruction'] + [f'C{i+1}' for i in range(num_cycles)]
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=70, anchor='center')

        for row in table:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUPipelineViewer(root)
    root.mainloop()