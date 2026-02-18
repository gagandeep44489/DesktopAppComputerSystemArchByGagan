import tkinter as tk
from tkinter import ttk, messagebox


class AllocationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("First-Fit / Best-Fit / Worst-Fit Allocation Simulator")
        self.root.geometry("750x600")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Memory Allocation Simulator",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Memory Blocks Input
        tk.Label(self.root, text="Enter Memory Block Sizes (comma separated):").pack()
        self.block_entry = tk.Entry(self.root, width=70)
        self.block_entry.pack(pady=5)

        # Process Sizes Input
        tk.Label(self.root, text="Enter Process Sizes (comma separated):").pack()
        self.process_entry = tk.Entry(self.root, width=70)
        self.process_entry.pack(pady=5)

        # Algorithm Selection
        tk.Label(self.root, text="Select Allocation Algorithm:").pack(pady=5)

        self.algorithm = ttk.Combobox(
            self.root,
            state="readonly",
            values=["First Fit", "Best Fit", "Worst Fit"]
        )
        self.algorithm.current(0)
        self.algorithm.pack(pady=5)

        # Allocate Button
        allocate_btn = tk.Button(self.root, text="Run Allocation",
                                 command=self.run_allocation)
        allocate_btn.pack(pady=10)

        # Results Display
        self.result_text = tk.Text(self.root, width=90, height=20)
        self.result_text.pack(pady=10)

    def parse_input(self, input_text):
        try:
            return [int(x.strip()) for x in input_text.split(",")]
        except:
            return None

    # ---------------- Allocation Algorithms ---------------- #

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

    # -------------------------------------------------------- #

    def run_allocation(self):
        self.result_text.delete("1.0", tk.END)

        blocks = self.parse_input(self.block_entry.get())
        processes = self.parse_input(self.process_entry.get())

        if blocks is None or processes is None:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid comma-separated integers.")
            return

        original_blocks = blocks.copy()
        selected_algo = self.algorithm.get()

        if selected_algo == "First Fit":
            allocation = self.first_fit(blocks, processes)
        elif selected_algo == "Best Fit":
            allocation = self.best_fit(blocks, processes)
        else:
            allocation = self.worst_fit(blocks, processes)

        self.display_results(processes, allocation, original_blocks, blocks)

    def display_results(self, processes, allocation, original_blocks, remaining_blocks):
        self.result_text.insert(tk.END, "ALLOCATION RESULTS\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n\n")

        for i in range(len(processes)):
            if allocation[i] != -1:
                self.result_text.insert(
                    tk.END,
                    f"Process {i + 1} (Size {processes[i]}) "
                    f"-> Allocated to Block {allocation[i] + 1}\n"
                )
            else:
                self.result_text.insert(
                    tk.END,
                    f"Process {i + 1} (Size {processes[i]}) "
                    f"-> Not Allocated\n"
                )

        self.result_text.insert(tk.END, "\nRemaining Memory in Blocks:\n")

        for i in range(len(remaining_blocks)):
            self.result_text.insert(
                tk.END,
                f"Block {i + 1}: {remaining_blocks[i]} remaining "
                f"(Original: {original_blocks[i]})\n"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AllocationSimulator(root)
    root.mainloop()
