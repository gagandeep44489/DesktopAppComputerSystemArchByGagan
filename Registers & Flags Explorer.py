#!/usr/bin/env python3
"""
Registers & Flags Explorer (desktop app)

A single-file Tkinter desktop app that lets users inspect/edit common CPU-like
registers and watch status flags update as arithmetic/logic operations run.
"""

import tkinter as tk
from tkinter import ttk, messagebox


REGISTER_NAMES = ["R0", "R1", "R2", "R3", "ACC", "PC", "SP"]
BIT_WIDTH_CHOICES = [8, 16, 32]


def mask_for_width(width: int) -> int:
    return (1 << width) - 1


def parse_number(text: str) -> int:
    s = text.strip().lower()
    if not s:
        raise ValueError("Value is empty")
    if s.startswith("0x"):
        return int(s, 16)
    if s.startswith("0b"):
        return int(s, 2)
    return int(s, 10)


class RegistersFlagsExplorer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Registers & Flags Explorer")
        self.geometry("980x640")

        self.bit_width = tk.IntVar(value=8)
        self.selected_register = tk.StringVar(value="R0")
        self.source_register = tk.StringVar(value="R1")
        self.immediate_value = tk.StringVar(value="1")
        self.operation = tk.StringVar(value="ADD")

        self.register_values = {name: 0 for name in REGISTER_NAMES}
        self.flag_values = {
            "Z": 0,  # Zero
            "N": 0,  # Negative/sign
            "C": 0,  # Carry/borrow indicator
            "V": 0,  # Overflow
        }

        self.register_display_vars = {
            name: tk.StringVar(value="0") for name in REGISTER_NAMES
        }
        self.flag_display_vars = {
            name: tk.StringVar(value="0") for name in self.flag_values
        }

        self._build_ui()
        self.refresh_views()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        top = ttk.LabelFrame(container, text="Configuration", padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="Bit width:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            top,
            textvariable=self.bit_width,
            values=BIT_WIDTH_CHOICES,
            state="readonly",
            width=8,
        ).grid(row=0, column=1, sticky="w", padx=(6, 16))

        ttk.Button(top, text="Reset CPU State", command=self.reset_state).grid(
            row=0, column=2, sticky="w"
        )

        middle = ttk.Frame(container)
        middle.pack(fill="both", expand=True, pady=8)
        middle.columnconfigure(0, weight=2)
        middle.columnconfigure(1, weight=1)

        regs_frame = ttk.LabelFrame(middle, text="Registers", padding=8)
        regs_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        regs_frame.columnconfigure(1, weight=1)

        for row, name in enumerate(REGISTER_NAMES):
            ttk.Label(regs_frame, text=f"{name}:").grid(row=row, column=0, sticky="w")
            ttk.Entry(
                regs_frame,
                textvariable=self.register_display_vars[name],
                width=28,
                state="readonly",
            ).grid(row=row, column=1, sticky="ew", pady=2)

        flags_frame = ttk.LabelFrame(middle, text="Flags", padding=8)
        flags_frame.grid(row=0, column=1, sticky="nsew")

        for row, (flag, label) in enumerate(
            [("Z", "Zero"), ("N", "Negative"), ("C", "Carry"), ("V", "Overflow")]
        ):
            ttk.Label(flags_frame, text=f"{flag} ({label})").grid(
                row=row, column=0, sticky="w"
            )
            ttk.Label(
                flags_frame,
                textvariable=self.flag_display_vars[flag],
                font=("TkDefaultFont", 10, "bold"),
            ).grid(row=row, column=1, sticky="e", padx=(8, 0))

        op_frame = ttk.LabelFrame(container, text="Operation Runner", padding=8)
        op_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(op_frame, text="Target register:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            op_frame,
            textvariable=self.selected_register,
            values=REGISTER_NAMES,
            state="readonly",
            width=8,
        ).grid(row=0, column=1, sticky="w", padx=(6, 12))

        ttk.Label(op_frame, text="Operation:").grid(row=0, column=2, sticky="w")
        ttk.Combobox(
            op_frame,
            textvariable=self.operation,
            values=["MOV", "ADD", "SUB", "AND", "OR", "XOR", "INC", "DEC"],
            state="readonly",
            width=8,
        ).grid(row=0, column=3, sticky="w", padx=(6, 12))

        ttk.Label(op_frame, text="Source register:").grid(row=0, column=4, sticky="w")
        ttk.Combobox(
            op_frame,
            textvariable=self.source_register,
            values=REGISTER_NAMES,
            state="readonly",
            width=8,
        ).grid(row=0, column=5, sticky="w", padx=(6, 12))

        ttk.Label(op_frame, text="Immediate:").grid(row=0, column=6, sticky="w")
        ttk.Entry(op_frame, textvariable=self.immediate_value, width=12).grid(
            row=0, column=7, sticky="w", padx=(6, 12)
        )

        ttk.Button(op_frame, text="Apply", command=self.apply_operation).grid(
            row=0, column=8, sticky="w"
        )

        help_text = (
            "Immediate accepts decimal (42), hex (0x2A), or binary (0b101010).\n"
            "MOV uses immediate value. ADD/SUB/AND/OR/XOR use source register value."
        )
        ttk.Label(container, text=help_text, foreground="#444").pack(anchor="w")

    def reset_state(self) -> None:
        self.register_values = {name: 0 for name in REGISTER_NAMES}
        self.flag_values = {key: 0 for key in self.flag_values}
        self.refresh_views()

    def refresh_views(self) -> None:
        width = self.bit_width.get()
        mask = mask_for_width(width)
        nibbles = (width + 3) // 4

        for name, value in self.register_values.items():
            v = value & mask
            self.register_display_vars[name].set(
                f"dec:{v:>10}   hex:0x{v:0{nibbles}X}   bin:{v:0{width}b}"
            )

        for flag, value in self.flag_values.items():
            self.flag_display_vars[flag].set(str(value))

    def update_zn_flags(self, result: int) -> None:
        width = self.bit_width.get()
        mask = mask_for_width(width)
        sign_bit = 1 << (width - 1)
        value = result & mask
        self.flag_values["Z"] = 1 if value == 0 else 0
        self.flag_values["N"] = 1 if (value & sign_bit) else 0

    def set_arith_flags(self, a: int, b: int, result: int, subtraction: bool = False) -> None:
        width = self.bit_width.get()
        mask = mask_for_width(width)
        sign_bit = 1 << (width - 1)

        a_m = a & mask
        b_m = b & mask
        r_m = result & mask

        if subtraction:
            self.flag_values["C"] = 1 if a_m >= b_m else 0
            self.flag_values["V"] = 1 if ((a_m ^ b_m) & (a_m ^ r_m) & sign_bit) else 0
        else:
            self.flag_values["C"] = 1 if (a_m + b_m) > mask else 0
            self.flag_values["V"] = 1 if (~(a_m ^ b_m) & (a_m ^ r_m) & sign_bit) else 0

        self.update_zn_flags(r_m)

    def apply_operation(self) -> None:
        target = self.selected_register.get()
        src = self.source_register.get()
        op = self.operation.get()

        width = self.bit_width.get()
        mask = mask_for_width(width)

        a = self.register_values[target] & mask
        b = self.register_values[src] & mask

        try:
            imm = parse_number(self.immediate_value.get()) & mask
        except ValueError as exc:
            messagebox.showerror("Invalid immediate", str(exc))
            return

        result = a
        if op == "MOV":
            result = imm
            self.flag_values["C"] = 0
            self.flag_values["V"] = 0
            self.update_zn_flags(result)
        elif op == "ADD":
            result = (a + b) & mask
            self.set_arith_flags(a, b, result, subtraction=False)
        elif op == "SUB":
            result = (a - b) & mask
            self.set_arith_flags(a, b, result, subtraction=True)
        elif op == "AND":
            result = a & b
            self.flag_values["C"] = 0
            self.flag_values["V"] = 0
            self.update_zn_flags(result)
        elif op == "OR":
            result = a | b
            self.flag_values["C"] = 0
            self.flag_values["V"] = 0
            self.update_zn_flags(result)
        elif op == "XOR":
            result = a ^ b
            self.flag_values["C"] = 0
            self.flag_values["V"] = 0
            self.update_zn_flags(result)
        elif op == "INC":
            result = (a + 1) & mask
            self.set_arith_flags(a, 1, result, subtraction=False)
        elif op == "DEC":
            result = (a - 1) & mask
            self.set_arith_flags(a, 1, result, subtraction=True)

        self.register_values[target] = result & mask
        self.refresh_views()


if __name__ == "__main__":
    app = RegistersFlagsExplorer()
    app.mainloop()