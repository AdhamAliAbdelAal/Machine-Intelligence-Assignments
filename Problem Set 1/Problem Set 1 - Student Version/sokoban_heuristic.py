from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use
import math


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    player = state.player
    crates = state.crates
    goals = problem.layout.goals
    walkable = problem.layout.walkable
    prev_heuristic = problem.cache().get("prev_heuristic", 0)
    prev_crates = problem.cache().get("prev_crates",None)
    if(prev_crates == crates):
        return prev_heuristic
    prev_heuristic = 0
    problem.cache()["prev_crates"] = crates

    # check if there is a deadlock for the current crate
    def is_deadlock(crate, walkable):
        directions = [False]*4
        for direction in Direction:
            if(crate + direction.to_vector() not in walkable):
                directions[direction] = True
        # (left or right) and (up or down) are blocked 
        if(directions[Direction.LEFT] or directions[Direction.RIGHT]) and (directions[Direction.UP] or directions[Direction.DOWN]):
            return True
    
    # check if there are deadlocks
    for crate in crates:
        if(crate in goals):
            continue
        if(is_deadlock(crate, walkable)):
            # print("hello")

            prev_heuristic = math.inf
            problem.cache()["prev_heuristic"] = prev_heuristic
            return math.inf
    # get the unassigned crates
    unassigned_crates = crates.difference(goals)
    # print(state)
    for crate in unassigned_crates:
        # get the distance to the nearest goal
        min_distance = math.inf
        for goal in goals:
            distance = manhattan_distance(crate, goal)
            if(distance < min_distance):
                min_distance = distance
            # print(min_distance)
        prev_heuristic += min_distance
    problem.cache()["prev_heuristic"] = prev_heuristic

    # if(prev_heuristic == 4):
        # print(unassigned_crates)
    # print(prev_heuristic)
    # if(prev_heuristic == 10 or prev_heuristic==12):
    #     print(temp)
    return prev_heuristic
