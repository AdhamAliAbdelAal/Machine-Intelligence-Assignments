from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint


# TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i + 1).upper() for i in range(3)]
        # print(LHS0, LHS1, RHS)

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        # set to all variables
        problem.variables = list(set(LHS0 + LHS1 + RHS))
        problem.constraints = []
        problem.domains = {}

        # set binary constraints
        # each letter should be different
        for i in range(len(problem.variables)):
            for j in range(i + 1, len(problem.variables)):
                problem.constraints.append(
                    BinaryConstraint((problem.variables[i], problem.variables[j]), lambda x, y: x != y))

        # set unary constraints
        # first letter of each word should not be 0
        for word in [LHS0, LHS1, RHS]:
            problem.constraints.append(UnaryConstraint(word[0], lambda x: x != 0))

        # set domains
        for var in problem.variables:
            problem.domains[var] = set(range(10))

        print(f'{LHS0} + {LHS1} = {RHS}')

        # reverse each string
        LHS0 = LHS0[::-1]
        LHS1 = LHS1[::-1]
        RHS = RHS[::-1]
        min_len = min(len(LHS0), len(LHS1))

        def generate_summation_with_carry(var1, var2, result, c1, i):
            # a + b + c1 = d + c2 
            # a, b, d in [0, 9] and c1, c2 in [0, 1] 
            # add c2 to the problem
            c2 = f"c{i}"
            problem.variables.append(c2)
            problem.domains[c2] = set(range(2))
            # a + b = t1 (concatenate a and b) domain: [0, 99]
            # add t1 to the problem
            t1 = f"t1{i}"
            problem.variables.append(t1)
            problem.domains[t1] = set(range(100))

            def condition_a_t1(a_val, t1_val):
                return a_val == t1_val % 10

            def condition_b_t1(b_val, t1_val):
                return b_val == t1_val // 10

            problem.constraints.append(BinaryConstraint((var1, t1), condition_a_t1))
            problem.constraints.append(BinaryConstraint((var2, t1), condition_b_t1))
            # t1 + c1 = t2 (concatenate c1 and t1) domain: [0, 199]
            # add t2 to the problem
            t2 = f"t2{i}"
            problem.variables.append(t2)
            problem.domains[t2] = set(range(200))

            def condition_t1_t2(t1_val, t2_val):
                return t1_val == t2_val % 100

            def condition_c1_t2(c1_val, t2_val):
                return c1_val == t2_val // 100

            problem.constraints.append(BinaryConstraint((t1, t2), condition_t1_t2))
            problem.constraints.append(BinaryConstraint((c1, t2), condition_c1_t2))

            # t2 = d + c2
            def condition_t2_result(t2_val, result_val):
                return sum([int(digit) for digit in str(t2_val)]) % 10 == result_val

            def condition_t2_c2(t2_val, c2_val):
                return sum([int(digit) for digit in str(t2_val)]) // 10 == c2_val

            problem.constraints.append(BinaryConstraint((t2, result), condition_t2_result))
            problem.constraints.append(BinaryConstraint((t2, c2), condition_t2_c2))

            # print(f'{var1} + {var2} + {c1} = {result} + {c2}')
            # print(f'{t1} = ({var1} , {var2})')
            # print(f'{t2} = ({c1} , {t1})')

        def sum_var_and_carry(var, c1, result, i):
            # a + c1 = x1 + c2 (concatenate a and c1) domain: [0, 19]
            # add c2 to the problem
            c2 = f"c{i}"
            problem.variables.append(c2)
            problem.domains[c2] = set(range(2))
            # add x1 to the problem
            x1 = f"x1{i}"
            problem.variables.append(x1)
            problem.domains[x1] = set(range(20))

            def condition_a_x1(a_val, x1_val):
                return a_val == x1_val % 10

            def condition_c1_x1(c1_val, x1_val):
                return c1_val == x1_val // 10

            problem.constraints.append(BinaryConstraint((var, x1), condition_a_x1))
            problem.constraints.append(BinaryConstraint((c1, x1), condition_c1_x1))

            # x1 = result
            def condition_x1_result(x1_val, result_val):
                return sum([int(digit) for digit in str(x1_val)]) % 10 == result_val

            def condition_x1_c2(x1_val, c2_val):
                return sum([int(digit) for digit in str(x1_val)]) // 10 == c2_val

            problem.constraints.append(BinaryConstraint((x1, result), condition_x1_result))
            problem.constraints.append(BinaryConstraint((x1, c2), condition_x1_c2))

            # print(f'{var} + {c1} = {result} + {c2}')
            # print(f'{x1} = ({c1} , {var})')

        def equal_carry_and_result(c1, result):
            def condition_c1_result(c1_val, result_val):
                return c1_val == result_val

            problem.constraints.append(BinaryConstraint((c1, result), condition_c1_result))
            # print(f'{c1} = {result}')

        carry = "c0"
        # add c10 to the problem
        problem.variables.append(carry)
        problem.domains[carry] = set(range(1))
        # print(f'{LHS0} + {LHS1} = {RHS}')
        # sum 2 vars and carry
        for i in range(min_len):
            var1 = LHS0[i]
            var2 = LHS1[i]
            carry = f"c{i}"
            result = RHS[i]
            generate_summation_with_carry(var1, var2, result, carry, i + 1)
        # sum var and carry
        max_len = max(len(LHS0), len(LHS1))
        LSH = LHS0 if len(LHS0) > len(LHS1) else LHS1
        for i in range(min_len, max_len):
            var = LSH[i]
            carry = f"c{i}"
            result = RHS[i]
            sum_var_and_carry(var, carry, result, i + 1)

        if len(RHS) > max_len:
            carry = f"c{max_len}"
            # equal carry and result
            equal_carry_and_result(carry, RHS[max_len])
        else:
            # carry must be 0
            carry = f"c{max_len}"
            problem.constraints.append(UnaryConstraint(carry, lambda x: x == 0))

        # print(len(problem.variables))
        # print(len(problem.domains))
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
