'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
from heapq import heappop, heappush

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
#Assume that process_list is sorted by arrive_time
def RR_scheduling(process_list, time_quantum ):
    schedule = []
    max_arrival_time = max(map(lambda p: p.arrive_time, process_list))
    process_arrivals = [None] * (max_arrival_time + 1)
    q = []
    remaining_bursts = {}
    arrival_times = {}
    for process in process_list:
        arrival_times[process] = process.arrive_time
        remaining_bursts[process] = process.burst_time
        process_arrivals[process.arrive_time] = process
    current_time = process_list[0].arrive_time
    done = False
    current_process = None
    remaining_quantum = -1
    remaining_burst = -1
    waiting_time = 0
    while (not done):
        if (current_time < len(process_arrivals)):
            if (process_arrivals[current_time] != None):
                q.append(process_arrivals[current_time])
        if (not current_process):
            if (len(q) <= 0):
                if (current_time >= len(process_arrivals)):
                    done = True
                    break
                else:
                    current_time += 1
                    continue
            else:
                current_process = q.pop(0)
                remaining_quantum = time_quantum
                remaining_burst = remaining_bursts[current_process]
                if (len(schedule) == 0 or current_process.id != schedule[-1][1]):
                    schedule.append((current_time, current_process.id))
        current_time += 1
        remaining_burst -= 1
        remaining_quantum -= 1
        if (remaining_burst <= 0):
            remaining_burst = -1
            remaining_quantum = -1
            waiting_time += (current_time - arrival_times[current_process])
            current_process = None
        elif (remaining_quantum <= 0):
            remaining_quantum = -1
            remaining_bursts[current_process] = remaining_burst
            remaining_burst = -1
            q.append(current_process)
            current_process = None
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    schedule = []
    max_arrival_time = max(map(lambda p: p.arrive_time, process_list))
    process_arrivals = [None] * (max_arrival_time + 1)
    arrival_times = {}
    for process in process_list:
        arrival_times[process] = process.arrive_time
        process_arrivals[process.arrive_time] = process
    current_time = process_list[0].arrive_time
    done = False
    current_process = None
    remaining_burst = -1
    heap = []
    waiting_time = 0
    while (not done):
        if (current_time < len(process_arrivals)):
            if (process_arrivals[current_time] != None):
                process = process_arrivals[current_time]
                if (process.burst_time < remaining_burst):
                    heappush(heap, (remaining_burst, current_process))
                    current_process = process
                    remaining_burst = process.burst_time
                    schedule.append((current_time, process.id))
                else:
                    heappush(heap, (process.burst_time, process))
        if (current_process == None):
            if (len(heap) <= 0):
                if (current_time >= len(process_arrivals)):
                    done = True
                    break
                else:
                    current_time += 1
                    continue
            else:
                current_process_tuple = heappop(heap)
                current_process = current_process_tuple[1]
                remaining_burst = current_process_tuple[0]
                if (len(schedule) == 0 or current_process.id != schedule[-1][1]):
                    schedule.append((current_time, current_process.id))
        current_time += 1
        remaining_burst -= 1
        if (remaining_burst <= 0):
            remaining_burst = -1
            waiting_time += (current_time - arrival_times[current_process])
            current_process = None
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

