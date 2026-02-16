import tkinter as tk
from tkinter import ttk

def show_comparison():
    data = [
        ("Feature", "DRAM", "SRAM"),
        ("Full Form", "Dynamic Random Access Memory", "Static Random Access Memory"),
        ("Storage Mechanism", "Capacitor + Transistor", "Flip-Flops (6 transistors)"),
        ("Refresh Required", "Yes", "No"),
        ("Speed", "Slower", "Faster"),
        ("Cost", "Cheaper", "Expensive"),
        ("Density", "High", "Low"),
        ("Power Consumption", "Low per bit", "Higher per bit"),
        ("Used In", "Main Memory (RAM)", "Cache Memory (L1, L2, L3)"),
        ("Volatility", "Volatile", "Volatile")
    ]

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            label = tk.Label(table_frame, text=value, borderwidth=1, relief="solid", 
                             width=28, height=2, font=("Arial", 10))
            label.grid(row=i, column=j)

# GUI Setup
root = tk.Tk()
root.title("DRAM vs SRAM Comparison Tool")
root.geometry("900x450")

title_label = tk.Label(root, text="DRAM vs SRAM Comparison Tool", 
                       font=("Arial", 16, "bold"))
title_label.pack(pady=15)

table_frame = tk.Frame(root)
table_frame.pack()

show_comparison()

root.mainloop()
