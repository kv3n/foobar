import sys
from time import sleep

def get_gcd(x, y):
    while (y):
        x, y = y, x % y

    return x


def is_power_of_2(x):
    has_one_bit_occurred = False

    while x != 0:
        if 1 == x & 1:
            if has_one_bit_occurred == True:
                return False

            has_one_bit_occurred = True
        x = x >> 1

    return True


def matchup_compatible(num_player_one_bananas, num_player_two_bananas):
    is_matchup_compatible = False
    total_bananas_at_play = num_player_one_bananas + num_player_two_bananas
    possible_convergence_spot = int(total_bananas_at_play / 2)

    # If both guards have same number of bananas then we can't match them up
    if num_player_one_bananas == num_player_two_bananas:
        is_matchup_compatible = False

    # This case can happen if
    #     one guard has odd number of bananas and other has even number of bananas
    # if total bananas is odd, then the game will last for ever
    elif total_bananas_at_play % 2 == 1:
        is_matchup_compatible = True

    # This case can happen if
    #     total number of bananas is even but the convergence point is odd.
    # Essentially after 1 iteration we are only left with an even-even case
    # And an even-even case can never converge to an odd=odd scenario
    elif possible_convergence_spot % 2 == 1:
        is_matchup_compatible = True

    # This case can happen if
    #     1. if both guards have even number of bananas
    #     2. if both guards have odd number of bananas
    else:
        # if both guards have odd number of bananas, run the iteration once, so that we end up with an even-even case
        if num_player_one_bananas % 2 != 0:
            if num_player_one_bananas > num_player_two_bananas:
                num_player_one_bananas = num_player_one_bananas - num_player_two_bananas
                num_player_two_bananas = num_player_two_bananas + num_player_two_bananas
            else:
                num_player_two_bananas = num_player_two_bananas - num_player_one_bananas
                num_player_one_bananas = num_player_one_bananas + num_player_one_bananas

        greatest_common_divisor = get_gcd(num_player_one_bananas, num_player_two_bananas)

        if possible_convergence_spot % greatest_common_divisor != 0:
            # If the greatest common divisor can't form the convergence spot then we will loop forever
            is_matchup_compatible = True
        else:
            # If the greatest common divisor is a power of 2 then matchup is compatible
            is_matchup_compatible = not is_power_of_2(possible_convergence_spot / greatest_common_divisor)

    return is_matchup_compatible


def thumb_wrestling_sim(num_a, num_b):
    pattern_dict = dict()
    is_infinite = False
    real_a = num_a
    real_b = num_b
    while num_a != num_b:
        pattern1 = str(num_a) + '-' + str(num_b)
        pattern2 = str(num_b) + '-' + str(num_a)
        if pattern1 in pattern_dict or pattern2 in pattern_dict:
            is_infinite = True
            break
        else:
            pattern_dict[pattern1] = True
            pattern_dict[pattern2] = True
            if num_a > num_b:
                num_a = num_a - num_b
                num_b = num_b + num_b
            else:
                num_b = num_b - num_a
                num_a = num_a + num_a

    #if is_infinite == False:
    #print(str(real_a) + ' + ' + str(real_b) + ' = ' + str((real_a + real_b)) + ', ' + str((real_a + real_b) / 2) + ', ' + str(get_gcd(real_a, real_b)) + ' -> ' + str(is_infinite))

    return is_infinite


import random

def get_random_with_sum(sum):
    num_a = random.randint(2, sum - 2)
    num_b = sum - num_a

    if num_a % 2 != 0:
        num_a -= 1
        num_b += 1

    return num_a, num_b


#for itr in range(0, 20):
    #num_a, num_b = get_random_with_sum(40)


"""
sum = 96
for num_a in range(2, sum / 2, 2):
    num_b = sum - num_a
    #print(matchup_compatible(num_a, num_b))
    thumb_wrestling_sim(num_a, num_b)
"""


"""
for sum in range(5, 100):
    if sum == 8 or sum == 16 or sum == 32 or sum == 64:
        continue

    for itr in range(0, 10):
        num_a, num_b = get_random_with_sum(sum)
        if num_a != num_b:
            thumb_wrestling_event(num_a, num_b)
"""

"""
thumb_wrestling_event(18, 54)
num_a, num_b = get_random_with_sum(72)
thumb_wrestling_event(num_a, num_b)
num_a, num_b = get_random_with_sum(72)
thumb_wrestling_event(num_a, num_b)
num_a, num_b = get_random_with_sum(72)
thumb_wrestling_event(num_a, num_b)
num_a, num_b = get_random_with_sum(72)
thumb_wrestling_event(num_a, num_b)
"""

"""
#thumb_wrestling_event(18, 54)
found_false = False
iteration_count = 0
while not found_false:
    num_a = random.randint(1, 10000000)
    num_b = random.randint(1, 10000000)

    if num_a % 2 == 1:
        num_a += 1

    if num_b % 2 == 1:
        num_b += 1

    is_simulated_true = thumb_wrestling_sim(num_a, num_b)
    is_actual_true = matchup_compatible(num_a, num_b)

    if is_simulated_true != is_actual_true:
        print('Fail at: ' + str(num_a) + ', ' + str(num_b))

        found_false = True
        break

    iteration_count += 1
    print(iteration_count)

    if iteration_count >= 10 ** 3:
        break

print('Ran ' + str(iteration_count) + ' iterations')
print('Found false = ' + str(found_false))
"""


num_a = 1
num_b = 255
is_simulated_true = thumb_wrestling_sim(num_a, num_b)
print(is_simulated_true)
is_actual_true = matchup_compatible(num_a, num_b)
print(is_actual_true)

"""
#num_a = 27744
#num_b = 31104

num_a = 5752
num_b = 158748
is_actual_true = matchup_compatible(num_a, num_b)
print('\t' + str(is_actual_true))
is_simulated_true = thumb_wrestling_sim(num_a, num_b)
print('\t' + str(is_simulated_true))
"""

"""
1: 84164, 42968
	False
	True
2: 194760, 29458
	True
	True
3: 129146, 147688
	True
	True
4: 140894, 24594
checking power
	True
	True
5: 142164, 24534
	True
	True
6: 5752, 158748
	False
	True
7: 14654, 66514
checking power
	True
	True
8: 78704, 66728
	False
	True
9: 153608, 82336
	False
	True
10: 19926, 111882
checking power
	True
	True
11: 23064, 59564
	False
	True
12: 51656, 95532
	False
	True
13: 60450, 140408
	True
	True
14: 172748, 11690
	True
	True
15: 161804, 165328
	False
	True
16: 153764, 95556
checking power
	True
	True
17: 53322, 171230
checking power
	True
	True
18: 92758, 135954
checking power
	True
	True
19: 19602, 46134
checking power
	True
	True
20: 193602, 193004
	True
	True
"""