import aocread

instructions = aocread.read_file('input07')

dependency_graph_in = dict()

for instruction in instructions:
    instruction_split = instruction.split(' ')
    pre_req_step = instruction_split[1]
    step = instruction_split[7]

    if pre_req_step not in dependency_graph_in:
        dependency_graph_in[pre_req_step] = []

    if step not in dependency_graph_in:
        dependency_graph_in[step] = []

    dependency_graph_in[step].append(pre_req_step)


def execute_step(step):
    dependency_graph_in.pop(step)

    for key, value in dependency_graph_in.items():
        if step in value:
            value.remove(step)


def fetch_step():
    step = None
    for key, value in dependency_graph_in.items():
        if len(value) == 0:
            if step is None:
                step = key
            elif key < step:
                step = key

    return step


execution_order = ''
while True:
    step = fetch_step()
    if step is None:
        break

    execution_order += step

    execute_step(step)

print(execution_order)
