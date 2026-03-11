import tkinter as tk
from tkinter import messagebox


class MemoryEncryptionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Encryption Simulator")
        self.root.geometry("900x650")

        title = tk.Label(
            root,
            text="Memory Encryption Simulator",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=8)

        config_frame = tk.Frame(root)
        config_frame.pack(fill="x", padx=12)

        tk.Label(config_frame, text="Memory Content (ASCII):").grid(
            row=0, column=0, sticky="w"
        )
        self.memory_entry = tk.Entry(config_frame, width=70)
        self.memory_entry.grid(row=0, column=1, padx=6, pady=4, sticky="w")
        self.memory_entry.insert(0, "Hello Computer Architecture")

        tk.Label(config_frame, text="Encryption Key (0-255):").grid(
            row=1, column=0, sticky="w"
        )
        self.key_entry = tk.Entry(config_frame, width=20)
        self.key_entry.grid(row=1, column=1, padx=6, pady=4, sticky="w")
        self.key_entry.insert(0, "19")

        tk.Label(config_frame, text="Block Size (bytes):").grid(
            row=2, column=0, sticky="w"
        )
        self.block_size_entry = tk.Entry(config_frame, width=20)
        self.block_size_entry.grid(row=2, column=1, padx=6, pady=4, sticky="w")
        self.block_size_entry.insert(0, "4")

        tk.Label(config_frame, text="Start Address (hex):").grid(
            row=3, column=0, sticky="w"
        )
        self.base_addr_entry = tk.Entry(config_frame, width=20)
        self.base_addr_entry.grid(row=3, column=1, padx=6, pady=4, sticky="w")
        self.base_addr_entry.insert(0, "0x1000")

        button_frame = tk.Frame(root)
        button_frame.pack(fill="x", padx=12, pady=6)

        tk.Button(button_frame, text="Simulate", command=self.simulate).pack(
            side="left", padx=(0, 6)
        )
        tk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side="left")

        self.summary_label = tk.Label(
            root,
            text="",
            anchor="w",
            justify="left",
            fg="#1a1a1a",
            font=("Consolas", 10, "bold"),
        )
        self.summary_label.pack(fill="x", padx=12, pady=(0, 6))

        self.output = tk.Text(root, width=120, height=30, wrap="none")
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    @staticmethod
    def parse_base_address(raw: str) -> int:
        text = raw.strip().lower()
        if text.startswith("0x"):
            return int(text, 16)
        return int(text)

    @staticmethod
    def xor_encrypt(memory_bytes, key):
        encrypted = []
        for index, byte_value in enumerate(memory_bytes):
            round_key = (key + index) % 256
            encrypted.append(byte_value ^ round_key)
        return encrypted

    def clear_output(self):
        self.output.delete("1.0", tk.END)
        self.summary_label.config(text="")

    def simulate(self):
        try:
            plaintext = self.memory_entry.get()
            if not plaintext:
                raise ValueError("Memory content cannot be empty.")

            key = int(self.key_entry.get())
            if not (0 <= key <= 255):
                raise ValueError("Encryption key must be in the range 0-255.")

            block_size = int(self.block_size_entry.get())
            if block_size <= 0:
                raise ValueError("Block size must be greater than 0.")

            base_address = self.parse_base_address(self.base_addr_entry.get())
            if base_address < 0:
                raise ValueError("Start address cannot be negative.")

            memory_bytes = plaintext.encode("utf-8")
            encrypted_bytes = self.xor_encrypt(memory_bytes, key)
            decrypted_bytes = self.xor_encrypt(encrypted_bytes, key)

            self.clear_output()
            self.output.insert(tk.END, "Address   | Block | Plain(byte/char) | Round Key | Encrypted(hex)\n")
            self.output.insert(tk.END, "-" * 72 + "\n")

            for i, plain in enumerate(memory_bytes):
                block_id = i // block_size
                address = base_address + i
                round_key = (key + i) % 256
                encrypted = encrypted_bytes[i]
                plain_char = chr(plain) if 32 <= plain <= 126 else "."

                self.output.insert(
                    tk.END,
                    f"0x{address:04X} | {block_id:5d} | {plain:3d} / {plain_char:1s}"
                    f"         | {round_key:3d}      | 0x{encrypted:02X}\n",
                )

            self.output.insert(tk.END, "\n")
            self.output.insert(
                tk.END,
                "Encrypted Memory Image (hex): "
                + " ".join(f"{b:02X}" for b in encrypted_bytes)
                + "\n",
            )
            self.output.insert(
                tk.END,
                "Decrypted Verification: " + decrypted_bytes.decode("utf-8", errors="replace") + "\n",
            )

            integrity = "PASS" if decrypted_bytes == memory_bytes else "FAIL"
            self.summary_label.config(
                text=(
                    f"Bytes: {len(memory_bytes)}  |  Blocks: {(len(memory_bytes) + block_size - 1) // block_size}"
                    f"  |  Base Address: 0x{base_address:04X}  |  Integrity: {integrity}"
                )
            )

        except Exception as exc:
            messagebox.showerror("Invalid Input", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryEncryptionSimulator(root)
    root.mainloop()