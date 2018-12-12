import aocread

instructions = aocread.read_file('input07')


class Worker:
    def __init__(self):
        self.task = ''
        self.time = 0

    def assign(self, step, time):
        self.task = step
        self.time = time

    def update(self):
        self.time -= 1
        if self.time == 0:
            return True

        return False

    def is_available(self):
        if self.task == '':
            return True
        else:
            return False


NUM_WORKERS = 5
BASE_TIME = 60
dependency_graph_in = dict()
workers = [Worker() for _ in xrange(NUM_WORKERS)]

for instruction in instructions:
    instruction_split = instruction.split(' ')
    pre_req_step = instruction_split[1]
    step = instruction_split[7]

    if pre_req_step not in dependency_graph_in:
        dependency_graph_in[pre_req_step] = []

    if step not in dependency_graph_in:
        dependency_graph_in[step] = []

    dependency_graph_in[step].append(pre_req_step)


def finish(worker):
    step = worker.task
    for key, value in dependency_graph_in.items():
        if step in value:
            value.remove(step)

    worker.task = ''


def assign(step, worker):
    def get_time_for(step):
        return BASE_TIME + ord(step) - ord('A') + 1

    dependency_graph_in.pop(step)
    worker.assign(step, get_time_for(step))


def fetch_step():
    available_steps = []
    for key, value in dependency_graph_in.items():
        if len(value) == 0 and key in dependency_graph_in:
            available_steps.append(key)

    return available_steps


execution_order = ''
time = 0
while True:
    available_steps = fetch_step()

    # Assign Tasks
    for available_step in available_steps:
        for worker in workers:
            if worker.is_available():
                assign(available_step, worker)
                break
    no_worker_update = True
    for worker in workers:
        if worker.task != '':
            if worker.update():
                finish(worker)

            no_worker_update = False

    if no_worker_update:
        break

    time += 1

print(time)
