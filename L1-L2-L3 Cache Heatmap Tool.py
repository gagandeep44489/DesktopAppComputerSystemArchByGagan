import random
import tkinter as tk
from tkinter import ttk, messagebox


class CacheLevel:
    def __init__(self, name: str, num_sets: int, associativity: int, line_size: int):
        self.name = name
        self.num_sets = num_sets
        self.associativity = associativity
        self.line_size = line_size
        self.reset()

    def reset(self):
        self.sets = [[{"tag": None, "last_used": -1, "access_count": 0} for _ in range(self.associativity)] for _ in range(self.num_sets)]
        self.hits = 0
        self.misses = 0

    def _index_and_tag(self, address: int):
        block = address // self.line_size
        set_index = block % self.num_sets
        tag = block // self.num_sets
        return set_index, tag

    def access(self, address: int, tick: int):
        set_index, tag = self._index_and_tag(address)
        cache_set = self.sets[set_index]

        for line in cache_set:
            if line["tag"] == tag:
                line["last_used"] = tick
                line["access_count"] += 1
                self.hits += 1
                return True, set_index

        victim = min(cache_set, key=lambda x: x["last_used"])
        victim["tag"] = tag
        victim["last_used"] = tick
        victim["access_count"] += 1
        self.misses += 1
        return False, set_index

    def max_access_count(self):
        return max((line["access_count"] for cache_set in self.sets for line in cache_set), default=0)


class CacheHeatmapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L1/L2/L3 Cache Heatmap Tool")
        self.root.geometry("1240x780")

        self._build_ui()
        self._reset_levels()

    def _build_ui(self):
        config_frame = ttk.LabelFrame(self.root, text="Simulation Configuration")
        config_frame.pack(fill=tk.X, padx=10, pady=8)

        self.entries = {}
        fields = [
            ("Memory size (bytes)", "1048576"),
            ("Line size (bytes)", "64"),
            ("Access count", "3000"),
            ("L1 sets", "16"),
            ("L1 associativity", "4"),
            ("L2 sets", "32"),
            ("L2 associativity", "8"),
            ("L3 sets", "64"),
            ("L3 associativity", "16"),
        ]

        for i, (label, default) in enumerate(fields):
            ttk.Label(config_frame, text=label).grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=6, pady=4)
            entry = ttk.Entry(config_frame, width=12)
            entry.insert(0, default)
            entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
            self.entries[label] = entry

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10)

        ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation).pack(side=tk.LEFT, padx=5, pady=6)
        ttk.Button(button_frame, text="Reset", command=self.reset_all).pack(side=tk.LEFT, padx=5, pady=6)

        self.status_var = tk.StringVar(value="Ready. Configure inputs and run simulation.")
        ttk.Label(self.root, textvariable=self.status_var).pack(fill=tk.X, padx=10, pady=(0, 8))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self.level_views = {}
        for level_name in ("L1", "L2", "L3"):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f"{level_name} Heatmap")

            canvas = tk.Canvas(frame, bg="white")
            canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            stats_var = tk.StringVar(value=f"{level_name}: no data")
            ttk.Label(frame, textvariable=stats_var).pack(fill=tk.X, padx=8, pady=(0, 8))

            self.level_views[level_name] = {"canvas": canvas, "stats_var": stats_var}

    def _parse_positive_int(self, name):
        value = int(self.entries[name].get())
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
        return value

    def _reset_levels(self):
        line_size = self._safe_read("Line size (bytes)", 64)
        l1_sets = self._safe_read("L1 sets", 16)
        l1_assoc = self._safe_read("L1 associativity", 4)
        l2_sets = self._safe_read("L2 sets", 32)
        l2_assoc = self._safe_read("L2 associativity", 8)
        l3_sets = self._safe_read("L3 sets", 64)
        l3_assoc = self._safe_read("L3 associativity", 16)

        self.levels = [
            CacheLevel("L1", l1_sets, l1_assoc, line_size),
            CacheLevel("L2", l2_sets, l2_assoc, line_size),
            CacheLevel("L3", l3_sets, l3_assoc, line_size),
        ]

    def _safe_read(self, key, fallback):
        try:
            return max(1, int(self.entries[key].get()))
        except ValueError:
            return fallback

    def reset_all(self):
        self._reset_levels()
        for level in self.levels:
            self.draw_level_heatmap(level)
            self.level_views[level.name]["stats_var"].set(f"{level.name}: no data")
        self.status_var.set("Reset complete.")

    def run_simulation(self):
        try:
            memory_size = self._parse_positive_int("Memory size (bytes)")
            access_count = self._parse_positive_int("Access count")
            line_size = self._parse_positive_int("Line size (bytes)")
            self._reset_levels()
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        if memory_size < line_size:
            messagebox.showerror("Invalid input", "Memory size must be at least one line size.")
            return

        last_level_misses = 0
        for tick in range(access_count):
            address = random.randrange(0, memory_size, line_size)
            for level in self.levels:
                hit, _ = level.access(address, tick)
                if hit:
                    break
            else:
                last_level_misses += 1

        for level in self.levels:
            self.draw_level_heatmap(level)
            total = level.hits + level.misses
            hit_rate = (level.hits / total * 100) if total else 0.0
            self.level_views[level.name]["stats_var"].set(
                f"{level.name}: hits={level.hits}  misses={level.misses}  hit-rate={hit_rate:.2f}%"
            )

        self.status_var.set(
            f"Simulation complete: {access_count} accesses, memory={memory_size} bytes, DRAM fetches={last_level_misses}."
        )

    def draw_level_heatmap(self, level: CacheLevel):
        canvas = self.level_views[level.name]["canvas"]
        canvas.delete("all")
        canvas.update_idletasks()

        width = max(400, canvas.winfo_width())
        height = max(250, canvas.winfo_height())
        pad = 20
        rows = level.num_sets
        cols = level.associativity
        cell_w = max(16, (width - 2 * pad) / max(1, cols))
        cell_h = max(8, (height - 2 * pad) / max(1, rows))

        max_count = level.max_access_count()

        for r in range(rows):
            for c in range(cols):
                line = level.sets[r][c]
                x1 = pad + c * cell_w
                y1 = pad + r * cell_h
                x2 = x1 + cell_w
                y2 = y1 + cell_h
                color = self._heat_color(line["access_count"], max_count)
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#eeeeee")

        canvas.create_text(
            pad,
            8,
            text=f"{level.name} ({rows} sets x {cols} ways) | Darker = hotter cache lines",
            anchor="w",
            fill="#333333",
            font=("Arial", 10, "bold"),
        )

    def _heat_color(self, count, max_count):
        if max_count == 0:
            return "#f2f2f2"
        ratio = count / max_count
        red = 255
        green = int(255 - ratio * 205)
        blue = int(255 - ratio * 255)
        return f"#{red:02x}{green:02x}{blue:02x}"


def main():
    root = tk.Tk()
    app = CacheHeatmapApp(root)
    app.reset_all()
    root.mainloop()


if __name__ == "__main__":
    main()