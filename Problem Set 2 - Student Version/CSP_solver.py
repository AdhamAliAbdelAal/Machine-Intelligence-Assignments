from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # get all binary constraints that involve the assigned variable
    binary_constraints = [constraint for constraint in problem.constraints if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables]

    for constraint in binary_constraints:
        # get the other involved variable
        other_variable = constraint.get_other(assigned_variable)
        # if the other variable has no domain, skip this constraint
        if other_variable not in domains:
            continue
        # update the other variable's domain 
        # temp_set is the set of values that do not satisfy the constraint
        temp_set = set()
        for value in domains[other_variable]:
            # get the value of the first variable in the constraint
            first_value = assigned_value if assigned_variable == constraint.variables[0] else value
            # get the value of the second variable in the constraint
            second_value = assigned_value if assigned_variable == constraint.variables[1] else value
            # if the value does not satisfy the constraint, add it to the temp_set
            if not constraint.condition(first_value, second_value):
                temp_set.add(value)
        # remove the values in the temp_set from the other variable's domain
        domains[other_variable] -= temp_set
        # if any variable's domain becomes empty, return False
        if len(domains[other_variable]) == 0:
            return False
    return True
    


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
import copy
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    # get all binary constraints that involve the assigned variable
    binary_constraints = [constraint for constraint in problem.constraints if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables]
    # sort the values in the variable's domain based on the least restraining value heuristic
    def sort_key(assigned_value):
        # neighbors is the set of variables that are involved in the binary constraints with the assigned variable
        neighbors = set()      
        # make a copy of the domains
        domains_copy = copy.deepcopy(domains)
        for constraint in binary_constraints:
            # get the other involved variable
            other_variable = constraint.get_other(variable_to_assign)
            # if the other variable has no domain, skip this constraint
            if other_variable not in domains_copy:
                continue
            neighbors.add(other_variable)
            # update the other variable's domain
            temp = set()
            for value in domains_copy[other_variable]:
                first_value = assigned_value if variable_to_assign == constraint.variables[0] else value
                second_value = assigned_value if variable_to_assign == constraint.variables[1] else value
                if not constraint.condition(first_value, second_value):
                    temp.add(value)
            # remove the values in the temp_set from the other variable's domain
            domains_copy[other_variable] -= temp
        # count is the number of values in the neighbors' domains
        count = 0
        for neighbor in neighbors:
            count += len(domains_copy[neighbor])
        # return the count and the negative of the assigned value to sort the values in ascending order if they have the same count
        return (count, -assigned_value)
    return sorted(list(domains[variable_to_assign]), key=sort_key, reverse=True)


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    unary_constraints = [constraint for constraint in problem.constraints if isinstance(constraint, UnaryConstraint)]
    domains = copy.deepcopy(problem.domains)
    # 1-Consistency
    for constraint in unary_constraints:
        variable = constraint.variable
        domains[variable] = {value for value in domains[variable] if constraint.condition(value)}
        if not domains[variable]:
            return None
    # backtracking search with forward checking
    assignment = {}
    ret = backtracking_search(problem, assignment, domains)
    return ret

def backtracking_search(problem: Problem, assignment: Assignment, domains: Dict[str,set]) -> Optional[Assignment]:
    # if the assignment is complete, return it
    if problem.is_complete(assignment):
        return assignment
    # get the variable that should be picked based on the MRV heuristic
    variable = minimum_remaining_values(problem, domains)
    # get the values of the variable based on the least restraining value heuristic
    values = least_restraining_values(problem, variable, domains)
    # make a copy of the domains
    domains_copy = copy.deepcopy(domains)
    for value in values:
        domains = copy.deepcopy(domains_copy)
        # remove the variable from the domains
        domains.pop(variable)
        # if the assignment is not consistent, skip this value
        if forward_checking(problem, variable, value, domains):
            # add the variable and its value to the assignment
            assignment[variable] = value
            # get the result of backtracking search
            result = backtracking_search(problem, assignment, domains)
            # if the result is not None, return it
            if result is not None:
                return result
            # remove the variable from the assignment
            assignment.pop(variable)
    return None