import aocread


class Shift:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.guardid = 0
        self.type = 0  # Start / Sleep / WakeUp
        self.friendlytype = 'START'

    def stamp(self, in_str):
        close_index = in_str.find(']')
        datetime_str = in_str[:close_index].lstrip('[')
        shift_detail = in_str[close_index+2:]

        date_str = datetime_str.split(' ')[0]
        time_str = datetime_str.split(' ')[1]

        self.year = int(date_str.split('-')[0])
        self.month = int(date_str.split('-')[1])
        self.day = int(date_str.split('-')[2])

        self.hour = int(time_str.split(':')[0])
        self.minute = int(time_str.split(':')[1])

        if 'asleep' in shift_detail:
            self.type = 1
            self.friendlytype = 'ASLEEP'
        elif 'wakes' in shift_detail:
            self.type = 2
            self.friendlytype = 'AWAKE'
        else:
            self.guardid = int(shift_detail.split(' ')[1].lstrip('#'))

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year

        if self.month != other.month:
            return self.month < other.month

        if self.day != other.day:
            return self.day < other.day

        if self.hour != other.hour:
            return self.hour < other.hour

        return self.minute < other.minute

    def __repr__(self):
        return '[{}-{}-{} {}:{}] {} -> {}\n'.format(self.year, self.month, self.day,
                                                  self.hour, self.minute,
                                                  self.guardid, self.friendlytype)


class Guard:
    def __init__(self):
        self.schedule = [0] * 60
        self.time_slept = 0

    def stamp_sleep_time(self, start, end):
        for minute in xrange(start, end):
            self.schedule[minute] += 1

        self.time_slept += (end - start)

    def __gt__(self, other):
        return self.time_slept > other.time_slept


time_logs = aocread.read_file('input04')
parsed_logs = []
guards = dict()

for time_log in time_logs:
    parsed_log = Shift()
    parsed_log.stamp(time_log)

    if parsed_log.guardid != 0 and parsed_log.guardid not in guards:
        guards[parsed_log.guardid] = Guard()

    parsed_logs.append(parsed_log)

parsed_logs.sort()

num_logs = len(parsed_logs)
for log_id in xrange(num_logs):
    if parsed_logs[log_id].type == 0:
        continue
    else:
        parsed_logs[log_id].guardid = parsed_logs[log_id - 1].guardid

    if parsed_logs[log_id].type == 1:
        guards[parsed_logs[log_id].guardid].stamp_sleep_time(parsed_logs[log_id].minute,
                                                             parsed_logs[log_id + 1].minute)


max_guard_id = -1
max_guard_sleep = -1
max_minute = -1
for id, guard in guards.items():
    if guard.time_slept > max_guard_sleep:
        max_guard_id = id
        max_guard_sleep = guard.time_slept
        max_minute = guard.schedule.index(max(guard.schedule))

print('{} for {} minutes with max at {}'.format(max_guard_id, max_guard_sleep, max_minute))
print(max_guard_id * max_minute)

max_guard_id = -1
max_sleep_minute = -1
max_sleep_frequency = -1
for id, guard in guards.items():
    max_guard_sleep_frequency = max(guard.schedule)
    if max_guard_sleep_frequency > max_sleep_frequency:
        max_guard_id = id
        max_sleep_minute = guard.schedule.index(max_guard_sleep_frequency)
        max_sleep_frequency = max_guard_sleep_frequency

print('{} for {} times at minute {}'.format(max_guard_id, max_sleep_frequency, max_sleep_minute))
print(max_guard_id * max_sleep_minute)
