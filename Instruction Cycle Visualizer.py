"""
Instruction Cycle Visualizer (Tkinter)
Save as: instruction_cycle_visualizer.py
Run:    python instruction_cycle_visualizer.py
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import copy

# --- Model ---

class Stage:
    FETCH = "FETCH"
    DECODE = "DECODE"
    EXECUTE = "EXECUTE"
    MEMORY = "MEMORY"
    WRITEBACK = "WRITEBACK"
    IDLE = "IDLE"

@dataclass
class Instruction:
    asm: str
    op: str
    rd: int = 0
    rs: int = 0
    imm: int = 0

@dataclass
class CPUState:
    pc: int
    ir: Optional[Instruction]
    stage: str
    regs: List[int]
    memory: List[int]

class SimpleCPU:
    def __init__(self, program: List[Instruction]):
        self.program = program
        self.pc = 0
        self.ir: Optional[Instruction] = None
        self.stage = Stage.IDLE
        self.regs = [0] * 4
        self.memory = [0] * 16
        # history for stepping back (store deep copies of CPUState)
        self.history: List[CPUState] = []

    def snapshot(self) -> CPUState:
        return CPUState(
            pc=self.pc,
            ir=copy.deepcopy(self.ir),
            stage=self.stage,
            regs=copy.deepcopy(self.regs),
            memory=copy.deepcopy(self.memory),
        )

    def push_history(self):
        self.history.append(self.snapshot())

    def pop_history(self) -> bool:
        if not self.history:
            return False
        s = self.history.pop()
        self.pc = s.pc
        self.ir = s.ir
        self.stage = s.stage
        self.regs = s.regs
        self.memory = s.memory
        return True

    def reset(self):
        self.push_history()
        self.pc = 0
        self.ir = None
        self.stage = Stage.IDLE
        self.regs = [0] * 4
        self.memory = [0] * 16

    def step_forward(self):
        # Save state so stepBack can restore
        self.push_history()

        if self.stage in (Stage.IDLE, Stage.WRITEBACK):
            self.begin_fetch()
            return

        if self.stage == Stage.FETCH:
            self.do_decode()
            return

        if self.stage == Stage.DECODE:
            self.do_execute()
            return

        if self.stage == Stage.EXECUTE:
            self.do_memory()
            return

        if self.stage == Stage.MEMORY:
            self.do_writeback()
            return

    def step_back(self):
        return self.pop_history()

    def begin_fetch(self):
        if 0 <= self.pc < len(self.program):
            self.stage = Stage.FETCH
            # IR will be set in decode
        else:
            self.stage = Stage.IDLE
            self.ir = None

    def do_decode(self):
        if self.stage != Stage.FETCH:
            return
        if 0 <= self.pc < len(self.program):
            self.ir = self.program[self.pc]
            self.stage = Stage.DECODE
        else:
            self.ir = None
            self.stage = Stage.IDLE

    def do_execute(self):
        if self.stage != Stage.DECODE:
            return
        # In this simple model, execute doesn't commit changes; writeback does.
        self.stage = Stage.EXECUTE

    def do_memory(self):
        if self.stage != Stage.EXECUTE:
            return
        # For LOAD/STORE we might check addresses here (still waiting to commit)
        self.stage = Stage.MEMORY

    def do_writeback(self):
        if self.stage != Stage.MEMORY:
            return
        ins = self.ir
        if ins is not None:
            if ins.op == "MOVI":
                self.regs[ins.rd] = ins.imm
            elif ins.op == "ADD":
                self.regs[ins.rd] = self.regs[ins.rd] + self.regs[ins.rs]
            elif ins.op == "ADDI":
                self.regs[ins.rd] = self.regs[ins.rd] + ins.imm
            elif ins.op == "LOAD":
                addr = max(0, min(len(self.memory) - 1, ins.imm))
                self.regs[ins.rd] = self.memory[addr]
            elif ins.op == "STORE":
                addr = max(0, min(len(self.memory) - 1, ins.imm))
                self.memory[addr] = self.regs[ins.rs]
            # else: unknown op => no-op
        # advance PC and set writeback stage (so next step goes to fetch)
        self.pc += 1
        self.stage = Stage.WRITEBACK

# --- Sample Program ---
sample_program = [
    Instruction("MOVI R0, #5", "MOVI", rd=0, imm=5),
    Instruction("MOVI R1, #10", "MOVI", rd=1, imm=10),
    Instruction("ADD R0, R1", "ADD", rd=0, rs=1),
    Instruction("STORE R0, 2", "STORE", rs=0, imm=2),
    Instruction("LOAD R2, 2", "LOAD", rd=2, imm=2),
]

# --- UI ---

class VisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instruction Cycle Visualizer")
        self.cpu = SimpleCPU(sample_program)
        self.is_playing = False
        self.play_job = None

        self.build_ui()
        self.update_ui()  # initial render

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        title = ttk.Label(frm, text="Instruction Cycle Visualizer", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

        # Stages
        stages_frm = ttk.Frame(frm)
        stages_frm.grid(row=1, column=0, columnspan=3, sticky="w")
        self.stage_labels: Dict[str, ttk.Label] = {}
        for i, s in enumerate([Stage.FETCH, Stage.DECODE, Stage.EXECUTE, Stage.MEMORY, Stage.WRITEBACK]):
            lbl = ttk.Label(stages_frm, text=s, relief="ridge", padding=(10,6))
            lbl.grid(row=0, column=i, padx=4)
            self.stage_labels[s] = lbl

        # Info panel (PC, IR, Program)
        info = ttk.Frame(frm, relief="groove", padding=8)
        info.grid(row=2, column=0, sticky="nsew", padx=(0,8), pady=8)
        info.columnconfigure(0, weight=1)
        self.pc_var = tk.StringVar()
        self.ir_var = tk.StringVar()
        self.stage_var = tk.StringVar()
        ttk.Label(info, text="PC:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(info, textvariable=self.pc_var).grid(row=0, column=1, sticky="w")
        ttk.Label(info, text="IR:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
        ttk.Label(info, textvariable=self.ir_var).grid(row=1, column=1, sticky="w")
        ttk.Label(info, text="Stage:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        ttk.Label(info, textvariable=self.stage_var).grid(row=2, column=1, sticky="w")

        ttk.Separator(info, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=6)
        ttk.Label(info, text="Program:").grid(row=4, column=0, columnspan=2, sticky="w")
        self.program_text = tk.Text(info, height=6, width=36, padx=4, pady=4)
        self.program_text.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.program_text.configure(state="disabled")

        # Controls
        ctrls = ttk.Frame(frm)
        ctrls.grid(row=3, column=0, sticky="w", pady=(0,8))
        ttk.Button(ctrls, text="Step Back", command=self.on_step_back).grid(row=0, column=0, padx=4)
        ttk.Button(ctrls, text="Step", command=self.on_step).grid(row=0, column=1, padx=4)
        ttk.Button(ctrls, text="Reset", command=self.on_reset).grid(row=0, column=2, padx=4)
        self.play_button = ttk.Button(ctrls, text="Play", command=self.on_play_pause)
        self.play_button.grid(row=0, column=3, padx=4)

        ttk.Label(ctrls, text="Speed (ms/stage):").grid(row=0, column=4, padx=(12,4))
        self.speed_var = tk.IntVar(value=700)
        self.speed_scale = ttk.Scale(ctrls, from_=100, to=1500, orient="horizontal", variable=self.speed_var)
        self.speed_scale.grid(row=0, column=5, padx=4)

        # Right side: registers and memory
        right = ttk.Frame(frm)
        right.grid(row=2, column=1, rowspan=2, sticky="nsew")
        right.columnconfigure(0, weight=1)
        reg_frame = ttk.LabelFrame(right, text="Registers (R0..R3)")
        reg_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=2)
        self.reg_labels: List[ttk.Label] = []
        for i in range(4):
            l = ttk.Label(reg_frame, text=f"R{i}: 0", padding=(6,4))
            l.grid(row=0, column=i, padx=4)
            self.reg_labels.append(l)

        mem_frame = ttk.LabelFrame(right, text="Memory (addr : val)")
        mem_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.mem_text = tk.Text(mem_frame, width=20, height=10)
        self.mem_text.pack(padx=4, pady=4)
        self.mem_text.configure(state="disabled")

        # Notes
        notes = ttk.Label(frm, text="Notes: This is a single-instruction staged simulator for teaching purposes.",
                          foreground="gray")
        notes.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6,0))

        # Fill program area
        self.refresh_program_text()

    def refresh_program_text(self):
        self.program_text.configure(state="normal")
        self.program_text.delete("1.0", tk.END)
        for idx, ins in enumerate(self.cpu.program):
            marker = "=> " if idx == self.cpu.pc else "   "
            self.program_text.insert(tk.END, f"{marker}{ins.asm}\n")
        self.program_text.configure(state="disabled")

    def update_ui(self):
        # update PC, IR, stage
        self.pc_var.set(str(self.cpu.pc))
        self.ir_var.set(self.cpu.ir.asm if self.cpu.ir else "----")
        self.stage_var.set(self.cpu.stage)

        # update stage label colors
        for s, lbl in self.stage_labels.items():
            if self.cpu.stage == s:
                lbl.config(background="#b3e5fc")
            else:
                lbl.config(background=self.root.cget("background"))

        # registers
        for i, lbl in enumerate(self.reg_labels):
            lbl.config(text=f"R{i}: {self.cpu.regs[i]}")

        # memory
        self.mem_text.configure(state="normal")
        self.mem_text.delete("1.0", tk.END)
        for i, val in enumerate(self.cpu.memory):
            self.mem_text.insert(tk.END, f"{i} : {val}\n")
        self.mem_text.configure(state="disabled")

        # program text marker
        self.refresh_program_text()

    def on_step(self):
        self.cpu.step_forward()
        self.update_ui()

    def on_step_back(self):
        ok = self.cpu.step_back()
        if not ok:
            # if no history (first press), do a gentle reset
            self.cpu.reset()
        self.update_ui()

    def on_reset(self):
        self.cpu.push_history()
        self.cpu.pc = 0
        self.cpu.ir = None
        self.cpu.stage = Stage.IDLE
        self.cpu.regs = [0] * 4
        self.cpu.memory = [0] * 16
        self.update_ui()

    def on_play_pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button.config(text="Play")
            if self.play_job is not None:
                self.root.after_cancel(self.play_job)
                self.play_job = None
        else:
            self.is_playing = True
            self.play_button.config(text="Pause")
            self.play_tick()

    def play_tick(self):
        # one automated step then schedule next
        self.cpu.step_forward()
        self.update_ui()
        # stop if program ended and CPU is IDLE
        if self.cpu.stage == Stage.IDLE and not (0 <= self.cpu.pc < len(self.cpu.program)):
            self.is_playing = False
            self.play_button.config(text="Play")
            return
        delay = max(50, int(self.speed_var.get()))
        self.play_job = self.root.after(delay, self.play_tick)


def main():
    root = tk.Tk()
    app = VisualizerApp(root)
    root.geometry("820x520")
    root.mainloop()

if __name__ == "__main__":
    main()
