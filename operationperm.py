class Solution(object):
    def mul(self, a, b):
        return a * b

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def get_results(self, equation):
        equation_len = len(equation)
        if equation_len == 1:
            return equation

        results = []
        index = 1
        while index < equation_len:
            cur_result = equation[index](equation[index-1], equation[index+1])
            new_equation = equation[0:index-1] + [cur_result] + equation[index+2:]
            fut_results = self.get_results(new_equation)
            results = results + fut_results
            index += 2

        return results

    def parse(self, in_equation):
        operand_start = 0
        parsed_equation = []
        index = 1
        operation_mapping = {'*': self.mul, '+': self.add, '-': self.sub}
        while index < len(in_equation):
            if in_equation[index] in operation_mapping:
                parsed_equation.append(int(in_equation[operand_start:index]))
                parsed_equation.append(operation_mapping[in_equation[index]])

                operand_start = index + 1
                index = operand_start
            index += 1
        parsed_equation.append(int(in_equation[operand_start:index]))

        return parsed_equation


    def diffWaysToCompute(self, input):
        """
        :type input: str
        :rtype: List[int]
        """

        equation = self.parse(input)
        results = self.get_results(equation)

        return results



solution = Solution()
print(solution.diffWaysToCompute("2*3-4*5"))
print(solution.diffWaysToCompute("2-1-1"))

