import tkinter as tk
from tkinter import messagebox

class PagingSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("Paging Simulator")

        tk.Label(root, text="Enter Page Reference String (comma separated):").pack()
        self.pages_entry = tk.Entry(root, width=50)
        self.pages_entry.pack()

        tk.Label(root, text="Number of Frames:").pack()
        self.frames_entry = tk.Entry(root)
        self.frames_entry.pack()

        tk.Label(root, text="Select Algorithm:").pack()
        self.algorithm_var = tk.StringVar(value="FIFO")
        tk.OptionMenu(root, self.algorithm_var, 
                      "FIFO", "LRU", "Optimal").pack()

        tk.Button(root, text="Simulate", command=self.simulate).pack(pady=10)

        self.output_text = tk.Text(root, height=15, width=70)
        self.output_text.pack()

    def simulate(self):
        try:
            pages = list(map(int, self.pages_entry.get().split(",")))
            frames_count = int(self.frames_entry.get())
            algorithm = self.algorithm_var.get()

            frames = []
            page_faults = 0
            self.output_text.delete(1.0, tk.END)

            for i, page in enumerate(pages):
                if page not in frames:
                    page_faults += 1
                    if len(frames) < frames_count:
                        frames.append(page)
                    else:
                        if algorithm == "FIFO":
                            frames.pop(0)

                        elif algorithm == "LRU":
                            lru_index = min(
                                range(len(frames)),
                                key=lambda x: pages[:i][::-1].index(frames[x])
                            )
                            frames.pop(lru_index)

                        elif algorithm == "Optimal":
                            future = pages[i+1:]
                            replace_index = -1
                            farthest = -1
                            for j in range(len(frames)):
                                if frames[j] not in future:
                                    replace_index = j
                                    break
                                else:
                                    idx = future.index(frames[j])
                                    if idx > farthest:
                                        farthest = idx
                                        replace_index = j
                            frames.pop(replace_index)

                        frames.append(page)

                    self.output_text.insert(tk.END, f"Page {page} → FAULT | Frames: {frames}\n")
                else:
                    self.output_text.insert(tk.END, f"Page {page} → HIT   | Frames: {frames}\n")

            self.output_text.insert(tk.END, f"\nTotal Page Faults: {page_faults}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PagingSimulator(root)
    root.mainloop()