import tkinter as tk
from tkinter import messagebox

class CacheSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Level Cache Simulator")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Cache Sizes
        self.l1_size = 3
        self.l2_size = 5

        self.l1_cache = []
        self.l2_cache = []

        self.hits = 0
        self.misses = 0
        self.total_requests = 0

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Multi-Level Cache Simulator",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        tk.Label(self.root, text="Enter Memory Address:").pack()
        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=5)

        tk.Button(self.root, text="Access Memory",
                  command=self.access_memory).pack(pady=5)

        tk.Button(self.root, text="Reset",
                  command=self.reset).pack(pady=5)

        self.result_text = tk.StringVar()
        self.result_label = tk.Label(self.root, textvariable=self.result_text,
                                     justify="left", font=("Arial", 11))
        self.result_label.pack(pady=15)

    def access_memory(self):
        address = self.entry.get().strip()
        if address == "":
            messagebox.showerror("Error", "Enter a valid memory address")
            return

        self.total_requests += 1

        # L1 Cache Check
        if address in self.l1_cache:
            self.hits += 1
            result = f"L1 Cache HIT for address {address}\n"
        
        # L2 Cache Check
        elif address in self.l2_cache:
            self.hits += 1
            result = f"L2 Cache HIT for address {address}\n"
            self.update_cache(self.l1_cache, self.l1_size, address)
        
        # Miss (Main Memory)
        else:
            self.misses += 1
            result = f"Cache MISS for address {address} (Loaded from Main Memory)\n"
            self.update_cache(self.l2_cache, self.l2_size, address)
            self.update_cache(self.l1_cache, self.l1_size, address)

        hit_ratio = self.hits / self.total_requests
        miss_ratio = self.misses / self.total_requests

        result += f"\nL1 Cache: {self.l1_cache}"
        result += f"\nL2 Cache: {self.l2_cache}"
        result += f"\n\nTotal Requests: {self.total_requests}"
        result += f"\nHits: {self.hits}"
        result += f"\nMisses: {self.misses}"
        result += f"\nHit Ratio: {hit_ratio:.2f}"
        result += f"\nMiss Ratio: {miss_ratio:.2f}"

        self.result_text.set(result)
        self.entry.delete(0, tk.END)

    def update_cache(self, cache, size, address):
        if address in cache:
            cache.remove(address)
        elif len(cache) >= size:
            cache.pop(0)
        cache.append(address)

    def reset(self):
        self.l1_cache = []
        self.l2_cache = []
        self.hits = 0
        self.misses = 0
        self.total_requests = 0
        self.result_text.set("Simulator Reset")

if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulator(root)
    root.mainloop()
