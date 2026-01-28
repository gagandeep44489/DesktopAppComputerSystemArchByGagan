# Instruction Reorder Buffer (ROB) Visualizer
# Python Desktop App using Tkinter

import tkinter as tk
from tkinter import ttk

class ROBVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Instruction Reorder Buffer Visualizer")
        self.root.geometry("900x500")

        self.rob = []  # ROB entries
        self.max_size = 8

        self.create_ui()

    def create_ui(self):
        title = tk.Label(self.root, text="Instruction Reorder Buffer (ROB) Simulator", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        tk.Label(controls, text="Instruction:").grid(row=0, column=0, padx=5)
        self.instr_entry = tk.Entry(controls, width=40)
        self.instr_entry.grid(row=0, column=1, padx=5)

        tk.Button(controls, text="Issue", command=self.issue_instruction).grid(row=0, column=2, padx=5)
        tk.Button(controls, text="Execute", command=self.execute_instruction).grid(row=0, column=3, padx=5)
        tk.Button(controls, text="Commit", command=self.commit_instruction).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Instruction", "State"), show="headings")
        self.tree.heading("ID", text="ROB ID")
        self.tree.heading("Instruction", text="Instruction")
        self.tree.heading("State", text="State")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

        info = tk.Label(self.root, text="States: Issued → Executed → Committed", fg="gray")
        info.pack(pady=5)

    def issue_instruction(self):
        if len(self.rob) >= self.max_size:
            return
        instr = self.instr_entry.get()
        if instr:
            entry = {"id": len(self.rob), "instr": instr, "state": "Issued"}
            self.rob.append(entry)
            self.refresh()
            self.instr_entry.delete(0, tk.END)

    def execute_instruction(self):
        for entry in self.rob:
            if entry["state"] == "Issued":
                entry["state"] = "Executed"
                break
        self.refresh()

    def commit_instruction(self):
        if self.rob and self.rob[0]["state"] == "Executed":
            self.rob.pop(0)
            for i, entry in enumerate(self.rob):
                entry["id"] = i
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.rob:
            self.tree.insert("", tk.END, values=(entry["id"], entry["instr"], entry["state"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = ROBVisualizer(root)
    root.mainloop()