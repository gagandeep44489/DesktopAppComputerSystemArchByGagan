import tkinter as tk
from tkinter import messagebox

class CacheAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Hit/Miss Analyzer")
        self.root.geometry("750x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Cache Hit/Miss Analyzer",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Enter Memory Reference String (comma separated):").pack()
        self.entry_refs = tk.Entry(self.root, width=60)
        self.entry_refs.pack(pady=5)

        tk.Label(self.root, text="Enter Cache Size:").pack()
        self.entry_size = tk.Entry(self.root, width=20)
        self.entry_size.pack(pady=5)

        tk.Label(self.root, text="Select Replacement Policy:").pack()
        self.policy_var = tk.StringVar(value="FIFO")
        tk.Radiobutton(self.root, text="FIFO", variable=self.policy_var, value="FIFO").pack()
        tk.Radiobutton(self.root, text="LRU", variable=self.policy_var, value="LRU").pack()

        tk.Button(self.root, text="Analyze",
                  command=self.analyze).pack(pady=10)

        tk.Button(self.root, text="Reset",
                  command=self.reset).pack(pady=5)

        self.result_text = tk.StringVar()
        tk.Label(self.root, textvariable=self.result_text,
                 justify="left", font=("Arial", 11)).pack(pady=15)

    def analyze(self):
        try:
            refs = [r.strip() for r in self.entry_refs.get().split(",") if r.strip()]
            cache_size = int(self.entry_size.get())

            if cache_size <= 0:
                raise ValueError

            cache = []
            hits = 0
            misses = 0
            policy = self.policy_var.get()

            log = ""

            for ref in refs:
                if ref in cache:
                    hits += 1
                    log += f"{ref} → HIT | "
                    if policy == "LRU":
                        cache.remove(ref)
                        cache.append(ref)
                else:
                    misses += 1
                    log += f"{ref} → MISS | "
                    if len(cache) >= cache_size:
                        cache.pop(0)
                    cache.append(ref)

                log += f"Cache: {cache}\n"

            total = hits + misses
            hit_ratio = hits / total if total else 0
            miss_ratio = misses / total if total else 0

            summary = f"\nTotal Requests: {total}"
            summary += f"\nHits: {hits}"
            summary += f"\nMisses: {misses}"
            summary += f"\nHit Ratio: {hit_ratio:.2f}"
            summary += f"\nMiss Ratio: {miss_ratio:.2f}"

            self.result_text.set(log + summary)

        except:
            messagebox.showerror("Error", "Invalid Input")

    def reset(self):
        self.entry_refs.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.result_text.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = CacheAnalyzer(root)
    root.mainloop()
