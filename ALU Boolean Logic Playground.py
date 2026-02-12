import tkinter as tk
from tkinter import messagebox

def perform_operation():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        operation = operation_var.get()

        if operation == "AND":
            result = a & b
        elif operation == "OR":
            result = a | b
        elif operation == "XOR":
            result = a ^ b
        elif operation == "NOT A":
            result = ~a
        elif operation == "NOT B":
            result = ~b
        elif operation == "Left Shift":
            result = a << b
        elif operation == "Right Shift":
            result = a >> b
        elif operation == "Add":
            result = a + b
        elif operation == "Subtract":
            result = a - b
        elif operation == "Multiply":
            result = a * b
        elif operation == "Divide":
            if b == 0:
                messagebox.showerror("Error", "Division by zero not allowed.")
                return
            result = a / b
        else:
            result = "Invalid Operation"

        result_label.config(text=f"Result: {result}")

    except:
        messagebox.showerror("Error", "Enter valid integer inputs.")

# GUI Setup
root = tk.Tk()
root.title("ALU Boolean Logic Playground")
root.geometry("500x450")

tk.Label(root, text="ALU Boolean Logic Playground", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Enter Value A").pack()
entry_a = tk.Entry(root)
entry_a.pack(pady=5)

tk.Label(root, text="Enter Value B").pack()
entry_b = tk.Entry(root)
entry_b.pack(pady=5)

operation_var = tk.StringVar(root)
operation_var.set("AND")

operations = [
    "AND", "OR", "XOR",
    "NOT A", "NOT B",
    "Left Shift", "Right Shift",
    "Add", "Subtract", "Multiply", "Divide"
]

tk.OptionMenu(root, operation_var, *operations).pack(pady=15)

tk.Button(root, text="Execute Operation", command=perform_operation).pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
