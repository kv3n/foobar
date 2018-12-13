import aocread

data = aocread.read_file('input12')
initial_state = data[0].split(':')[1].lstrip().rstrip('\n')
initial_state = initial_state.replace('.', '0').replace('#', '1')

config = dict()
for config_str in data[2:]:
    config_str = config_str.rstrip('\n').replace('.', '0').replace('#', '1')
    config_key = int(config_str.split(' ')[0], 2)
    config_result = int(config_str.split(' ')[2], 2)
    config[config_key] = config_result


num_generations = 0
pattern_length = 5
cur_state = initial_state
origin_loc = 0
num_stable_generations = 0
prev_num_plants = 0
threshold = 50000000000
while num_generations < threshold:
    cur_state = '0' * pattern_length + cur_state + '0' * pattern_length
    origin_loc += (pattern_length - pattern_length // 2)

    evolved_state = ''
    sum_of_plants = 0
    num_plants = 0
    for start_index in xrange(len(cur_state) - pattern_length + 1):
        batch_config_str = cur_state[start_index:start_index+pattern_length]
        batch_config = int(batch_config_str, 2)
        if batch_config in config:
            evolution = config[batch_config]
        else:
            evolution = 0
        num_plants += evolution
        sum_of_plants += evolution * (start_index - origin_loc)
        evolved_state += str(evolution)

    evolved_state_stripped = evolved_state.lstrip('0')
    change_in_origin = len(evolved_state) - len(evolved_state_stripped)
    origin_loc -= change_in_origin

    evolved_state = evolved_state_stripped.rstrip('0')
    cur_state = evolved_state

    if prev_num_plants == num_plants:
        num_stable_generations += 1
    else:
        num_stable_generations = 0
    prev_num_plants = num_plants

    num_generations += 1

    if num_stable_generations > 10:
        skip_generations = (threshold - num_generations)
        origin_loc -= skip_generations
        num_generations += skip_generations
        num_stable_generations = 0
        sum_of_plants = sum_of_plants + skip_generations * num_plants

    print('{:11d}: {} = {}, {}, {}'.format(num_generations, cur_state, sum_of_plants, num_plants, origin_loc))


