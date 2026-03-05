import tkinter as tk
from tkinter import ttk, messagebox


class CacheCoherencyVisualizer:
    """Desktop visualizer for MSI / MESI cache coherency transitions."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Cache Coherency Protocol Visualizer")
        self.root.geometry("980x650")

        self.protocol = tk.StringVar(value="MESI")
        self.sequence_input = tk.StringVar(value="C0:R, C1:R, C0:W, C1:R, C1:W")
        self.address = tk.StringVar(value="X")

        self.reset_state()
        self._build_ui()

    def reset_state(self) -> None:
        self.cache_states = {"C0": "I", "C1": "I"}
        self.memory_value = 0
        self.cache_data = {"C0": None, "C1": None}
        self.current_step = 0
        self.sequence = []

    def _build_ui(self) -> None:
        controls = ttk.LabelFrame(self.root, text="Controls", padding=12)
        controls.pack(fill="x", padx=12, pady=8)

        ttk.Label(controls, text="Protocol:").grid(row=0, column=0, sticky="w")
        proto_box = ttk.Combobox(
            controls,
            textvariable=self.protocol,
            values=["MSI", "MESI"],
            state="readonly",
            width=12,
        )
        proto_box.grid(row=0, column=1, padx=8)

        ttk.Label(controls, text="Address:").grid(row=0, column=2, sticky="w")
        ttk.Entry(controls, textvariable=self.address, width=10).grid(row=0, column=3, padx=8)

        ttk.Label(controls, text="Sequence (e.g., C0:R, C1:W):").grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Entry(controls, textvariable=self.sequence_input, width=70).grid(
            row=1, column=2, columnspan=4, sticky="we", pady=(8, 0)
        )

        ttk.Button(controls, text="Load Sequence", command=self.load_sequence).grid(row=0, column=4, padx=4)
        ttk.Button(controls, text="Step", command=self.step_once).grid(row=0, column=5, padx=4)
        ttk.Button(controls, text="Run All", command=self.run_all).grid(row=0, column=6, padx=4)
        ttk.Button(controls, text="Reset", command=self.reset_and_refresh).grid(row=0, column=7, padx=4)

        for col in range(8):
            controls.columnconfigure(col, weight=1 if col in (2, 3, 6) else 0)

        state_frame = ttk.LabelFrame(self.root, text="Current Cache Line States", padding=12)
        state_frame.pack(fill="x", padx=12, pady=8)

        self.core_state_labels = {}
        for i, core in enumerate(("C0", "C1")):
            card = ttk.Frame(state_frame, padding=10, relief="ridge")
            card.grid(row=0, column=i, sticky="nsew", padx=8)
            ttk.Label(card, text=core, font=("Arial", 12, "bold")).pack(anchor="w")
            state_lbl = ttk.Label(card, text="State: I", font=("Arial", 14))
            state_lbl.pack(anchor="w", pady=4)
            data_lbl = ttk.Label(card, text="Data: -", font=("Arial", 11))
            data_lbl.pack(anchor="w")
            self.core_state_labels[core] = (state_lbl, data_lbl)

        state_frame.columnconfigure(0, weight=1)
        state_frame.columnconfigure(1, weight=1)

        misc = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        misc.pack(fill="x")
        self.memory_label = ttk.Label(misc, text="Memory Value: 0", font=("Arial", 11, "bold"))
        self.memory_label.pack(side="left")
        self.step_label = ttk.Label(misc, text="Step: 0 / 0", font=("Arial", 11))
        self.step_label.pack(side="right")

        log_frame = ttk.LabelFrame(self.root, text="Bus / Transition Log", padding=8)
        log_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.log = tk.Text(log_frame, height=18, wrap="word", font=("Consolas", 10))
        self.log.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        scroll.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scroll.set)

        self.refresh_ui()

    def parse_sequence(self, raw: str):
        items = [x.strip() for x in raw.split(",") if x.strip()]
        parsed = []
        for item in items:
            try:
                core, op = item.split(":")
                core = core.strip().upper()
                op = op.strip().upper()
            except ValueError as exc:
                raise ValueError(f"Invalid token '{item}'. Use C0:R format.") from exc

            if core not in ("C0", "C1"):
                raise ValueError(f"Unknown core '{core}'. Use C0 or C1.")
            if op not in ("R", "W"):
                raise ValueError(f"Unknown operation '{op}'. Use R or W.")
            parsed.append((core, op))
        if not parsed:
            raise ValueError("Sequence is empty.")
        return parsed

    def load_sequence(self) -> None:
        try:
            self.sequence = self.parse_sequence(self.sequence_input.get())
        except ValueError as err:
            messagebox.showerror("Invalid sequence", str(err))
            return

        self.current_step = 0
        self.log.delete("1.0", "end")
        self.log_event(
            f"Loaded sequence for {self.protocol.get()} on address {self.address.get()}: {self.sequence_input.get()}"
        )
        self.refresh_ui()

    def reset_and_refresh(self) -> None:
        self.reset_state()
        self.log.delete("1.0", "end")
        self.log_event("Simulation reset.")
        self.refresh_ui()

    def run_all(self) -> None:
        if not self.sequence:
            self.load_sequence()
            if not self.sequence:
                return
        while self.current_step < len(self.sequence):
            self.step_once(show_done=False)
        self.log_event("Sequence complete.")

    def step_once(self, show_done: bool = True) -> None:
        if not self.sequence:
            self.load_sequence()
            if not self.sequence:
                return

        if self.current_step >= len(self.sequence):
            if show_done:
                messagebox.showinfo("Done", "No more operations in the loaded sequence.")
            return

        core, op = self.sequence[self.current_step]
        self.current_step += 1

        if self.protocol.get() == "MSI":
            self.apply_msi(core, op)
        else:
            self.apply_mesi(core, op)

        self.refresh_ui()

    def other_core(self, core: str) -> str:
        return "C1" if core == "C0" else "C0"

    def apply_msi(self, core: str, op: str) -> None:
        other = self.other_core(core)
        s, o = self.cache_states[core], self.cache_states[other]

        if op == "R":
            if s == "I":
                if o == "M":
                    self.cache_states[other] = "S"
                    self.memory_value = self.cache_data[other]
                    self.log_event(f"{other} flushes modified line to memory; M→S")
                self.cache_states[core] = "S"
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} read miss: BusRd, state I→S")
            else:
                self.log_event(f"{core} read hit in state {s}")
        else:  # Write
            if s == "M":
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write hit in M (stays M), updates cached value")
            elif s == "S":
                self.cache_states[other] = "I" if o == "S" else o
                self.cache_states[core] = "M"
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write upgrade: BusUpgr, S→M; invalidates shared copies")
            else:  # I
                if o in ("S", "M"):
                    if o == "M":
                        self.memory_value = self.cache_data[other]
                        self.log_event(f"{other} flushes modified line to memory before invalidation")
                    self.cache_states[other] = "I"
                self.cache_states[core] = "M"
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write miss: BusRdX, I→M; other copies invalidated")

    def apply_mesi(self, core: str, op: str) -> None:
        other = self.other_core(core)
        s, o = self.cache_states[core], self.cache_states[other]

        if op == "R":
            if s == "I":
                if o == "I":
                    self.cache_states[core] = "E"
                    self.cache_data[core] = self.memory_value
                    self.log_event(f"{core} read miss with no sharers: BusRd, I→E")
                else:
                    if o == "M":
                        self.cache_states[other] = "S"
                        self.memory_value = self.cache_data[other]
                        self.log_event(f"{other} flushes modified line: M→S")
                    elif o == "E":
                        self.cache_states[other] = "S"
                        self.log_event(f"{other} supplies clean line: E→S")
                    self.cache_states[core] = "S"
                    self.cache_data[core] = self.memory_value
                    self.log_event(f"{core} read miss with sharer: I→S")
            else:
                self.log_event(f"{core} read hit in state {s}")
        else:  # Write
            if s == "M":
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write hit in M, remains M")
            elif s == "E":
                self.cache_states[core] = "M"
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} silent upgrade E→M on write")
            elif s == "S":
                if o == "S":
                    self.cache_states[other] = "I"
                self.cache_states[core] = "M"
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write upgrade: BusUpgr, S→M")
            else:  # I
                if o in ("S", "E", "M"):
                    if o == "M":
                        self.memory_value = self.cache_data[other]
                        self.log_event(f"{other} flushes M line to memory before invalidation")
                    self.cache_states[other] = "I"
                self.cache_states[core] = "M"
                self.memory_value += 1
                self.cache_data[core] = self.memory_value
                self.log_event(f"{core} write miss: BusRdX, I→M")

    def log_event(self, msg: str) -> None:
        self.log.insert("end", f"[{self.current_step}] {msg}\n")
        self.log.see("end")

    def refresh_ui(self) -> None:
        for core in ("C0", "C1"):
            state_lbl, data_lbl = self.core_state_labels[core]
            state_lbl.config(text=f"State: {self.cache_states[core]}")
            value = self.cache_data[core]
            data_lbl.config(text=f"Data: {'-' if value is None else value}")

        self.memory_label.config(text=f"Memory Value: {self.memory_value}")
        self.step_label.config(text=f"Step: {self.current_step} / {len(self.sequence)}")


def main() -> None:
    root = tk.Tk()
    app = CacheCoherencyVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()