#!/usr/bin/env python3
"""
ALU Operation Simulator (desktop app)

Single-file Tkinter app that simulates ALU operations with configurable bit-width,
operand base (decimal, binary, hex), and shows flags (Carry, Overflow, Zero, Negative).

Save as alu_simulator.py and run with: python alu_simulator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import functools

# ---------- ALU logic helpers ----------

def parse_int(text: str, base_hint: str):
    """
    Parse user input into integer. Accepts:
    - binary: start with 0b or 'b' or only contains 0/1
    - hex: start with 0x
    - decimal: otherwise
    base_hint: 'dec'|'bin'|'hex' to prefer a base when ambiguous
    """
    s = str(text).strip().lower()
    if s == '':
        raise ValueError("Empty input")
    # explicit prefixes
    if s.startswith('0b'):
        return int(s, 2)
    if s.startswith('b') and all(ch in '01' for ch in s[1:]):
        return int(s[1:], 2)
    if s.startswith('0x'):
        return int(s, 16)
    # if string contains hex letters
    if any(ch in 'abcdef' for ch in s):
        return int(s, 16)
    # if string contains only 0/1 and user prefers bin
    if all(ch in '01' for ch in s) and base_hint == 'bin':
        return int(s, 2)
    # try decimal parse, then fallback
    try:
        return int(s, 10)
    except ValueError:
        # fallback binary if only 0/1, else hex if starts with hex-like, else raise
        if all(ch in '01' for ch in s):
            return int(s, 2)
        raise ValueError(f"Cannot parse number: '{text}'")

def mask_for_width(width: int):
    return (1 << width) - 1

def twos_complement(value: int, width: int):
    """Return signed integer value interpreting value as two's complement of given width."""
    mask = mask_for_width(width)
    v = value & mask
    sign_bit = 1 << (width - 1)
    if v & sign_bit:
        return v - (1 << width)
    return v

def format_bin(value: int, width: int):
    mask = mask_for_width(width)
    v = value & mask
    return format(v, '0{}b'.format(width))

def format_hex(value: int, width: int):
    # hex digits to display
    nibbles = (width + 3) // 4
    mask = mask_for_width(width)
    v = value & mask
    return '0x' + format(v, '0{}X'.format(nibbles))

def compute_add(a: int, b: int, width: int):
    mask = mask_for_width(width)
    unsigned_sum = (a + b)
    result = unsigned_sum & mask
    carry = 1 if unsigned_sum > mask else 0
    # overflow: for signed two's complement, if signs of a and b are same and differ from result's sign
    sa = (a >> (width - 1)) & 1
    sb = (b >> (width - 1)) & 1
    sr = (result >> (width - 1)) & 1
    overflow = 1 if (sa == sb and sr != sa) else 0
    return result, carry, overflow

def compute_sub(a: int, b: int, width: int):
    # a - b = a + (~b + 1)
    mask = mask_for_width(width)
    unsigned_diff = (a - b) & ((1 << (width + 1)) - 1)  # keep carry detection safe
    result = unsigned_diff & mask
    # Borrow detection: in unsigned, borrow occurs if a < b
    borrow = 1 if a < b else 0
    # Carry flag often defined as not borrow for subtraction in some ISAs. We'll expose borrow separately as Carry= (not borrow).
    carry = 0 if borrow else 1
    # Overflow for signed: if signs of a and b differ and sign of result differs from sign of a
    sa = (a >> (width - 1)) & 1
    sb = (b >> (width - 1)) & 1
    sr = (result >> (width - 1)) & 1
    overflow = 1 if (sa != sb and sr != sa) else 0
    return result, carry, overflow, borrow

def compute_and(a: int, b: int, width: int):
    mask = mask_for_width(width)
    r = (a & b) & mask
    return r

def compute_or(a: int, b: int, width: int):
    mask = mask_for_width(width)
    r = (a | b) & mask
    return r

def compute_xor(a: int, b: int, width: int):
    mask = mask_for_width(width)
    r = (a ^ b) & mask
    return r

def compute_not(a: int, width: int):
    mask = mask_for_width(width)
    return (~a) & mask

