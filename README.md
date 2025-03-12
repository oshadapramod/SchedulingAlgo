# CPU Scheduling Simulator

## Overview
This project is a CPU Scheduling Simulator that implements various scheduling algorithms. It provides a graphical user interface (GUI) using Tkinter and visualizes the scheduling process with Gantt charts.

## Features
- Supports multiple scheduling algorithms:
  - First Come First Served (FCFS)
  - Round Robin (RR)
  - Shortest Process Next (SPN)
  - Shortest Remaining Time Next (SRTN)
  - Priority Scheduling
- Automatic selection of the best algorithm based on task characteristics.
- Interactive GUI to add tasks and visualize scheduling results.
- Displays completion time, turnaround time, and waiting time for processes.
- Gantt chart visualization for better understanding of scheduling order.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/cpu-scheduler.git
   cd cpu-scheduler
   ```
2. Install the required dependencies:
   ```sh
   pip install matplotlib numpy
   ```

## Usage
1. Run the script:
   ```sh
   python scheduler.py
   ```
2. Enter process details (Process ID, Arrival Time, Burst Time, Priority) in the GUI.
3. Select a scheduling algorithm or use "Auto Select" for automatic algorithm selection.
4. Click on "Run Scheduling" to execute the algorithm and visualize results.
5. View the calculated completion time, waiting time, turnaround time, and Gantt chart.

## How It Works
- The user inputs processes with arrival time, burst time, and priority.
- The selected scheduling algorithm is applied to determine the execution order.
- The GUI displays the execution results, including:
  - Completion time
  - Waiting time
  - Turnaround time
  - Gantt chart visualization

## Algorithms Explained
- **First Come First Served (FCFS)**: Processes are executed in the order of arrival.
- **Round Robin (RR)**: Each process gets a fixed time slice (quantum) in a cyclic order.
- **Shortest Process Next (SPN)**: The process with the shortest burst time is executed first.
- **Shortest Remaining Time Next (SRTN)**: A preemptive version of SPN, where the process with the shortest remaining burst time executes.
- **Priority Scheduling**: Processes are executed based on priority, where a lower priority number represents a higher priority.

## Contributors
- Oshada Pramod (@oshadapramod)
- Kavindu Ishara (@kavinduishara)

## License
This project is licensed under the MIT License.

