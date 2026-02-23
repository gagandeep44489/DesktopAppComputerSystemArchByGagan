import tkinter as tk
from tkinter import messagebox, ttk

class SegmentationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentation Simulator")
        self.root.geometry("600x500")

        self.segments = {}

        # Segment Input Frame
        frame1 = tk.LabelFrame(root, text="Add Segment", padx=10, pady=10)
        frame1.pack(padx=10, pady=10, fill="x")

        tk.Label(frame1, text="Segment Name").grid(row=0, column=0)
        tk.Label(frame1, text="Base Address").grid(row=1, column=0)
        tk.Label(frame1, text="Limit").grid(row=2, column=0)

        self.name_entry = tk.Entry(frame1)
        self.base_entry = tk.Entry(frame1)
        self.limit_entry = tk.Entry(frame1)

        self.name_entry.grid(row=0, column=1)
        self.base_entry.grid(row=1, column=1)
        self.limit_entry.grid(row=2, column=1)

        tk.Button(frame1, text="Add Segment", command=self.add_segment).grid(row=3, columnspan=2, pady=5)

        # Translation Frame
        frame2 = tk.LabelFrame(root, text="Address Translation", padx=10, pady=10)
        frame2.pack(padx=10, pady=10, fill="x")

        tk.Label(frame2, text="Segment Name").grid(row=0, column=0)
        tk.Label(frame2, text="Offset").grid(row=1, column=0)

        self.trans_segment = tk.Entry(frame2)
        self.offset_entry = tk.Entry(frame2)

        self.trans_segment.grid(row=0, column=1)
        self.offset_entry.grid(row=1, column=1)

        tk.Button(frame2, text="Translate", command=self.translate).grid(row=2, columnspan=2, pady=5)

        # Table
        self.tree = ttk.Treeview(root, columns=("Base", "Limit"), show="headings")
        self.tree.heading("Base", text="Base Address")
        self.tree.heading("Limit", text="Limit")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def add_segment(self):
        name = self.name_entry.get()
        try:
            base = int(self.base_entry.get())
            limit = int(self.limit_entry.get())
            self.segments[name] = (base, limit)
            self.tree.insert("", "end", values=(base, limit))
            messagebox.showinfo("Success", f"Segment '{name}' added.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values.")

    def translate(self):
        name = self.trans_segment.get()
        try:
            offset = int(self.offset_entry.get())
            if name in self.segments:
                base, limit = self.segments[name]
                if offset < limit:
                    physical = base + offset
                    messagebox.showinfo("Physical Address", f"Physical Address = {physical}")
                else:
                    messagebox.showerror("Segmentation Fault", "Offset exceeds limit!")
            else:
                messagebox.showerror("Error", "Segment not found.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid offset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentationSimulator(root)
    root.mainloop()