def compute_shl(a: int, sh: int, width: int):
    mask = mask_for_width(width)
    r = (a << sh) & mask
    # carry out: last bit shifted out? For simplicity compute carry as bits shifted out beyond width
    carry_bits = (a >> (width - sh)) & ((1 << sh) - 1) if sh < width else a & ((1 << sh) - 1)
    carry = 1 if carry_bits != 0 else 0
    return r, carry

def compute_shr_logical(a: int, sh: int, width: int):
    # logical right shift inserts zeros
    r = (a & mask_for_width(width)) >> sh
    # carry: bits shifted out (lower bits)
    mask_out = (1 << sh) - 1 if sh > 0 else 0
    carry_bits = a & mask_out
    carry = 1 if carry_bits != 0 else 0
    return r, carry

def compute_shr_arithmetic(a: int, sh: int, width: int):
    # arithmetic preserves sign
    signed = twos_complement(a, width)
    r_signed = signed >> sh
    # convert back to two's complement representation in width
    r = r_signed & mask_for_width(width)
    # carry as bits shifted out lower bits
    mask_out = (1 << sh) - 1 if sh > 0 else 0
    carry_bits = a & mask_out
    carry = 1 if carry_bits != 0 else 0
    return r, carry

def compute_mul(a: int, b: int, width: int):
    mask = mask_for_width(width)
    unsigned_product = a * b
    result = unsigned_product & mask
    overflow = 1 if unsigned_product > mask else 0
    # no well-defined carry flag for multi-bit product; show high bits as overflow info
    high_bits = unsigned_product >> width
    return result, overflow, high_bits

# ---------- GUI ----------

class ALUSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ALU Operation Simulator")
        self.geometry("980x640")
        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, padding=8)
        main.pack(fill='both', expand=True)

        # Top row: operands and options
        row1 = ttk.Frame(main)
        row1.pack(fill='x', pady=4)

        # Operand A
        ttk.Label(row1, text="Operand A:").grid(row=0, column=0, sticky='w')
        self.op_a_var = tk.StringVar(value='0')
        ttk.Entry(row1, textvariable=self.op_a_var, width=20).grid(row=0, column=1, sticky='w', padx=4)

        # Operand B
        ttk.Label(row1, text="Operand B:").grid(row=0, column=2, sticky='w', padx=(12,0))
        self.op_b_var = tk.StringVar(value='0')
        ttk.Entry(row1, textvariable=self.op_b_var, width=20).grid(row=0, column=3, sticky='w', padx=4)

        # Base selection
        ttk.Label(row1, text="Base:").grid(row=0, column=4, sticky='w', padx=(12,0))
        self.base_var = tk.StringVar(value='dec')
        base_menu = ttk.Combobox(row1, textvariable=self.base_var, values=['dec','bin','hex'], width=6, state='readonly')
        base_menu.grid(row=0, column=5, sticky='w', padx=4)

        # Bit width
        ttk.Label(row1, text="Bit width:").grid(row=0, column=6, sticky='w', padx=(12,0))
        self.width_var = tk.IntVar(value=8)
        self.width_spin = ttk.Spinbox(row1, from_=4, to=64, textvariable=self.width_var, width=6)
        self.width_spin.grid(row=0, column=7, sticky='w', padx=4)

        # Operation selection
        row2 = ttk.Frame(main)
        row2.pack(fill='x', pady=8)

        ttk.Label(row2, text="Operation:").grid(row=0, column=0, sticky='w')
        self.op_var = tk.StringVar(value='ADD')
        ops = ['ADD','SUB','AND','OR','XOR','NOT','SHL','SHR_LOGIC','SAR','MUL']
        self.op_menu = ttk.Combobox(row2, textvariable=self.op_var, values=ops, state='readonly', width=12)
        self.op_menu.grid(row=0, column=1, padx=4)

        # Shift amount entry (used for shift ops)
        ttk.Label(row2, text="Shift amount:").grid(row=0, column=2, sticky='w', padx=(12,0))
        self.shift_var = tk.IntVar(value=1)
        ttk.Entry(row2, textvariable=self.shift_var, width=6).grid(row=0, column=3, sticky='w', padx=4)

        # Execute button
        ttk.Button(row2, text="Execute", command=self.execute).grid(row=0, column=4, padx=(12,0))

        ttk.Button(row2, text="Clear History", command=self.clear_history).grid(row=0, column=5, padx=(12,0))

        # Middle: result and flags
        mid = ttk.Frame(main)
        mid.pack(fill='x', pady=(12,6))

        # Result labels
        ttk.Label(mid, text="Result (dec):").grid(row=0, column=0, sticky='w')
        self.res_dec = tk.StringVar(value='0')
        ttk.Entry(mid, textvariable=self.res_dec, width=24, state='readonly').grid(row=0, column=1, sticky='w', padx=4)

        ttk.Label(mid, text="Result (bin):").grid(row=0, column=2, sticky='w', padx=(12,0))
        self.res_bin = tk.StringVar(value='0b0')
        ttk.Entry(mid, textvariable=self.res_bin, width=36, state='readonly').grid(row=0, column=3, sticky='w', padx=4, columnspan=2)

        ttk.Label(mid, text="Result (hex):").grid(row=1, column=0, sticky='w', pady=(8,0))
        self.res_hex = tk.StringVar(value='0x0')
        ttk.Entry(mid, textvariable=self.res_hex, width=24, state='readonly').grid(row=1, column=1, sticky='w', padx=4, pady=(8,0))

        # Flags
        flags_frame = ttk.LabelFrame(mid, text="Flags", padding=6)
        flags_frame.grid(row=1, column=2, columnspan=3, sticky='w', padx=(12,0), pady=(8,0))

        self.flag_carry = tk.IntVar(value=0)
        self.flag_overflow = tk.IntVar(value=0)
        self.flag_zero = tk.IntVar(value=0)
        self.flag_negative = tk.IntVar(value=0)
        self.flag_borrow = tk.IntVar(value=0)  # for subtraction clarity

        ttk.Checkbutton(flags_frame, text="Carry", variable=self.flag_carry, state='disabled').grid(row=0, column=0, padx=6)
        ttk.Checkbutton(flags_frame, text="Overflow", variable=self.flag_overflow, state='disabled').grid(row=0, column=1, padx=6)
        ttk.Checkbutton(flags_frame, text="Zero", variable=self.flag_zero, state='disabled').grid(row=0, column=2, padx=6)
        ttk.Checkbutton(flags_frame, text="Negative", variable=self.flag_negative, state='disabled').grid(row=0, column=3, padx=6)
        ttk.Checkbutton(flags_frame, text="Borrow", variable=self.flag_borrow, state='disabled').grid(row=0, column=4, padx=6)

        # Binary breakdown / signed interpretation
        breakdown = ttk.LabelFrame(main, text="Binary / Signed Info", padding=6)
        breakdown.pack(fill='both', expand=False, pady=(10,6))

        self.bin_text = tk.Text(breakdown, height=5, wrap='none')
        self.bin_text.pack(fill='both', expand=True)

        # Bottom: history
        hist_frame = ttk.LabelFrame(main, text="History", padding=6)
        hist_frame.pack(fill='both', expand=True)

        self.history_list = tk.Listbox(hist_frame, height=8)
        self.history_list.pack(side='left', fill='both', expand=True)
        vsb = ttk.Scrollbar(hist_frame, orient='vertical', command=self.history_list.yview)
        vsb.pack(side='right', fill='y')
        self.history_list.configure(yscrollcommand=vsb.set)
        self.history = []

    def clear_history(self):
        self.history = []
        self.history_list.delete(0, 'end')

    def execute(self):
        try:
            base = self.base_var.get()
            width = int(self.width_var.get())
            if width < 1 or width > 64:
                raise ValueError("Bit width must be 1..64")
            a = parse_int(self.op_a_var.get(), base)
            b = parse_int(self.op_b_var.get(), base)
            op = self.op_var.get()
            shift = int(self.shift_var.get() or 0)
            # normalize inputs to unsigned within width for internal ops where needed
            mask = mask_for_width(width)
            a_u = a & mask
            b_u = b & mask
        except Exception as e:
            messagebox.showerror("Input error", str(e))
            return

        # reset flags
        self.flag_carry.set(0)
        self.flag_overflow.set(0)
        self.flag_zero.set(0)
        self.flag_negative.set(0)
        self.flag_borrow.set(0)

        result_u = 0
        extra_info = ''

        try:
            if op == 'ADD':
                r, carry, overflow = compute_add(a_u, b_u, width)
                result_u = r
                self.flag_carry.set(carry)
                self.flag_overflow.set(overflow)
                self.flag_borrow.set(0)
            elif op == 'SUB':
                r, carry, overflow, borrow = compute_sub(a_u, b_u, width)
                result_u = r
                self.flag_carry.set(carry)
                self.flag_overflow.set(overflow)
                self.flag_borrow.set(borrow)
            elif op == 'AND':
                result_u = compute_and(a_u, b_u, width)
            elif op == 'OR':
                result_u = compute_or(a_u, b_u, width)
            elif op == 'XOR':
                result_u = compute_xor(a_u, b_u, width)
            elif op == 'NOT':
                result_u = compute_not(a_u, width)
            elif op == 'SHL':
                r, carry = compute_shl(a_u, shift, width)
                result_u = r
                self.flag_carry.set(carry)
            elif op == 'SHR_LOGIC':
                r, carry = compute_shr_logical(a_u, shift, width)
                result_u = r
                self.flag_carry.set(carry)
            elif op == 'SAR':
                r, carry = compute_shr_arithmetic(a_u, shift, width)
                result_u = r
                self.flag_carry.set(carry)
            elif op == 'MUL':
                r, overflow, high = compute_mul(a_u, b_u, width)
                result_u = r
                self.flag_overflow.set(1 if overflow else 0)
                extra_info = f"  [high bits: 0x{high:X}]" if high != 0 else ''
            else:
                raise ValueError("Unsupported operation")
        except Exception as e:
            messagebox.showerror("Operation error", str(e))
            return

        # set other flags
        self.flag_zero.set(1 if (result_u & mask) == 0 else 0)
        # negative / sign bit
        sign_bit = 1 << (width - 1)
        self.flag_negative.set(1 if (result_u & sign_bit) != 0 else 0)

        # show result in dec/bin/hex; also signed interpretation
        signed = twos_complement(result_u, width)
        self.res_dec.set(str(signed if self.flag_negative.get() else result_u))
        # For clarity show both signed and unsigned in decimal field if negative:
        if self.flag_negative.get():
            self.res_dec.set(f"{signed} (unsigned {result_u})")
        self.res_bin.set('0b' + format_bin(result_u, width))
        self.res_hex.set(format_hex(result_u, width))

        # binary breakdown
        bin_lines = []
        bin_lines.append(f"Operand A (unsigned): {a_u}    {format_bin(a_u, width)}    {format_hex(a_u, width)}")
        bin_lines.append(f"Operand B (unsigned): {b_u}    {format_bin(b_u, width)}    {format_hex(b_u, width)}")
        bin_lines.append(f"Result    (unsigned): {result_u}    {format_bin(result_u, width)}    {format_hex(result_u, width)}{extra_info}")
        bin_lines.append(f"Signed interpretation (two's complement {width}-bit): {twos_complement(a_u, width)} , {twos_complement(b_u, width)} -> {twos_complement(result_u, width)}")
        bin_lines.append(f"Flags: Carry={self.flag_carry.get()}  Overflow={self.flag_overflow.get()}  Borrow={self.flag_borrow.get()}  Zero={self.flag_zero.get()}  Negative={self.flag_negative.get()}")
        self.bin_text.delete('1.0', 'end')
        self.bin_text.insert('end', '\n'.join(bin_lines))

        # add to history
        history_line = f"{op} | A={self.op_a_var.get()} B={self.op_b_var.get()} width={width} -> {self.res_dec.get()} | {self.res_bin.get()} | C={self.flag_carry.get()} V={self.flag_overflow.get()} Z={self.flag_zero.get()} N={self.flag_negative.get()}"
        self.history.append(history_line)
        self.history_list.insert('end', history_line)
        # select last
        self.history_list.see('end')

# ---------- Run ----------
if __name__ == "__main__":
    app = ALUSimulator()
    app.mainloop()
