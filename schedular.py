import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


# Define Scheduling Algorithms
def fcfs(tasks):
    tasks.sort(key=lambda x: x[1]) 
    current_time = 0
    execution_order=[]
    
    for task in tasks:
        pid, arrival, burst, priority = task
        if current_time < arrival:
            current_time = arrival
        start_time=current_time
        current_time += burst
    
        execution_order.append((pid, start_time, burst))

    return execution_order

def round_robin(tasks, quantum=1):
    tasks.sort(key=lambda x: x[1]) 
    queue = deque()
    remaining_time = {task[0]: task[2] for task in tasks}

    execution_order = [] 
    time = 0
    i = 0
    
    while i < len(tasks) or queue:
        while i < len(tasks) and tasks[i][1] <= time:
            queue.append(tasks[i])
            i += 1
        
        if queue:
            pid, arrival, burst, priority = queue.popleft()
            execute_time = min(quantum, remaining_time[pid])
            current_time = time
            time += execute_time
            remaining_time[pid] -= execute_time
            
            while i < len(tasks) and tasks[i][1] <= time:
                queue.append(tasks[i])
                i += 1
            
            if remaining_time[pid] > 0:
                queue.append((pid, arrival, burst, priority))

            execution_order.append((pid, current_time, execute_time))
        else:
            time = tasks[i][1] if i < len(tasks) else time
    
    return execution_order

def shortest_process_next(tasks):
    tasks.sort(key=lambda x: x[1])  
    ready_queue = []
    current_time = 0
    remaining_tasks = tasks.copy()
    execution_order = [] 

    while remaining_tasks or ready_queue:
        i = 0
        while i < len(remaining_tasks):
            if remaining_tasks[i][1] <= current_time:
                ready_queue.append(remaining_tasks.pop(i))
            else:
                i += 1  

        if not ready_queue:
            next_task = min(remaining_tasks, key=lambda x: x[1])  
            current_time = next_task[1]
            ready_queue.append(next_task)
            remaining_tasks.remove(next_task)

        ready_queue.sort(key=lambda x: x[2])

        task = ready_queue.pop(0)
        pid, arrival, burst, priority = task
        start_time = current_time  
        current_time += burst

        execution_order.append((pid, start_time, burst))

    return execution_order

def shortest_remaining_time_next(tasks):
    tasks.sort(key=lambda x: x[1])

    remaining_time = {task[0]: task[2] for task in tasks}

    current_time = 0

    execution_intervals = []

    running_process = None
    process_start_time = 0

    while remaining_time:
        available_tasks = [task for task in tasks if task[1] <= current_time and task[0] in remaining_time]

        next_process = None
        if available_tasks:
            next_process = min(available_tasks, key=lambda x: remaining_time[x[0]])[0]

        if running_process is not None and (next_process != running_process or not available_tasks):
            execution_time = current_time - process_start_time
            if execution_time > 0:
                execution_intervals.append((running_process, process_start_time, execution_time))
            running_process = None

        if not available_tasks:
            future_tasks = [task for task in tasks if task[0] in remaining_time]
            if future_tasks:
                current_time = min(future_tasks, key=lambda x: x[1])[1]
                continue
            else:
                break  

        if running_process != next_process:
            running_process = next_process
            process_start_time = current_time

        remaining_time[next_process] -= 1
        current_time += 1

        if remaining_time[next_process] == 0:
            execution_time = current_time - process_start_time
            execution_intervals.append((next_process, process_start_time, execution_time))
            del remaining_time[next_process]
            running_process = None
    
    return execution_intervals

def priority_scheduling(tasks):
    tasks.sort(key=lambda x: x[1]) 
    current_time = 0
    execution_order = []
    remaining_tasks = tasks.copy()
    ready_queue = []
    
    while remaining_tasks or ready_queue:
        i = 0
        while i < len(remaining_tasks):
            if remaining_tasks[i][1] <= current_time:
                ready_queue.append(remaining_tasks.pop(i))
            else:
                i += 1

        if not ready_queue:
            current_time = remaining_tasks[0][1]
            ready_queue.append(remaining_tasks.pop(0))

        ready_queue.sort(key=lambda x: x[3])

        task = ready_queue.pop(0)
        pid, arrival, burst, priority = task
        start_time = current_time
        current_time += burst
        
        execution_order.append((pid, start_time, burst))
    
    return execution_order

def add_task():
    try:
        pid = int(entry_pid.get())
        arrival = int(entry_arrival.get())
        burst = int(entry_burst.get())
        priority = int(entry_priority.get())
        
        task_table.insert("", tk.END, values=(pid, arrival, burst, priority))
        clear_input_fields()
        entry_pid.focus()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values")

def clear_input_fields():
    entry_pid.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_quantum.delete(0, tk.END)

