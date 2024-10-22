from pulp import *

#Task dictionary and length
tasks_best = {'A':[4], 'B':[80], 'C':[30], 'D1':[30], 
              'D2':[30], 'D3':[30],'D4':[160], 'D5':[60], 
              'D6':[30], 'D7':[30], 'D8':[8], 'E':[80],
              'F':[40], 'G':[20], 'H':[30]}

tasks_exp = {'A':[8], 'B':[120], 'C':[40], 'D1':[40], 
             'D2':[40], 'D3':[40],'D4':[200], 'D5':[80], 
             'D6':[40], 'D7':[40], 'D8':[16], 'E':[120],
             'F':[80], 'G':[40], 'H':[40]}

tasks_worst = {'A':[16], 'B':[200], 'C':[80], 'D1':[60], 
               'D2':[60], 'D3':[60],'D4':[280], 'D5':[100], 
               'D6':[60], 'D7':[60], 'D8':[24], 'E':[160],
               'F':[120], 'G':[80], 'H':[80]}

#Task list
tasks_list = list(tasks_best.keys())

#Predecessor dictionary
predecessors = {'A':[], 'B':[], 'C':['A'], 'D1':['A'], 'D2':['D1'],
               'D3':['D1'], 'D4':['D2', 'D3'], 'D5':['D4'], 'D6':['D4'],
               'D7':['D6'], 'D8':['D5', 'D7'], 'E':['B', 'C'],
               'F':['D8', 'E'], 'G':['A', 'D8'], 'H':['F', 'G']}

#Create LP problem
prob_best = LpProblem("Critical Path", LpMinimize)
prob_exp = LpProblem("Critical Path", LpMinimize)
prob_worst = LpProblem("Critical Path", LpMinimize)


#Create LP variables
start_times_best = {task: LpVariable(f"start_{task}", 0, None) for task in tasks_list}
end_times_best = {task:  LpVariable(f"end_{task}", 0,None) for task in tasks_list}

start_times_exp = {task: LpVariable(f"start_{task}", 0, None) for task in tasks_list}
end_times_exp = {task:  LpVariable(f"end_{task}", 0,None) for task in tasks_list}

start_times_worst = {task: LpVariable(f"start_{task}", 0, None) for task in tasks_list}
end_times_worst = {task:  LpVariable(f"end_{task}", 0,None) for task in tasks_list}

#Add constraints
for task in tasks_list:
    prob_best += end_times_best[task] == start_times_best[task] + tasks_best[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_best += start_times_best[task] >= end_times_best[predecessor], f"{task}_predecessor_{predecessor}"

for task in tasks_list:
    prob_exp += end_times_exp[task] == start_times_exp[task] + tasks_exp[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_exp += start_times_exp[task] >= end_times_exp[predecessor], f"{task}_predecessor_{predecessor}"

for task in tasks_list:
    prob_worst += end_times_worst[task] == start_times_worst[task] + tasks_worst[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_worst += start_times_worst[task] >= end_times_worst[predecessor], f"{task}_predecessor_{predecessor}"

#Set objective function
prob_best += lpSum([end_times_best[task] for task in tasks_list]), "minimize_end_times"
prob_exp += lpSum([end_times_exp[task] for task in tasks_list]), "minimize_end_times"
prob_worst += lpSum([end_times_worst[task] for task in tasks_list]), "minimize_end_times"

#Solve LP problem
status_best = prob_best.solve()
status_best = prob_exp.solve()
status_best = prob_worst.solve()

#Print results
print("\nCritical Path time for best scenario:")
for task in tasks_list:
    if value(start_times_best[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_best[task]) == max([value(end_times_best[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_best[task])} hours in duration")

print("\nCritical Path time for expected scenario:")
for task in tasks_list:
    if value(start_times_exp[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_exp[task]) == max([value(end_times_exp[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_exp[task])} hours in duration")

print("\nCritical Path time for worst scenario:")
for task in tasks_list:
    if value(start_times_worst[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_worst[task]) == max([value(end_times_worst[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_worst[task])} hours in duration")



#Print solution
print("\nSolution variable values for best scenario:")
for var in prob_best.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

print("\nSolution variable values for expeccted scenario:")
for var in prob_exp.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

print("\nSolution variable values for worst scenario:")
for var in prob_worst.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)
        




