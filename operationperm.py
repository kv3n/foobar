class Solution(object):
    def mul(self, a, b):
        return a * b

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def get_results(self, equation):
        equation_len = len(equation)
        if equation_len == 0:
            return []
        elif equation_len == 1:
            return equation

        results = []

        op_index = 1
        # if a * b + c, then do b + c first and then do *
        hold_op_results = self.get_results(equation[op_index+1:])
        hold_op_results = [equation[op_index](equation[op_index-1], result) for result in hold_op_results]
        results = results + hold_op_results

        # if a * b + c, then do a * b first and then do + the rest
        if equation_len > 3:
            cur_result = equation[op_index](equation[op_index-1], equation[op_index+1])
            do_op_results = self.get_results([cur_result] + equation[op_index+2:])
            results = results + do_op_results

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

