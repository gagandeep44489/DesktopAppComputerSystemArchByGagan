import tkinter as tk
from tkinter import messagebox

INSTRUCTION_LATENCY = {
    "ALU": 1,
    "LOAD": 2,
    "STORE": 2,
    "BRANCH": 2
}

class CPUCycleAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Cycle Counter Analyzer")

        tk.Label(root, text="Instruction Sequence (space-separated):").pack()
        self.seq_entry = tk.Entry(root, width=50)
        self.seq_entry.pack(pady=5)

        tk.Label(root, text="Custom Latency (optional, format: INSTR:cycles, comma-separated)").pack()
        self.lat_entry = tk.Entry(root, width=50)
        self.lat_entry.pack(pady=5)

        tk.Button(root, text="Analyze", command=self.analyze).pack(pady=10)

        self.output = tk.Text(root, height=15, width=60)
        self.output.pack()

    def analyze(self):
        seq_text = self.seq_entry.get().upper().split()
        lat_text = self.lat_entry.get()
        latency = INSTRUCTION_LATENCY.copy()

        if lat_text:
            try:
                for item in lat_text.split(","):
                    instr, val = item.split(":")
                    latency[instr.strip().upper()] = int(val.strip())
            except:
                messagebox.showerror("Error", "Invalid custom latency format")
                return

        total_cycles = 0
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Instruction | Latency | Cumulative Cycles\n")
        self.output.insert(tk.END, "-"*40 + "\n")

        for i, instr in enumerate(seq_text, 1):
            if instr not in latency:
                messagebox.showerror("Error", f"Unknown instruction: {instr}")
                return
            cycles = latency[instr]
            total_cycles += cycles
            self.output.insert(tk.END, f"{instr:^11} | {cycles:^7} | {total_cycles:^16}\n")

        cpi = total_cycles / len(seq_text) if seq_text else 0
        self.output.insert(tk.END, f"\nTotal Cycles: {total_cycles}\n")
        self.output.insert(tk.END, f"Average CPI: {cpi:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUCycleAnalyzerApp(root)
    root.mainloop()
