import tkinter as tk
from tkinter import messagebox

class BranchPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Branch Prediction Simulator")

        tk.Label(root, text="Branch Outcome Sequence (T / N):").pack()
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        self.predictor = tk.StringVar(value="1bit")

        options = [
            ("Always Taken", "always_taken"),
            ("Always Not Taken", "always_not"),
            ("1-Bit Predictor", "1bit"),
            ("2-Bit Predictor", "2bit")
        ]

        for text, value in options:
            tk.Radiobutton(root, text=text, variable=self.predictor, value=value).pack(anchor="w")

        tk.Button(root, text="Simulate", command=self.simulate).pack(pady=10)

        self.result = tk.Text(root, height=12, width=60)
        self.result.pack()

    def simulate(self):
        seq = self.entry.get().upper().split()
        if not seq or any(x not in ("T", "N") for x in seq):
            messagebox.showerror("Error", "Use only T or N separated by spaces.")
            return

        predictor = self.predictor.get()
        correct = 0
        history = "T"
        counter = 2  # 2-bit predictor (0–3)

        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, "Step | Prediction | Actual | Result\n")
        self.result.insert(tk.END, "-" * 40 + "\n")

        for i, actual in enumerate(seq, 1):
            if predictor == "always_taken":
                pred = "T"
            elif predictor == "always_not":
                pred = "N"
            elif predictor == "1bit":
                pred = history
            else:  # 2-bit predictor
                pred = "T" if counter >= 2 else "N"

            result = "✓" if pred == actual else "✗"
            if result == "✓":
                correct += 1

            self.result.insert(
                tk.END,
                f"{i:>4} | {pred:^10} | {actual:^6} | {result}\n"
            )

            # Update predictors
            history = actual
            if predictor == "2bit":
                if actual == "T":
                    counter = min(3, counter + 1)
                else:
                    counter = max(0, counter - 1)

        accuracy = (correct / len(seq)) * 100
        self.result.insert(tk.END, f"\nAccuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    BranchPredictorApp(root)
    root.mainloop()
