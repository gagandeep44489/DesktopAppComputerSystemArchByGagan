import tkinter as tk
import threading
import time

def execute_instruction(instr, output_box):
    time.sleep(delay_var.get())
    output_box.insert(tk.END, f"Executed: {instr}\n")
    output_box.see(tk.END)

def sequential_execution():
    output_box.delete("1.0", tk.END)
    instructions = instruction_box.get("1.0", tk.END).strip().split("\n")

    start = time.time()
    for instr in instructions:
        execute_instruction(instr, output_box)
    end = time.time()

    output_box.insert(tk.END, f"\nSequential Execution Time: {round(end-start,2)} sec\n")

def parallel_execution():
    output_box.delete("1.0", tk.END)
    instructions = instruction_box.get("1.0", tk.END).strip().split("\n")

    threads = []
    start = time.time()

    for instr in instructions:
        t = threading.Thread(target=execute_instruction, args=(instr, output_box))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()
    output_box.insert(tk.END, f"\nParallel Execution Time: {round(end-start,2)} sec\n")

# GUI
root = tk.Tk()
root.title("Parallel Instruction Execution Demonstrator")
root.geometry("650x500")

tk.Label(root, text="Enter Instructions (one per line):").pack(pady=5)

instruction_box = tk.Text(root, height=8, width=70)
instruction_box.pack()

delay_var = tk.DoubleVar(value=1.0)
tk.Label(root, text="Execution Delay (seconds):").pack()
tk.Entry(root, textvariable=delay_var).pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Sequential Execution", command=sequential_execution).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Parallel Execution", command=parallel_execution).pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Execution Output:").pack()

output_box = tk.Text(root, height=15, width=70)
output_box.pack()

root.mainloop()
