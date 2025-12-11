import tkinter as tk
from tkinter import ttk, messagebox

class MicroinstructionDebugger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Microinstruction Debugger")
        self.geometry("1000x600")

        # CPU state
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.registers["ACC"] = 0
        self.PC = 0
        self.flags = {"Z":0, "C":0, "N":0, "V":0}
        self.memory = [0]*256
        self.instructions = []
        
        # History
        self.history = []

        self._build_ui()

    def _build_ui(self):
        # Top: instruction input
        top_frame = ttk.LabelFrame(self, text="Microinstructions", padding=6)
        top_frame.pack(fill='x', padx=6, pady=4)

        self.text_instructions = tk.Text(top_frame, height=10)
        self.text_instructions.pack(fill='x', expand=True)

        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(fill='x', pady=4)
        ttk.Button(btn_frame, text="Load Instructions", command=self.load_instructions).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Step", command=self.step_instruction).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Reset CPU", command=self.reset_cpu).pack(side='left', padx=4)

        # Middle: registers
        reg_frame = ttk.LabelFrame(self, text="Registers & Flags", padding=6)
        reg_frame.pack(fill='x', padx=6, pady=4)

        self.reg_vars = {}
        col = 0
        for reg in self.registers:
            ttk.Label(reg_frame, text=reg).grid(row=0, column=col, padx=4)
            var = tk.StringVar(value=str(self.registers[reg]))
            self.reg_vars[reg] = var
            ttk.Entry(reg_frame, textvariable=var, width=8, state='readonly').grid(row=1, column=col, padx=4)
            col +=1

        # Flags
        ttk.Label(reg_frame, text="Flags").grid(row=0, column=col, padx=4)
        self.flag_vars = {}
        for i, f in enumerate(self.flags):
            var = tk.StringVar(value=str(self.flags[f]))
            self.flag_vars[f] = var
            ttk.Entry(reg_frame, textvariable=var, width=4, state='readonly').grid(row=1, column=col+i, padx=2)
        col += len(self.flags)

        # Memory display
        mem_frame = ttk.LabelFrame(self, text="Memory (first 32 cells)", padding=6)
        mem_frame.pack(fill='x', padx=6, pady=4)

        self.mem_vars = []
        for i in range(32):
            var = tk.StringVar(value=str(self.memory[i]))
            self.mem_vars.append(var)
            ttk.Label(mem_frame, text=f"M[{i}]").grid(row=0, column=i, padx=2)
            ttk.Entry(mem_frame, textvariable=var, width=4, state='readonly').grid(row=1, column=i, padx=2)

        # History
        hist_frame = ttk.LabelFrame(self, text="Instruction History", padding=6)
        hist_frame.pack(fill='both', expand=True, padx=6, pady=4)
        self.hist_listbox = tk.Listbox(hist_frame)
        self.hist_listbox.pack(fill='both', expand=True)

    def load_instructions(self):
        self.instructions = [line.strip() for line in self.text_instructions.get("1.0", "end").splitlines() if line.strip()]
        self.PC = 0
        self.hist_listbox.delete(0, 'end')
        messagebox.showinfo("Info", f"Loaded {len(self.instructions)} instructions.")

    def step_instruction(self):
        if self.PC >= len(self.instructions):
            messagebox.showinfo("Info", "All instructions executed.")
            return
        instr = self.instructions[self.PC]
        self.execute(instr)
        self.PC +=1

    def execute(self, instr):
        try:
            parts = instr.replace(',','').split()
            op = parts[0].upper()
            if op == "LOAD":
                reg = parts[1].upper()
                if parts[2].startswith("M["):
                    addr = int(parts[2][2:-1])
                    self.registers[reg] = self.memory[addr]
                else:
                    self.registers[reg] = int(parts[2])
            elif op == "STORE":
                reg = parts[1].upper()
                addr = int(parts[2][2:-1])
                self.memory[addr] = self.registers[reg]
            elif op == "ADD":
                r1 = parts[1].upper()
                r2 = parts[2].upper()
                res = self.registers[r1] + self.registers[r2]
                self.registers["ACC"] = res & 0xFFFF
                self.update_flags(res)
            elif op == "SUB":
                r1 = parts[1].upper()
                r2 = parts[2].upper()
                res = self.registers[r1] - self.registers[r2]
                self.registers["ACC"] = res & 0xFFFF
                self.update_flags(res)
            elif op == "AND":
                r1 = parts[1].upper()
                r2 = parts[2].upper()
                res = self.registers[r1] & self.registers[r2]
                self.registers["ACC"] = res
                self.update_flags(res)
            elif op == "OR":
                r1 = parts[1].upper()
                r2 = parts[2].upper()
                res = self.registers[r1] | self.registers[r2]
                self.registers["ACC"] = res
                self.update_flags(res)
            elif op == "NOT":
                r1 = parts[1].upper()
                res = ~self.registers[r1] & 0xFFFF
                self.registers["ACC"] = res
                self.update_flags(res)
            else:
                messagebox.showwarning("Warning", f"Unsupported instruction: {instr}")
                return

            # Update GUI
            for reg in self.registers:
                self.reg_vars[reg].set(str(self.registers[reg]))
            for i in range(32):
                self.mem_vars[i].set(str(self.memory[i]))
            for f in self.flags:
                self.flag_vars[f].set(str(self.flags[f]))

            # Add to history
            self.history.append(instr)
            self.hist_listbox.insert('end', f"PC={self.PC}: {instr}")
            self.hist_listbox.see('end')
        except Exception as e:
            messagebox.showerror("Error", f"Error executing instruction '{instr}': {e}")

    def update_flags(self, value):
        self.flags["Z"] = 1 if value == 0 else 0
        self.flags["N"] = 1 if (value & 0x8000) !=0 else 0
        self.flags["C"] = 1 if value > 0xFFFF else 0
        self.flags["V"] = 1 if value > 0x7FFF or value < -0x8000 else 0

    def reset_cpu(self):
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.registers["ACC"] = 0
        self.PC = 0
        self.flags = {"Z":0, "C":0, "N":0, "V":0}
        self.memory = [0]*256
        self.instructions = []
        self.text_instructions.delete("1.0","end")
        self.hist_listbox.delete(0,'end')
        for reg in self.reg_vars:
            self.reg_vars[reg].set(str(self.registers[reg]))
        for f in self.flag_vars:
            self.flag_vars[f].set(str(self.flags[f]))
        for i in range(32):
            self.mem_vars[i].set(str(self.memory[i]))

if __name__ == "__main__":
    app = MicroinstructionDebugger()
    app.mainloop()
