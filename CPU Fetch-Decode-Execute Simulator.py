"""
CPU Fetch-Decode-Execute Simulator (Tkinter)

Save as: cpu_fetch_decode_execute.py
Run:      python cpu_fetch_decode_execute.py

Focus: Visualize a single-instruction cycle with stages:
       FETCH -> DECODE -> EXECUTE

Features:
- Step forward / Step back (history snapshots)
- Play / Pause with adjustable speed
- PC, IR, Decoded fields (opcode, rd, rs, imm)
- Register file (R0..R3) and Memory (16 words)
- Simple sample program
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import List, Optional, Dict
import copy

# -----------------------
# CPU Model
# -----------------------

class Stage:
    FETCH = "FETCH"
    DECODE = "DECODE"
    EXECUTE = "EXECUTE"
    IDLE = "IDLE"

@dataclass
class Instruction:
    asm: str
    op: str
    rd: int = 0
    rs: int = 0
    imm: int = 0

@dataclass
class CPUStateSnapshot:
    pc: int
    ir: Optional[Instruction]
    stage: str
    regs: List[int]
    memory: List[int]
    decoded: Dict[str, Optional[int]]  # stores decoded fields for UI

class SimpleFetchDecodeExecuteCPU:
    def __init__(self, program: List[Instruction]):
        self.program = program
        self.reset()

    def reset(self):
        self.pc = 0
        self.ir: Optional[Instruction] = None
        self.stage = Stage.IDLE
        self.regs = [0] * 4  # R0..R3
        self.memory = [0] * 16
        self.decoded = {"op": None, "rd": None, "rs": None, "imm": None}
        self.history: List[CPUStateSnapshot] = []

    def snapshot(self) -> CPUStateSnapshot:
        return CPUStateSnapshot(
            pc=self.pc,
            ir=copy.deepcopy(self.ir),
            stage=self.stage,
            regs=copy.deepcopy(self.regs),
            memory=copy.deepcopy(self.memory),
            decoded=copy.deepcopy(self.decoded),
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
        self.decoded = s.decoded
        return True

    def step_forward(self):
        """Advance one stage in the cycle."""
        # save current state for Step Back
        self.push_history()

        if self.stage == Stage.IDLE or self.stage == Stage.EXECUTE:
            # Begin fetching next instruction (if any)
            if 0 <= self.pc < len(self.program):
                self.stage = Stage.FETCH
                self.ir = None
                self.decoded = {"op": None, "rd": None, "rs": None, "imm": None}
            else:
                # no more instructions
                self.stage = Stage.IDLE
                self.ir = None
        elif self.stage == Stage.FETCH:
            self._do_decode()
        elif self.stage == Stage.DECODE:
            self._do_execute()
        else:
            # fallback to IDLE
            self.stage = Stage.IDLE

    def _do_decode(self):
        """Set IR and decoded fields"""
        if not (0 <= self.pc < len(self.program)):
            self.ir = None
            self.stage = Stage.IDLE
            self.decoded = {"op": None, "rd": None, "rs": None, "imm": None}
            return
        self.ir = self.program[self.pc]
        # fill decoded view for UI
        self.decoded = {
            "op": self.ir.op,
            "rd": self.ir.rd,
            "rs": self.ir.rs,
            "imm": self.ir.imm,
        }
        self.stage = Stage.DECODE

    def _do_execute(self):
        """Perform the instruction action (writeback happens here for simplicity)"""
        if self.ir is None:
            self.stage = Stage.IDLE
            return
        op = self.ir.op
        if op == "MOVI":
            # Move immediate into destination register
            self.regs[self.ir.rd] = self.ir.imm
        elif op == "ADD":
            self.regs[self.ir.rd] = self.regs[self.ir.rd] + self.regs[self.ir.rs]
        elif op == "ADDI":
            self.regs[self.ir.rd] = self.regs[self.ir.rd] + self.ir.imm
        elif op == "LOAD":
            addr = max(0, min(len(self.memory) - 1, self.ir.imm))
            self.regs[self.ir.rd] = self.memory[addr]
        elif op == "STORE":
            addr = max(0, min(len(self.memory) - 1, self.ir.imm))
            self.memory[addr] = self.regs[self.ir.rs]
        # Advance PC and enter EXECUTE complete state (so next step begins fetch)
        self.pc += 1
        self.stage = Stage.EXECUTE

# -----------------------
# Sample Program
# -----------------------
SAMPLE_PROGRAM = [
    Instruction("MOVI R0, #7", "MOVI", rd=0, imm=7),
    Instruction("MOVI R1, #3", "MOVI", rd=1, imm=3),
    Instruction("ADD R0, R1", "ADD", rd=0, rs=1),
    Instruction("ADDI R2, #5", "ADDI", rd=2, imm=5),
    Instruction("STORE R0, 4", "STORE", rs=0, imm=4),
    Instruction("LOAD R3, 4", "LOAD", rd=3, imm=4),
]

# -----------------------
# UI (Tkinter)
# -----------------------

class FetchDecodeExecuteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Fetch-Decode-Execute Simulator")
        self.cpu = SimpleFetchDecodeExecuteCPU(SAMPLE_PROGRAM)
        self.playing = False
        self.play_job = None

        self._build_ui()
        self._refresh_ui()

    def _build_ui(self):
        pad = 8
        main = ttk.Frame(self.root, padding=pad)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        header = ttk.Label(main, text="CPU Fetch-Decode-Execute Simulator", font=("Segoe UI", 16, "bold"))
        header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

        # Stage boxes
        stage_frame = ttk.Frame(main)
        stage_frame.grid(row=1, column=0, columnspan=3, sticky="w")
        self.stage_labels: Dict[str, ttk.Label] = {}
        for i, s in enumerate([Stage.FETCH, Stage.DECODE, Stage.EXECUTE]):
            lbl = ttk.Label(stage_frame, text=s, relief="ridge", padding=(12, 8))
            lbl.grid(row=0, column=i, padx=6)
            self.stage_labels[s] = lbl

        # Left info: PC, IR, decoded fields, program
        left = ttk.Frame(main)
        left.grid(row=2, column=0, sticky="nsew", padx=(0,12), pady=(10,0))
        left.columnconfigure(1, weight=1)

        ttk.Label(left, text="PC:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.pc_var = tk.StringVar()
        ttk.Label(left, textvariable=self.pc_var).grid(row=0, column=1, sticky="w")

        ttk.Label(left, text="IR:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
        self.ir_var = tk.StringVar()
        ttk.Label(left, textvariable=self.ir_var).grid(row=1, column=1, sticky="w")

        ttk.Separator(left, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)

        # Decoded fields
        ttk.Label(left, text="Decoded:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w")
        df = ttk.Frame(left)
        df.grid(row=4, column=0, columnspan=2, sticky="w")
        ttk.Label(df, text="Opcode:").grid(row=0, column=0, sticky="w")
        self.dec_op_var = tk.StringVar()
        ttk.Label(df, textvariable=self.dec_op_var).grid(row=0, column=1, sticky="w", padx=(6,12))
        ttk.Label(df, text="rd:").grid(row=1, column=0, sticky="w")
        self.dec_rd_var = tk.StringVar()
        ttk.Label(df, textvariable=self.dec_rd_var).grid(row=1, column=1, sticky="w", padx=(6,12))
        ttk.Label(df, text="rs:").grid(row=2, column=0, sticky="w")
        self.dec_rs_var = tk.StringVar()
        ttk.Label(df, textvariable=self.dec_rs_var).grid(row=2, column=1, sticky="w", padx=(6,12))
        ttk.Label(df, text="imm:").grid(row=3, column=0, sticky="w")
        self.dec_imm_var = tk.StringVar()
        ttk.Label(df, textvariable=self.dec_imm_var).grid(row=3, column=1, sticky="w", padx=(6,12))

        ttk.Separator(left, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=6)

        ttk.Label(left, text="Program:", font=("Segoe UI", 10, "bold")).grid(row=6, column=0, sticky="w")
        self.program_text = tk.Text(left, height=8, width=36, padx=4, pady=4)
        self.program_text.grid(row=7, column=0, columnspan=2, sticky="nsew")
        self.program_text.configure(state="disabled")

        # Controls
        ctrls = ttk.Frame(main)
        ctrls.grid(row=3, column=0, sticky="w", pady=(10,0))
        ttk.Button(ctrls, text="Step Back", command=self.on_step_back).grid(row=0, column=0, padx=4)
        ttk.Button(ctrls, text="Step", command=self.on_step).grid(row=0, column=1, padx=4)
        ttk.Button(ctrls, text="Reset", command=self.on_reset).grid(row=0, column=2, padx=4)
        self.play_btn = ttk.Button(ctrls, text="Play", command=self.on_play_pause)
        self.play_btn.grid(row=0, column=3, padx=4)

        ttk.Label(ctrls, text="Speed (ms):").grid(row=0, column=4, padx=(12,4))
        self.speed_var = tk.IntVar(value=700)
        self.speed_scale = ttk.Scale(ctrls, from_=100, to=1500, orient="horizontal", variable=self.speed_var)
        self.speed_scale.grid(row=0, column=5, padx=4)

        # Right info: Registers & Memory
        right = ttk.Frame(main)
        right.grid(row=2, column=1, rowspan=2, sticky="nsew")
        right.columnconfigure(0, weight=1)

        regs_frame = ttk.LabelFrame(right, text="Registers (R0..R3)")
        regs_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=2)
        self.reg_labels = []
        for i in range(4):
            l = ttk.Label(regs_frame, text=f"R{i}: 0", padding=(6,4))
            l.grid(row=0, column=i, padx=6)
            self.reg_labels.append(l)

        mem_frame = ttk.LabelFrame(right, text="Memory (addr : val)")
        mem_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.mem_text = tk.Text(mem_frame, width=22, height=12)
        self.mem_text.pack(padx=4, pady=4)
        self.mem_text.configure(state="disabled")

        # Footer notes
        ttk.Label(main, text="Notes: Execute stage performs writeback here for clarity (so students see the result instantly).",
                  foreground="gray").grid(row=4, column=0, columnspan=2, sticky="w", pady=(8,0))

        # populate program text
        self._refresh_program_text()

    def _refresh_program_text(self):
        self.program_text.configure(state="normal")
        self.program_text.delete("1.0", tk.END)
        for idx, ins in enumerate(self.cpu.program):
            marker = "=> " if idx == self.cpu.pc else "   "
            self.program_text.insert(tk.END, f"{marker}{ins.asm}\n")
        self.program_text.configure(state="disabled")

    def _refresh_ui_stage_boxes(self):
        for s, lbl in self.stage_labels.items():
            if self.cpu.stage == s:
                lbl.config(background="#b3e5fc")
            else:
                # reset to default system bg
                lbl.config(background=self.root.cget("background"))

    def _refresh_registers(self):
        for i, lbl in enumerate(self.reg_labels):
            lbl.config(text=f"R{i}: {self.cpu.regs[i]}")

    def _refresh_memory(self):
        self.mem_text.configure(state="normal")
        self.mem_text.delete("1.0", tk.END)
        for i, v in enumerate(self.cpu.memory):
            self.mem_text.insert(tk.END, f"{i} : {v}\n")
        self.mem_text.configure(state="disabled")

    def _refresh_decoded(self):
        self.dec_op_var.set(str(self.cpu.decoded.get("op")) if self.cpu.decoded.get("op") is not None else "----")
        self.dec_rd_var.set(str(self.cpu.decoded.get("rd")) if self.cpu.decoded.get("rd") is not None else "----")
        self.dec_rs_var.set(str(self.cpu.decoded.get("rs")) if self.cpu.decoded.get("rs") is not None else "----")
        self.dec_imm_var.set(str(self.cpu.decoded.get("imm")) if self.cpu.decoded.get("imm") is not None else "----")

    def _refresh_ui(self):
        # PC and IR
        self.pc_var.set(str(self.cpu.pc))
        self.ir_var.set(self.cpu.ir.asm if self.cpu.ir else "----")
        # stages / decoded / registers / memory
        self._refresh_ui_stage_boxes()
        self._refresh_decoded()
        self._refresh_registers()
        self._refresh_memory()
        self._refresh_program_text()

    # -------------------------
    # Control handlers
    # -------------------------
    def on_step(self):
        self.cpu.step_forward()
        self._refresh_ui()

    def on_step_back(self):
        ok = self.cpu.pop_history()
        if not ok:
            # nothing to pop -> reset to initial
            self.cpu.reset()
        self._refresh_ui()

    def on_reset(self):
        self.cpu.push_history()
        self.cpu.reset()
        self._refresh_ui()

    def on_play_pause(self):
        if self.playing:
            # pause
            self.playing = False
            self.play_btn.config(text="Play")
            if self.play_job:
                self.root.after_cancel(self.play_job)
                self.play_job = None
        else:
            # start playing
            self.playing = True
            self.play_btn.config(text="Pause")
            self._play_tick()

    def _play_tick(self):
        # single tick then reschedule if still playing
        self.cpu.step_forward()
        self._refresh_ui()
        # If CPU is idle and pc is beyond program, stop
        if self.cpu.stage == Stage.IDLE and not (0 <= self.cpu.pc < len(self.cpu.program)):
            self.playing = False
            self.play_btn.config(text="Play")
            return
        delay = max(50, int(self.speed_var.get()))
        self.play_job = self.root.after(delay, self._play_tick)

def main():
    root = tk.Tk()
    app = FetchDecodeExecuteApp(root)
    root.geometry("880x540")
    root.mainloop()

if __name__ == "__main__":
    main()
