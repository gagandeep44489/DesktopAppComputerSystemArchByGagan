import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

df = None

# -----------------------------
# Load CSV File
# -----------------------------
def load_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Select Memory Log CSV",
        filetypes=[("CSV Files", "*.csv")]
    )
    
    if file_path:
        try:
            df = pd.read_csv(file_path)

            required_cols = {"Timestamp", "Operation", "Bytes"}
            if not required_cols.issubset(df.columns):
                messagebox.showerror(
                    "Invalid File",
                    "CSV must contain: Timestamp, Operation, Bytes"
                )
                df = None
                return

            messagebox.showinfo("Success", "Memory log loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# -----------------------------
# Analyze Memory Traffic
# -----------------------------
def analyze_traffic():
    global df

    if df is None:
        messagebox.showerror("Error", "Load memory log first.")
        return

    total_reads = len(df[df["Operation"] == "READ"])
    total_writes = len(df[df["Operation"] == "WRITE"])
    total_bytes = df["Bytes"].sum()

    time_span = df["Timestamp"].max() - df["Timestamp"].min()
    bandwidth = total_bytes / time_span if time_span > 0 else 0

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Memory Bus Traffic Analysis\n\n")
    result_text.insert(tk.END, f"Total READ operations: {total_reads}\n")
    result_text.insert(tk.END, f"Total WRITE operations: {total_writes}\n")
    result_text.insert(tk.END, f"Total Data Transferred: {total_bytes} bytes\n")
    result_text.insert(tk.END, f"Estimated Bandwidth: {bandwidth:.2f} bytes/sec\n")

# -----------------------------
# Plot Traffic Over Time
# -----------------------------
def plot_traffic():
    global df

    if df is None:
        messagebox.showerror("Error", "Load memory log first.")
        return

    traffic = df.groupby("Timestamp")["Bytes"].sum()

    plt.figure()
    plt.plot(traffic.index, traffic.values)
    plt.xlabel("Timestamp (seconds)")
    plt.ylabel("Bytes Transferred")
    plt.title("Memory Bus Traffic Over Time")
    plt.show()

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Memory Bus Traffic Analyzer")
root.geometry("650x500")

tk.Label(root, text="Memory Bus Traffic Analyzer",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Load Memory Log",
          command=load_file,
          bg="blue", fg="white").pack(pady=5)

tk.Button(root, text="Analyze Traffic",
          command=analyze_traffic,
          bg="green", fg="white").pack(pady=5)

tk.Button(root, text="Plot Traffic",
          command=plot_traffic,
          bg="orange", fg="white").pack(pady=5)

tk.Label(root, text="Results:",
         font=("Arial", 12, "bold")).pack(pady=5)

result_text = tk.Text(root, height=15, width=70, bg="#f4f4f4")
result_text.pack(padx=10, pady=5)

root.mainloop()