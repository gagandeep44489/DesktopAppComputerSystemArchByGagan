import tkinter as tk
from tkinter import ttk, messagebox

class PageFaultExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Fault Explorer")
        self.root.geometry("750x600")

        tk.Label(root, text="Page Fault Explorer",
                 font=("Arial", 18, "bold")).pack(pady=10)

        # Inputs
        tk.Label(root, text="Page Reference String (comma separated):").pack()
        self.ref_entry = tk.Entry(root, width=60)
        self.ref_entry.pack()

        tk.Label(root, text="Number of Frames:").pack()
        self.frame_entry = tk.Entry(root, width=20)
        self.frame_entry.pack()

        tk.Label(root, text="Select Algorithm:").pack()
        self.algorithm = ttk.Combobox(root, values=["FIFO", "LRU", "Optimal"])
        self.algorithm.pack()

        tk.Button(root, text="Run Simulation",
                  command=self.run_simulation).pack(pady=10)

        self.output = tk.Text(root, height=20, width=90)
        self.output.pack(pady=10)

    # FIFO Algorithm
    def fifo(self, pages, frames):
        memory = []
        faults = 0
        pointer = 0

        for page in pages:
            if page not in memory:
                faults += 1
                if len(memory) < frames:
                    memory.append(page)
                else:
                    memory[pointer] = page
                    pointer = (pointer + 1) % frames
            self.output.insert(tk.END, f"{page} -> {memory}\n")
        return faults

    # LRU Algorithm
    def lru(self, pages, frames):
        memory = []
        faults = 0

        for page in pages:
            if page not in memory:
                faults += 1
                if len(memory) < frames:
                    memory.append(page)
                else:
                    memory.pop(0)
                    memory.append(page)
            else:
                memory.remove(page)
                memory.append(page)
            self.output.insert(tk.END, f"{page} -> {memory}\n")
        return faults

    # Optimal Algorithm
    def optimal(self, pages, frames):
        memory = []
        faults = 0

        for i in range(len(pages)):
            page = pages[i]
            if page not in memory:
                faults += 1
                if len(memory) < frames:
                    memory.append(page)
                else:
                    future = pages[i+1:]
                    indices = []
                    for m in memory:
                        if m in future:
                            indices.append(future.index(m))
                        else:
                            indices.append(float('inf'))
                    memory[indices.index(max(indices))] = page
            self.output.insert(tk.END, f"{page} -> {memory}\n")
        return faults

    def run_simulation(self):
        try:
            pages = list(map(int, self.ref_entry.get().split(",")))
            frames = int(self.frame_entry.get())
            algo = self.algorithm.get()

            self.output.delete(1.0, tk.END)

            if algo == "FIFO":
                faults = self.fifo(pages, frames)
            elif algo == "LRU":
                faults = self.lru(pages, frames)
            elif algo == "Optimal":
                faults = self.optimal(pages, frames)
            else:
                messagebox.showerror("Error", "Select Algorithm")
                return

            self.output.insert(tk.END, f"\nTotal Page Faults: {faults}")

        except:
            messagebox.showerror("Error", "Invalid Input")

if __name__ == "__main__":
    root = tk.Tk()
    app = PageFaultExplorer(root)
    root.mainloop()