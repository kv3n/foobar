class Solution(object):
    def monotoneIncreasingDigits(self, N):
        split_n = str(N)
        num_digits = len(split_n)

        first_dec_index = -1
        repeat = -1
        for digit in range(1, num_digits):
            if split_n[digit] < split_n[digit - 1]:
                first_dec_index = digit - 1
                break
            elif repeat < 0 and split_n[digit] == split_n[digit - 1]:
                repeat = digit - 1
            elif repeat >= 0 and split_n[digit] > split_n[digit - 1]:
                repeat = -1

        if repeat >= 0 and first_dec_index >= 0:
            first_dec_index = repeat

        if first_dec_index < 0:
            return N
        else:
            new_num = 0
            for digit in range(0, num_digits):
                digit_val = int(split_n[digit])
                if digit == first_dec_index:
                    digit_val -= 1
                elif digit > first_dec_index:
                    digit_val = 9
                new_num = new_num * 10 + int(digit_val)

            return new_num





solution = Solution()
print(solution.monotoneIncreasingDigits(123))
print(solution.monotoneIncreasingDigits(421))
print(solution.monotoneIncreasingDigits(233))
print(solution.monotoneIncreasingDigits(322))
print(solution.monotoneIncreasingDigits(3322))
print(solution.monotoneIncreasingDigits(122441))
