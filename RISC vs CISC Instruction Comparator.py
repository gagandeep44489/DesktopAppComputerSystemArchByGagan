import tkinter as tk
from tkinter import messagebox, ttk

class RISCvsCISCComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("RISC vs CISC Instruction Comparator")
        self.root.geometry("900x500")

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Instructions for RISC (comma-separated)").pack()
        self.risc_entry = tk.Entry(input_frame, width=80)
        self.risc_entry.pack(pady=5)

        tk.Label(input_frame, text="Enter Instructions for CISC (comma-separated)").pack()
        self.cisc_entry = tk.Entry(input_frame, width=80)
        self.cisc_entry.pack(pady=5)

        compare_btn = tk.Button(input_frame, text="Compare Instructions", command=self.compare_instructions)
        compare_btn.pack(pady=10)

        # Output frame
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = None

    def compare_instructions(self):
        risc_text = self.risc_entry.get().strip()
        cisc_text = self.cisc_entry.get().strip()

        if not risc_text or not cisc_text:
            messagebox.showwarning("Input Error", "Please enter instructions for both RISC and CISC")
            return

        risc_instr = [i.strip() for i in risc_text.split(',')]
        cisc_instr = [i.strip() for i in cisc_text.split(',')]

        max_len = max(len(risc_instr), len(cisc_instr))
        table = []

        for i in range(max_len):
            risc_i = risc_instr[i] if i < len(risc_instr) else ''
            cisc_i = cisc_instr[i] if i < len(cisc_instr) else ''
            table.append([i+1, risc_i, cisc_i])

        # Clear previous tree
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        columns = ['Index', 'RISC Instruction', 'CISC Instruction']
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor='center')

        for row in table:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = RISCvsCISCComparator(root)
    root.mainloop()