import tkinter as tk
from tkinter import ttk

class SuperscalarSimulator:
    def __init__(self, width=2):
        self.width = width
        self.pipeline = {'IF': [], 'ID': [], 'EX': [], 'MEM': [], 'WB': []}
        self.instructions = []
        self.cycle = 0

    def load_instructions(self, instr_list):
        self.instructions = instr_list

    def step(self):
        """Simulate one cycle"""
        self.cycle += 1
        # Move instructions through pipeline stages
        self.pipeline['WB'] = self.pipeline['MEM']
        self.pipeline['MEM'] = self.pipeline['EX']
        self.pipeline['EX'] = self.pipeline['ID']
        # Fetch new instructions
        fetch_count = min(self.width, len(self.instructions))
        self.pipeline['ID'] = self.instructions[:fetch_count]
        self.instructions = self.instructions[fetch_count:]
        print(f"Cycle {self.cycle}: {self.pipeline}")

class SimulatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Superscalar Architecture Simulator")
        self.geometry("600x400")
        self.sim = SuperscalarSimulator(width=2)
        
        self.instr_entry = tk.Entry(self, width=50)
        self.instr_entry.pack(pady=10)
        
        self.add_btn = tk.Button(self, text="Add Instruction", command=self.add_instruction)
        self.add_btn.pack(pady=5)
        
        self.start_btn = tk.Button(self, text="Start Simulation", command=self.start_sim)
        self.start_btn.pack(pady=5)
        
        self.output = tk.Text(self, height=15, width=70)
        self.output.pack(pady=10)

    def add_instruction(self):
        instr = self.instr_entry.get()
        if instr:
            self.sim.instructions.append(instr)
            self.output.insert(tk.END, f"Added: {instr}\n")
            self.instr_entry.delete(0, tk.END)

    def start_sim(self):
        while self.sim.instructions or any(self.sim.pipeline.values()):
            self.sim.step()
            self.output.insert(tk.END, f"Cycle {self.sim.cycle}: {self.sim.pipeline}\n")
            self.output.see(tk.END)
            self.update_idletasks()

if __name__ == "__main__":
    app = SimulatorGUI()
    app.mainloop()
