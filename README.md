# CPU Scheduling Simulator

## Overview
This CPU Scheduling Simulator is a graphical application that demonstrates various CPU scheduling algorithms used in operating systems. It allows users to visualize and compare different scheduling strategies through an interactive interface. This project was developed for the EC6110: Operating Systems module in the 6th semester of the Computer Engineering undergraduate program at the Faculty of Engineering, University of Jaffna.

## Features
- Implementation of multiple CPU scheduling algorithms:
  - First Come First Served (FCFS)
  - Round Robin (RR)
  - Shortest Process Next (SPN)
  - Shortest Remaining Time Next (SRTN)
  - Priority Scheduling
   
- Interactive GUI built with Tkinter
- Dynamic task entry and management
- Automatic algorithm selection based on task characteristics
- Visual representation through Gantt charts
- Performance metrics calculation (completion time, waiting time, turnaround time)
- Comparative analysis of scheduling algorithms


## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python packages:
  - tkinter
  - matplotlib
  - numpy

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cpu-scheduling-simulator.git
   cd cpu-scheduling-simulator
   ```

2. Install the required packages:
   ```
   pip install matplotlib numpy
   ```

3. Run the application:
   ```
   python scheduler.py
   ```

## Usage

### Adding Tasks
1. Enter the following parameters for each process:
   - Process ID: Unique identifier for the process
   - Arrival Time: When the process arrives in the ready queue
   - Burst Time: CPU time required by the process
   - Priority: Priority value (lower number = higher priority)

2. Click "Add Task" or press Enter to add the process to the task list

### Running Simulations
1. Select a scheduling algorithm from the dropdown menu:
   - Auto Select (automatically chooses the most appropriate algorithm)
   - First Come First Served (FCFS)
   - Round Robin (specify a time quantum)
   - Shortest Process Next
   - Shortest Remaining Time Next
   - Priority Scheduling

2. If you select Round Robin, enter a time quantum value

3. Click "Run Scheduling" to execute the simulation

### Viewing Results
- The results window displays:
  - The selected/best algorithm
  - Completion time for each process
  - Waiting time for each process
  - Turnaround time for each process
  - Average metrics for all processes
  - A Gantt chart visualization of the schedule

## Algorithm Details

### First Come First Served (FCFS)
- Non-preemptive algorithm
- Processes are executed in the order they arrive
- Simple but may result in the convoy effect

### Round Robin (RR)
- Preemptive algorithm
- Each process gets a small unit of CPU time (time quantum)
- Processes are scheduled in a circular queue

### Shortest Process Next (SPN)
- Non-preemptive algorithm
- Selects the process with the shortest burst time
- Minimizes average waiting time

### Shortest Remaining Time Next (SRTN)
- Preemptive version of SPN
- Process with the shortest remaining time is selected for execution
- May cause starvation for processes with longer burst times

### Priority Scheduling
- Can be preemptive or non-preemptive
- Each process is assigned a priority
- Lower priority number indicates higher priority

## Project Information
- **Course**: EC6110: Operating Systems
- **Institution**: Faculty of Engineering, University of Jaffna
- **Semester**: 6th Semester
- **Developers**:
  - [Oshada Pramod](https://github.com/oshadapramod)
  - [Kavindu Ishara](https://github.com/kavinduishara)

## Screenshots
![image](https://github.com/user-attachments/assets/e1c2c1a8-2fc5-4a73-9a03-5fbae84c2487)
![image](https://github.com/user-attachments/assets/cdcf85fb-6540-4aa8-923d-8321ff95ef19)
![image](https://github.com/user-attachments/assets/050d43bc-cbe9-4e35-82c2-f56031cb9aed)
![image](https://github.com/user-attachments/assets/a686c4fb-422a-4741-b905-5b7f791daf71)


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- The Faculty of Engineering, University of Jaffna, for providing the resources and environment to develop this project
