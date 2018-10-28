class Solution(object):
    class Operation:
        def __init__(self, op, idx):
            self.op = op
            self.idx = idx
            self.result = 0

    def add(self, a, b):
        return b + a

    def sub(self, a, b):
        return b - a

    def mul(self, a, b):
        return b * a

    def get_result(self, permutation, operands):
        print(permutation)
        cur_operands = operands + []
        operation_stack = []
        index = 0;
        for perm in permutation:
            while index < perm[1] + 1:
                operation_stack.append(cur_operands.pop(0))
                index += 1
            result = perm[0](operation_stack.pop(), operation_stack.pop())
            operation_stack.append(result)
        print(result)


    def generate_combination(self, results, operators, start, operands):
        if start == len(operators):
            results.append(self.get_result(operators, operands))
            return

        for index in range(start, len(operators)):
            operators[index], operators[start] = operators[start], operators[index]
            self.generate_combination(results, operators, start + 1, operands)
            operators[index], operators[start] = operators[start], operators[index]


    def diffWaysToCompute(self, input):
        """
        :type input: str
        :rtype: List[int]
        """
        operand_start = 0
        operands = []
        operators = []
        index = 1
        while index < len(input):
            if input[index] == '*' or input[index] == '+' or input[index] == '-':
                if input[index] == '*':
                    operators.append((self.mul, len(operators) + 1))
                elif input[index] == '+':
                    operators.append((self.add, len(operators) + 1))
                elif input[index] == '-':
                    operators.append((self.sub, len(operators) + 1))
                operands.append(int(input[operand_start:index]))
                operand_start = index + 1
                index = operand_start

            index += 1

        results = []
        operands.append(int(input[operand_start:len(input)]))
        self.generate_combination(results, operators, 0, operands)

        print(results)
        return results

solution = Solution()
solution.diffWaysToCompute("2*3-4*5")

