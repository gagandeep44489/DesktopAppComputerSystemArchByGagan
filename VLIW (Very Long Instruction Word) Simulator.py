import tkinter as tk
from tkinter import ttk, messagebox

# =======================
# VLIW PROCESSOR CORE
# =======================

class VLIWProcessor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.registers = {f"R{i}": 0 for i in range(16)}
        self.memory = [0] * 256
        self.program = []
        self.pc = 0
        self.cycle = 0

    def load_program(self, code_lines):
        self.program = [line.strip() for line in code_lines if line.strip()]
        self.pc = 0
        self.cycle = 0

    def step(self):
        if self.pc >= len(self.program):
            return False

        vliw_word = self.program[self.pc]
        self.execute_vliw(vliw_word)

        self.pc += 1
        self.cycle += 1
        return True

    def execute_vliw(self, word):
        slots = word.split("|")
        for slot in slots:
            self.execute_instruction(slot.strip())

    def execute_instruction(self, instr):
        parts = instr.split()
        if not parts:
            return

        op = parts[0]

        try:
            if op == "ADD":
                rd, r1, r2 = parts[1:]
                self.registers[rd] = self.registers[r1] + self.registers[r2]

            elif op == "SUB":
                rd, r1, r2 = parts[1:]
                self.registers[rd] = self.registers[r1] - self.registers[r2]

            elif op == "MUL":
                rd, r1, r2 = parts[1:]
                self.registers[rd] = self.registers[r1] * self.registers[r2]

            elif op == "LOAD":
                rd, addr = parts[1], parts[2]
                offset, base = addr.replace(")", "").split("(")
                self.registers[rd] = self.memory[self.registers[base] + int(offset)]

            elif op == "STORE":
                rs, addr = parts[1], parts[2]
                offset, base = addr.replace(")", "").split("(")
                self.memory[self.registers[base] + int(offset)] = self.registers[rs]

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))


# =======================
# GUI APPLICATION
# =======================

class VLIWSimulatorApp:
    def __init__(self, root):
        self.cpu = VLIWProcessor()
        self.root = root
        root.title("VLIW Simulator (Single File)")
        root.geometry("850x600")

        self.create_widgets()
        self.refresh_registers()
        self.refresh_status()

    def create_widgets(self):
        # Instruction Editor
        tk.Label(self.root, text="VLIW Program").pack(anchor="w", padx=10)
        self.code_editor = tk.Text(self.root, height=8)
        self.code_editor.pack(fill="x", padx=10)

        self.code_editor.insert(
            "1.0",
            "ADD R1 R2 R3 | MUL R4 R5 R6\n"
            "ADD R7 R1 R4 | LOAD R8 0(R9)\n"
        )

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Load Program", command=self.load_program).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Step", command=self.step).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Run All", command=self.run_all).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset).pack(side="left", padx=5)

        # Register View
        tk.Label(self.root, text="Registers").pack(anchor="w", padx=10)
        self.reg_table = ttk.Treeview(self.root, columns=("Value"), height=10)
        self.reg_table.heading("#0", text="Register")
        self.reg_table.heading("Value", text="Value")
        self.reg_table.pack(fill="x", padx=10)

        # Status Bar
        self.status = tk.Label(self.root, text="", relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom")

    def load_program(self):
        code = self.code_editor.get("1.0", tk.END).splitlines()
        self.cpu.load_program(code)
        self.refresh_status()
        messagebox.showinfo("Program Loaded", "VLIW program loaded successfully.")

    def step(self):
        if not self.cpu.program:
            self.load_program()

        if not self.cpu.step():
            messagebox.showinfo("Finished", "Program execution completed.")
            return

        self.refresh_registers()
        self.refresh_status()

    def run_all(self):
        if not self.cpu.program:
            self.load_program()

        while self.cpu.step():
            pass

        self.refresh_registers()
        self.refresh_status()
        messagebox.showinfo("Finished", "Program execution completed.")

    def reset(self):
        self.cpu.reset()
        self.refresh_registers()
        self.refresh_status()

    def refresh_registers(self):
        self.reg_table.delete(*self.reg_table.get_children())
        for reg, val in sorted(self.cpu.registers.items()):
            self.reg_table.insert("", "end", text=reg, values=(val,))

    def refresh_status(self):
        self.status.config(
            text=f"Cycle: {self.cpu.cycle} | PC: {self.cpu.pc}"
        )


# =======================
# MAIN
# =======================

if __name__ == "__main__":
    root = tk.Tk()
    app = VLIWSimulatorApp(root)
    root.mainloop()