def clear_tasks():
    for item in task_table.get_children():
        task_table.delete(item)
    clear_input_fields()

def calculate_schedule():
    tasks = []
    for item in task_table.get_children():
        values = task_table.item(item, "values")
        tasks.append((int(values[0]), int(values[1]), int(values[2]), int(values[3])))
    
    if not tasks:
        messagebox.showerror("Error", "No tasks entered!")
        return
    
    if algo_choice.get() == "Auto Select":
        best_algorithm, execution_order = select_best_algorithm(tasks)
    else:
        best_algorithm = algo_choice.get()
        if best_algorithm == "First Come First Served (FCFS)":
            execution_order = fcfs(tasks)
        elif best_algorithm == "Round Robin":
            quantum = int(entry_quantum.get()) if entry_quantum.get() else 2
            execution_order = round_robin(tasks, quantum)
        elif best_algorithm == "Shortest Process Next":
            execution_order = shortest_process_next(tasks)
        elif best_algorithm == "Shortest Remaining Time Next":
            execution_order = shortest_remaining_time_next(tasks)
        elif best_algorithm == "Priority Scheduling":
            execution_order = priority_scheduling(tasks)
        else:
            messagebox.showerror("Error", "Algorithm not implemented yet!")
            return
    
    display_results(tasks, best_algorithm, execution_order)

def select_best_algorithm(tasks):
    algorithms = {
        "First Come First Served (FCFS)": fcfs,
        "Round Robin": lambda t: round_robin(t, quantum=2),
        "Shortest Process Next": shortest_process_next,
        "Shortest Remaining Time Next": shortest_remaining_time_next,
        "Priority Scheduling": priority_scheduling
    }
    
    best_algorithm = None
    best_avg_waiting_time = float('inf')
    best_execution_order = []
    
    for name, algo in algorithms.items():
        try:
            execution_order = algo(tasks[:])
            avg_waiting_time = calculate_avg_waiting_time(tasks, execution_order)
            
            if avg_waiting_time < best_avg_waiting_time:
                best_avg_waiting_time = avg_waiting_time
                best_algorithm = name
                best_execution_order = execution_order
        except Exception as e:
            print(f"Error with {name}: {e}")
            continue
    
    return best_algorithm, best_execution_order

def calculate_avg_waiting_time(tasks, execution_order):
    pid_to_index = {task[0]: i for i, task in enumerate(tasks)}
    completion = [-1] * len(tasks)
    turnaround = [0] * len(tasks)
    waiting = [0] * len(tasks)
    
    for ex in execution_order:
        pid, start_time, burst = ex
        task_index = pid_to_index[pid]
        end_time = start_time + burst
        
        completion[task_index] = max(end_time, completion[task_index])
    
    for i, task in enumerate(tasks):
        pid, arrival, burst, _ = task
        turnaround[i] = completion[i] - arrival
        waiting[i] = turnaround[i] - burst
    
    return sum(waiting) / len(tasks)  # Average waiting time

def display_results(tasks, algorithm, execution_order):
    result_window = tk.Toplevel(root)
    result_window.title("Scheduling Results")

    pid_to_index = {task[0]: i for i, task in enumerate(tasks)}

    completion = [-1] * len(tasks)
    turnaround = [0] * len(tasks)
    waiting = [0] * len(tasks)
    
    # Calculate completion times
    for ex in execution_order:
        pid, start_time, burst = ex
        task_index = pid_to_index[pid]
        end_time = start_time + burst
        completion[task_index] = max(end_time, completion[task_index])
    
    # Calculate turnaround and waiting times
    for i, task in enumerate(tasks):
        pid, arrival, burst, _ = task
        turnaround[i] = completion[i] - arrival
        waiting[i] = turnaround[i] - burst
    
    ttk.Label(result_window, text=f"Algorithm Used: {algorithm}", font=("Arial", 12, "bold")).pack()
    tree = ttk.Treeview(result_window, columns=("PID", "Completion", "Waiting", "Turnaround"), show="headings")
    for col in ("PID", "Completion", "Waiting", "Turnaround"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    for i, task in enumerate(tasks):
        tree.insert("", tk.END, values=(task[0], completion[i], waiting[i], turnaround[i]))
    tree.pack()

    avg_completion = sum(completion) / len(completion)
    avg_waiting = sum(waiting) / len(waiting)
    avg_turnaround = sum(turnaround) / len(turnaround)
    
    ttk.Label(result_window, text=f"Average Completion Time: {avg_completion:.2f}", font=("Arial", 10)).pack()
    ttk.Label(result_window, text=f"Average Waiting Time: {avg_waiting:.2f}", font=("Arial", 10)).pack()
    ttk.Label(result_window, text=f"Average Turnaround Time: {avg_turnaround:.2f}", font=("Arial", 10)).pack()
    
    visualize_gantt_chart(tasks, execution_order)

def visualize_gantt_chart(tasks, execution_order):
    fig, ax = plt.subplots(figsize=(12, 6))

    unique_pids = set(task[0] for task in tasks)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_pids)))
    pid_to_color = {pid: colors[i % len(colors)] for i, pid in enumerate(unique_pids)}

    max_time = max(ex[1] + ex[2] for ex in execution_order)

    for t in range(0, max_time + 1, 1):
        ax.axvline(t, color='gray', linestyle='dashed', linewidth=0.5, alpha=0.3)

    process_labels = sorted(unique_pids)

    for i, ex in enumerate(execution_order):
        pid, start_time, burst = ex
        y_pos = process_labels.index(pid)
        
        ax.barh(y_pos, burst, left=start_time, 
               color=pid_to_color[pid], edgecolor='black', alpha=0.7)
        
        if burst > 1:  
            ax.text(start_time + burst/2, y_pos, str(pid), 
                   ha='center', va='center', color='black', fontweight='bold')
    
    # Set labels and title
    plt.xlabel("Time")
    plt.ylabel("Process")
    plt.yticks(range(len(process_labels)), [f"P{pid}" for pid in process_labels])
    plt.title("Gantt Chart")
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("CPU Scheduling Simulator")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Process ID").grid(row=0, column=0)
ttk.Label(frame, text="Arrival Time").grid(row=0, column=1)
ttk.Label(frame, text="Burst Time").grid(row=0, column=2)
ttk.Label(frame, text="Priority").grid(row=0, column=3)

