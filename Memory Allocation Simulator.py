import tkinter as tk
from tkinter import messagebox, ttk


class MemoryAllocationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Allocation Simulator")
        self.root.geometry("700x550")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Memory Allocation Simulator",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Memory Blocks Input
        tk.Label(self.root, text="Enter Memory Block Sizes (comma separated):").pack()
        self.block_entry = tk.Entry(self.root, width=60)
        self.block_entry.pack(pady=5)

        # Process Sizes Input
        tk.Label(self.root, text="Enter Process Sizes (comma separated):").pack()
        self.process_entry = tk.Entry(self.root, width=60)
        self.process_entry.pack(pady=5)

        # Allocation Strategy
        tk.Label(self.root, text="Select Allocation Strategy:").pack(pady=5)

        self.strategy = ttk.Combobox(self.root, state="readonly",
                                     values=["First Fit", "Best Fit", "Worst Fit"])
        self.strategy.current(0)
        self.strategy.pack(pady=5)

        # Allocate Button
        allocate_btn = tk.Button(self.root, text="Allocate Memory",
                                 command=self.allocate_memory)
        allocate_btn.pack(pady=10)

        # Results Area
        self.result_text = tk.Text(self.root, height=15, width=80)
        self.result_text.pack(pady=10)

    def parse_input(self, input_text):
        try:
            return [int(x.strip()) for x in input_text.split(",")]
        except:
            return None

    def first_fit(self, blocks, processes):
        allocation = [-1] * len(processes)

        for i in range(len(processes)):
            for j in range(len(blocks)):
                if blocks[j] >= processes[i]:
                    allocation[i] = j
                    blocks[j] -= processes[i]
                    break
        return allocation

    def best_fit(self, blocks, processes):
        allocation = [-1] * len(processes)

        for i in range(len(processes)):
            best_index = -1
            for j in range(len(blocks)):
                if blocks[j] >= processes[i]:
                    if best_index == -1 or blocks[j] < blocks[best_index]:
                        best_index = j
            if best_index != -1:
                allocation[i] = best_index
                blocks[best_index] -= processes[i]
        return allocation

    def worst_fit(self, blocks, processes):
        allocation = [-1] * len(processes)

        for i in range(len(processes)):
            worst_index = -1
            for j in range(len(blocks)):
                if blocks[j] >= processes[i]:
                    if worst_index == -1 or blocks[j] > blocks[worst_index]:
                        worst_index = j
            if worst_index != -1:
                allocation[i] = worst_index
                blocks[worst_index] -= processes[i]
        return allocation

    def allocate_memory(self):
        self.result_text.delete("1.0", tk.END)

        blocks = self.parse_input(self.block_entry.get())
        processes = self.parse_input(self.process_entry.get())

        if blocks is None or processes is None:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid comma-separated numbers.")
            return

        strategy = self.strategy.get()

        blocks_copy = blocks.copy()

        if strategy == "First Fit":
            allocation = self.first_fit(blocks_copy, processes)
        elif strategy == "Best Fit":
            allocation = self.best_fit(blocks_copy, processes)
        else:
            allocation = self.worst_fit(blocks_copy, processes)

        self.display_results(processes, allocation)

    def display_results(self, processes, allocation):
        self.result_text.insert(tk.END, "Allocation Results:\n\n")

        for i in range(len(processes)):
            if allocation[i] != -1:
                self.result_text.insert(
                    tk.END,
                    f"Process {i + 1} (Size {processes[i]}) "
                    f"-> Block {allocation[i] + 1}\n"
                )
            else:
                self.result_text.insert(
                    tk.END,
                    f"Process {i + 1} (Size {processes[i]}) "
                    f"-> Not Allocated\n"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocationSimulator(root)
    root.mainloop()
