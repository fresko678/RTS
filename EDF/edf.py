import math
import random
import pylab
"""edf"""

class Task:
    def __init__(self, time, lampd):
        self.time_to_solve = MX
        self.appearing_time = time - 1 / lampd * math.log(random.random())
        self.deadline = random.randint(2, MAX_K) * self.time_to_solve

    def get_appeartime(self):
        return self.appearing_time

    def get_solvetime(self):
        return self.time_to_solve

    def get_deadline(self):
        return self.deadline

def find_last_appeared_time(t):
    return queue[-1].get_appeartime() if len(queue) != 0 and queue[-1].get_appeartime() > t else t

def get_new_task(t):
    ret = 0

    for i in range(len(queue)):
        if queue[i].get_deadline() < queue[ret].get_deadline() and t > queue[i].get_appeartime():
            ret = i
    return queue.pop(ret)
MAX_K = 5
MX = 3
MODEL_TIME = 10000
AMOUNT_OF_LAMBDA = 100
lambda_list_x_for_plot = []
response_to_lambda = []
sleep_to_lambda = []
tasks_in_time = []
task_made_by_025 = []

for scale_lambda in range(1, AMOUNT_OF_LAMBDA+1, 1):
    lampda = 0.01 * scale_lambda

    T = 0
    queue = []
    response_time = []
    sleep = 0

    task = Task(0, lampda)
    task.appearing_time = 0.0
    while T < MODEL_TIME:
        if T < task.get_appeartime():  # простой процесора
            sleep += task.get_appeartime() - T
            T = task.get_appeartime()

        if T < task.get_appeartime() + task.get_deadline():
            if T + task.get_solvetime() < task.get_appeartime() + task.get_deadline():  # выполнился до дедлайна
                response_time.append(T - task.get_appeartime())
                if lampda == 0.25:
                    task_made_by_025.append(T - task.appearing_time)
                T += task.get_solvetime()
            else:
                T += task.get_appeartime() + task.get_deadline() - T

        while T > find_last_appeared_time(task.get_appeartime()):
            queue.append(Task(find_last_appeared_time(task.get_appeartime()), lampda))
            if lampda == 0.25:
                tasks_in_time.append(queue[-1].get_appeartime())
        task = get_new_task(T)

    lambda_list_x_for_plot.append(lampda)
    response_to_lambda.append(sum([i for i in response_time]) / len(response_time))
    sleep_to_lambda.append(sleep)

    print('\r{}%'.format(scale_lambda), end='')
    if scale_lambda == AMOUNT_OF_LAMBDA:
        print()
pylab.plot(lambda_list_x_for_plot, response_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('average response time')
pylab.show()
pylab.plot(lambda_list_x_for_plot, sleep_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('sleep time')
pylab.show()

bar_x = [0]
GROUP = 100
for i in range(len(tasks_in_time)):
    if tasks_in_time[i] < GROUP*(len(bar_x)):
        bar_x[-1] += 1
    else:
        bar_x.append(1)

pylab.plt.bar(tasks_in_time, [1 for i in range(len(tasks_in_time))], align='center', alpha=1)
pylab.plt.show()

pylab.plt.bar([i for i in range(len(bar_x))], bar_x, align='center', alpha=1)
pylab.plt.show()

task_made_by_025.sort()
tmp = [0]
for i in range(len(task_made_by_025)):
    if task_made_by_025[i] < len(tmp):
        tmp[-1] += 1
    else:
        tmp.append(0)

pylab.plot([i for i in range(len(tmp))], tmp)
pylab.xlabel('response time')
pylab.ylabel('tasks')
pylab.show()