entry_pid = ttk.Entry(frame, width=5)
entry_arrival = ttk.Entry(frame, width=5)
entry_burst = ttk.Entry(frame, width=5)
entry_priority = ttk.Entry(frame, width=5)
entry_quantum = ttk.Entry(frame, width=5)

entry_pid.grid(row=1, column=0)
entry_arrival.grid(row=1, column=1)
entry_burst.grid(row=1, column=2)
entry_priority.grid(row=1, column=3)

def on_enter_pressed(event):
    widget = event.widget
    if widget == entry_pid:
        entry_arrival.focus()
    elif widget == entry_arrival:
        entry_burst.focus()
    elif widget == entry_burst:
        entry_priority.focus()
    elif widget == entry_priority or widget == add_task_button:
        add_task()
    return "break" 

entry_pid.bind("<Return>", on_enter_pressed)
entry_arrival.bind("<Return>", on_enter_pressed)
entry_burst.bind("<Return>", on_enter_pressed)
entry_priority.bind("<Return>", on_enter_pressed)

add_task_button = ttk.Button(frame, text="Add Task", command=add_task)
add_task_button.grid(row=1, column=4)
add_task_button.bind("<Return>", on_enter_pressed)

clear_button = ttk.Button(frame, text="Clear", command=clear_input_fields)
clear_button.grid(row=1, column=5)

quantum_label = ttk.Label(frame, text="Time Quantum:")
quantum_label.grid(row=4, column=0)
entry_quantum.grid(row=4, column=1)
quantum_label.grid_remove()
entry_quantum.grid_remove()

task_table = ttk.Treeview(frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
for col in ("PID", "Arrival", "Burst", "Priority"):
    task_table.heading(col, text=col)
    task_table.column(col, width=100)

task_table.grid(row=2, column=0, columnspan=6)

def toggle_quantum_entry(event):
    if algo_choice.get() == "Round Robin":
        quantum_label.grid()
        entry_quantum.grid()
    else:
        quantum_label.grid_remove()
        entry_quantum.grid_remove()

def auto_select_algorithm(tasks):
    """Automatically select the best scheduling algorithm based on task characteristics."""
    if all(task[1] == tasks[0][1] for task in tasks): 
        return "Shortest Process Next"
    elif any(task[3] != 0 for task in tasks):  
        return "Priority Scheduling"
    elif len(set(task[2] for task in tasks)) > 3:
        return "Round Robin"
    else:
        return "First Come First Served (FCFS)"


algo_choice = ttk.Combobox(frame, values=["Auto Select", "First Come First Served (FCFS)", "Round Robin", "Shortest Process Next", "Shortest Remaining Time Next", "Priority Scheduling"])
algo_choice.grid(row=3, column=1)
algo_choice.set("Auto Select")
algo_choice.bind("<<ComboboxSelected>>", toggle_quantum_entry)

clear_tasks_button = ttk.Button(frame, text="Clear Tasks", command=clear_tasks)
clear_tasks_button.grid(row=3, column=3)

ttk.Button(frame, text="Run Scheduling", command=calculate_schedule).grid(row=3, column=2)

root.mainloop()