import math
import random
import pylab


class Task:
    def __init__(self, time, lampd):
        self.time_to_solve = TIME_OF_FINISHING_TASK
        self.appearing_time = time - 1 / lampd * math.log(random.random())
        self.deadline = random.randint(2, MAX_K) * self.time_to_solve
        self.time_after_break = self.appearing_time
        self.reaction = None

    def get_appeartime(self):
        return self.appearing_time

    def get_solvetime(self):
        return self.time_to_solve

    def get_deadline(self):
        return self.deadline

    def get_break_time(self):
        return self.time_after_break


def insert_in_stack(full_task):
    if len(stack) == 0 or stack[-1].get_break_time() < full_task.get_break_time():
        stack.append(full_task)
    else:
        for i in range(len(stack)):
            if full_task.get_break_time() < stack[i].get_break_time():
                stack.insert(i, full_task)
                break


lampda = 0.01
breaking_time = 0.1
TIME_OF_FINISHING_TASK = 3  # регулярний потік

lambda_list_x_for_plot = []
response_to_lambda = []
sleep_to_lambda = []
tasks_in_time = []
task_made_by_025 = []

MAX_K = 5
MODEL_TIME = 10000
AMOUNT_OF_LAMBDA = 100
for scale_lambda in range(1, AMOUNT_OF_LAMBDA+1, 1):
    lampda = 0.01 * scale_lambda
    response_time = []
    sleep = 0

    T = 0
    stack = [Task(0, lampda)]
    stack[-1].appearing_time = 0
    while T < MODEL_TIME:
        task = stack.pop(0)
        if T < task.get_break_time():
            sleep += task.get_break_time() - T
            T = task.get_break_time()

        if task.reaction is None:  # формирование след задачи
            next_task = task.get_appeartime() - 1 / lampda * math.log(random.random())
            insert_in_stack(Task(task.get_appeartime(), lampda))
            if lampda == 0.25:
                tasks_in_time.append(stack[-1].get_appeartime())

        if task.get_solvetime() > breaking_time and T - task.get_appeartime() + breaking_time < task.get_deadline():  # задача прерывеается
            task.time_to_solve = task.get_solvetime() - breaking_time
            task.time_after_break = T + breaking_time

            if task.reaction is None:  # время реакции
                task.reaction = T - task.get_appeartime()

            T += breaking_time
            insert_in_stack(task)

        elif task.get_solvetime() <= breaking_time and T - task.get_appeartime() + task.get_solvetime() < task.get_deadline():  # задача выполнится
            if lampda == 0.25:
                task_made_by_025.append(T - task.appearing_time)
            T += task.get_solvetime()
            response_time.append(task.reaction)

        elif T - task.get_break_time() < task.get_deadline():  # потеряное время из за наступления дедлайга
            T += task.get_deadline() - (T - task.get_break_time())

    lambda_list_x_for_plot.append(lampda)
    print(len(response_time))
    if len(response_time) != 0:
        response_to_lambda.append(sum([i for i in response_time]) / len(response_time))
    else:
        response_to_lambda.append(0)
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


pylab.plt.bar(tasks_in_time,[1 for i in range(len(tasks_in_time))], align='center', alpha=1)
pylab.plt.show()

pylab.plt.bar([i for i in range(len(bar_x))], bar_x, align='center', alpha=1)
pylab.plt.show()

pylab.plot(lambda_list_x_for_plot, [i/MODEL_TIME*110 for i in sleep_to_lambda])
pylab.xlabel('lambda')
pylab.ylabel('sleep time 100%')
pylab.show()

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
