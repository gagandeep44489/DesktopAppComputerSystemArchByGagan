"""
Program Counter Simulation Tool (Tkinter)

Run:
    python "Program Counter Simulation Tool.py"

What it demonstrates:
- How the Program Counter (PC) moves during sequential execution
- How branch and jump instructions modify control flow
- How reset, step, back-step, and auto-run affect PC state
"""

from __future__ import annotations

import copy
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import List


@dataclass
class Instruction:
    op: str
    arg: int | None = None

    def asm(self) -> str:
        if self.arg is None:
            return self.op
        return f"{self.op} {self.arg:+d}" if self.op in {"JMP_REL", "BRZ"} else f"{self.op} {self.arg}"


@dataclass
class Snapshot:
    pc: int
    acc: int
    halted: bool
    zero_flag: bool
    steps: int


class ProgramCounterCPU:
    def __init__(self, program: List[Instruction]) -> None:
        self.program = program
        self.history: List[Snapshot] = []
        self.reset()

    def reset(self) -> None:
        self.pc = 0
        self.acc = 0
        self.halted = False
        self.zero_flag = True
        self.steps = 0
        self.history.clear()

    def snapshot(self) -> Snapshot:
        return Snapshot(
            pc=self.pc,
            acc=self.acc,
            halted=self.halted,
            zero_flag=self.zero_flag,
            steps=self.steps,
        )

    def step_back(self) -> bool:
        if not self.history:
            return False
        snap = self.history.pop()
        self.pc = snap.pc
        self.acc = snap.acc
        self.halted = snap.halted
        self.zero_flag = snap.zero_flag
        self.steps = snap.steps
        return True

    def _in_bounds(self) -> bool:
        return 0 <= self.pc < len(self.program)

    def step_forward(self) -> str:
        if self.halted:
            return "HALTED"

        if not self._in_bounds():
            self.halted = True
            return "PC out of bounds -> HALT"

        self.history.append(copy.deepcopy(self.snapshot()))
        inst = self.program[self.pc]
        current_pc = self.pc
        reason = ""

        if inst.op == "NOP":
            self.pc += 1
            reason = "NOP: PC <- PC + 1"
        elif inst.op == "INC":
            self.acc += 1
            self.pc += 1
            reason = "INC: ACC <- ACC + 1, PC <- PC + 1"
        elif inst.op == "DEC":
            self.acc -= 1
            self.pc += 1
            reason = "DEC: ACC <- ACC - 1, PC <- PC + 1"
        elif inst.op == "LOADI":
            assert inst.arg is not None
            self.acc = inst.arg
            self.pc += 1
            reason = f"LOADI: ACC <- {inst.arg}, PC <- PC + 1"
        elif inst.op == "JMP":
            assert inst.arg is not None
            self.pc = inst.arg
            reason = f"JMP: PC <- {inst.arg}"
        elif inst.op == "JMP_REL":
            assert inst.arg is not None
            self.pc = current_pc + inst.arg
            reason = f"JMP_REL: PC <- {current_pc} + ({inst.arg:+d}) = {self.pc}"
        elif inst.op == "BRZ":
            assert inst.arg is not None
            if self.zero_flag:
                self.pc = current_pc + inst.arg
                reason = f"BRZ taken: Z=1, PC <- {current_pc} + ({inst.arg:+d}) = {self.pc}"
            else:
                self.pc += 1
                reason = "BRZ not taken: Z=0, PC <- PC + 1"
        elif inst.op == "HALT":
            self.halted = True
            reason = "HALT instruction executed"
        else:
            self.halted = True
            reason = f"Unknown op '{inst.op}' -> HALT"

        self.zero_flag = self.acc == 0
        self.steps += 1

        if not self._in_bounds() and not self.halted:
            self.halted = True
            reason += " | Next PC out of bounds -> HALT"

        return reason


SAMPLE_PROGRAM: List[Instruction] = [
    Instruction("LOADI", 3),     # 0  ACC=3
    Instruction("DEC"),          # 1
    Instruction("BRZ", +2),      # 2  if ACC==0 skip jump
    Instruction("JMP", 1),       # 3  loop back to DEC
    Instruction("NOP"),          # 4
    Instruction("INC"),          # 5
    Instruction("JMP_REL", -2),  # 6  demonstrate relative jump
    Instruction("HALT"),         # 7
]


class ProgramCounterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Program Counter Simulation Tool")
        self.cpu = ProgramCounterCPU(SAMPLE_PROGRAM)
        self.playing = False
        self.play_job: str | None = None

        self._build_ui()
        self._refresh()

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(2, weight=1)

        ttk.Label(
            main,
            text="Program Counter Simulation Tool",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(
            main,
            text="Observe how PC changes under sequential flow, branch, and jump operations.",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 10))

        left = ttk.LabelFrame(main, text="Program + State", padding=8)
        left.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        state = ttk.Frame(left)
        state.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.pc_var = tk.StringVar()
        self.acc_var = tk.StringVar()
        self.zero_var = tk.StringVar()
        self.halt_var = tk.StringVar()
        self.step_var = tk.StringVar()

        for i, (label, var) in enumerate(
            [
                ("PC", self.pc_var),
                ("ACC", self.acc_var),
                ("Zero Flag", self.zero_var),
                ("Halted", self.halt_var),
                ("Steps", self.step_var),
            ]
        ):
            ttk.Label(state, text=f"{label}:", font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w")
            ttk.Label(state, textvariable=var).grid(row=i, column=1, sticky="w", padx=(6, 0))

        self.program_list = tk.Listbox(left, height=14, font=("Consolas", 10))
        self.program_list.grid(row=1, column=0, sticky="nsew")
        for idx, inst in enumerate(self.cpu.program):
            self.program_list.insert("end", f"{idx:02d}: {inst.asm()}")

        right = ttk.LabelFrame(main, text="Controls + Trace", padding=8)
        right.grid(row=2, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        controls = ttk.Frame(right)
        controls.grid(row=0, column=0, sticky="ew")

        ttk.Button(controls, text="Step", command=self.on_step).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(controls, text="Back", command=self.on_back).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(controls, text="Reset", command=self.on_reset).grid(row=0, column=2, padx=2, pady=2)
        ttk.Button(controls, text="Run", command=self.on_run).grid(row=0, column=3, padx=2, pady=2)
        ttk.Button(controls, text="Pause", command=self.on_pause).grid(row=0, column=4, padx=2, pady=2)

        speed_row = ttk.Frame(right)
        speed_row.grid(row=1, column=0, sticky="ew", pady=(6, 4))
        speed_row.columnconfigure(1, weight=1)

        ttk.Label(speed_row, text="Speed:").grid(row=0, column=0, sticky="w")
        self.speed_var = tk.IntVar(value=500)
        ttk.Scale(speed_row, from_=100, to=1200, orient="horizontal", variable=self.speed_var).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

        self.trace = tk.Text(right, height=12, wrap="word")
        self.trace.grid(row=2, column=0, sticky="nsew", pady=(4, 0))
        self.trace.configure(state="disabled")

    def _append_trace(self, line: str) -> None:
        self.trace.configure(state="normal")
        self.trace.insert("end", line + "\n")
        self.trace.see("end")
        self.trace.configure(state="disabled")

    def _refresh(self) -> None:
        self.pc_var.set(str(self.cpu.pc))
        self.acc_var.set(str(self.cpu.acc))
        self.zero_var.set("1" if self.cpu.zero_flag else "0")
        self.halt_var.set("Yes" if self.cpu.halted else "No")
        self.step_var.set(str(self.cpu.steps))

        self.program_list.selection_clear(0, "end")
        if 0 <= self.cpu.pc < len(self.cpu.program):
            self.program_list.selection_set(self.cpu.pc)
            self.program_list.see(self.cpu.pc)

    def on_step(self) -> None:
        if self.cpu.halted:
            self._append_trace("Already halted. Use Reset to start over.")
            self._refresh()
            return

        pc_before = self.cpu.pc
        inst = self.cpu.program[pc_before] if 0 <= pc_before < len(self.cpu.program) else Instruction("<none>")
        reason = self.cpu.step_forward()
        self._append_trace(f"Step {self.cpu.steps:03d} | PC={pc_before:02d} | {inst.asm():<12} -> {reason}")
        self._refresh()

    def on_back(self) -> None:
        if self.cpu.step_back():
            self._append_trace(f"Back-step -> restored PC={self.cpu.pc}, ACC={self.cpu.acc}")
        else:
            self._append_trace("Back-step unavailable (history is empty).")
        self._refresh()

    def on_reset(self) -> None:
        self.on_pause()
        self.cpu.reset()
        self.trace.configure(state="normal")
        self.trace.delete("1.0", "end")
        self.trace.configure(state="disabled")
        self._append_trace("Simulation reset.")
        self._refresh()

    def on_run(self) -> None:
        if self.playing:
            return
        self.playing = True
        self._auto_step()

    def on_pause(self) -> None:
        self.playing = False
        if self.play_job is not None:
            self.root.after_cancel(self.play_job)
            self.play_job = None

    def _auto_step(self) -> None:
        if not self.playing:
            return
        if self.cpu.halted:
            self._append_trace("Auto-run stopped: CPU halted.")
            self.playing = False
            return

        self.on_step()
        delay = max(100, int(self.speed_var.get()))
        self.play_job = self.root.after(delay, self._auto_step)


def main() -> None:
    root = tk.Tk()
    ProgramCounterApp(root)
    root.minsize(900, 540)
    root.mainloop()


if __name__ == "__main__":
    main()