class Solution(object):
    def monotoneIncreasingDigits(self, N):
        power_of_10 = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
        split_n = str(N)
        num_digits = len(split_n)

        first_dec_index = -1
        repeat = 1
        for digit in range(1, num_digits):
            if split_n[digit] < split_n[digit - 1]:
                first_dec_index = digit - repeat
                break
            elif split_n[digit] == split_n[digit - 1]:
                repeat += 1
            else:
                repeat = 1

        if first_dec_index < 0:
            return N
        else:
            first_dec_index = num_digits - first_dec_index - 1
            new_num = N - N % power_of_10[first_dec_index] - 1
            return new_num



print([10 ** x for x in range(10)])

solution = Solution()
print(solution.monotoneIncreasingDigits(123))
print(solution.monotoneIncreasingDigits(421))
print(solution.monotoneIncreasingDigits(233))
print(solution.monotoneIncreasingDigits(322))
print(solution.monotoneIncreasingDigits(3322))
print(solution.monotoneIncreasingDigits(122441))
