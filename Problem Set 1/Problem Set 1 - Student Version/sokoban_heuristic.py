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

    # get the crates, goals and walkable points
    crates = state.crates
    goals = problem.layout.goals
    walkable = problem.layout.walkable

    # get the cached values
    prev_crate = problem.cache().get("prev_crate", None)
    prev_heuristic = problem.cache().get("prev_heuristic", None)

    # if the boxes are not changed, return the cached value
    if(crates == prev_crate):
        return prev_heuristic
    
    # update the cached values
    problem.cache()["prev_crate"] = crates
    problem.cache()["prev_heuristic"] = math.inf

    # prev_heuristic is used to calculated the heuristic for the current state 
    prev_heuristic = math.inf

    # check if there is a deadlock for the current crate
    def is_deadlock(crate):
        # get all surrounding walls of the crate
        directions_walls = [False]*4
        # get all surrounding crates of the crate
        directions_crates = [False]*4

        # count number of non walkable
        cnt = 0

        for direction in Direction:

            if(crate + direction.to_vector() not in walkable):
                directions_walls[direction] = True
                cnt+=1
            
            if(crate + direction.to_vector() in crates):
                directions_crates[direction] = True

        
        # (left or right) and (up or down) are blocked
        # for the four corners
        if(directions_walls[Direction.LEFT] or directions_walls[Direction.RIGHT]) and (directions_walls[Direction.UP] or directions_walls[Direction.DOWN]):
            return True
        
        # if there are more than two surrounding walls then it is a deadlock
        if(cnt>2):
            return True
        
        # make a list of all surrounding walls or crates
        directions_all = [False]*4
        for i in range(4):
            directions_all[i] = directions_walls[i] or directions_crates[i]
        
        # check if the crate is in square deadlock of walls or crates 
        # case one the crate is the left upper corner of the square
        if(directions_all[Direction.RIGHT] and directions_all[Direction.DOWN]):
            right_down = crate + Direction.RIGHT.to_vector() + Direction.DOWN.to_vector()
            if(right_down not in walkable):
                return True
            if(right_down in crates):
                return True
            
        # case two the crate is the right upper corner of the square
        if(directions_all[Direction.LEFT] and directions_all[Direction.DOWN]):
            left_down = crate + Direction.LEFT.to_vector() + Direction.DOWN.to_vector()
            if(left_down not in walkable):
                return True
            if(left_down in crates):
                return True
            
        # case three the crate is the left down corner of the square
        if(directions_all[Direction.RIGHT] and directions_all[Direction.UP]):
            right_up = crate + Direction.RIGHT.to_vector() + Direction.UP.to_vector()
            if(right_up not in walkable):
                return True
            if(right_up in crates):
                return True
            
        # case four the crate is the right down corner of the square
        if(directions_all[Direction.LEFT] and directions_all[Direction.UP]):
            left_up = crate + Direction.LEFT.to_vector() + Direction.UP.to_vector()
            if(left_up not in walkable):
                return True
            if(left_up in crates):
                return True
            
        # crate against the goal

        #get the nearest goal
        goal = None
        for it_goal in goals:
            if(it_goal in crates):
                continue
            if(goal is None or manhattan_distance(it_goal,crate)<manhattan_distance(goal,crate)):
                goal = it_goal
        # if the crate stuck in the far left and the goal is in the right
        if(crate.x==1 and goal.x>1):
            return True
        # if the crate stuck in the far right and the goal is in the left
        if(crate.x==problem.layout.width-2 and goal.x<problem.layout.width-2):
            return True
        # if the crate stuck in the far up and the goal is in the down
        if(crate.y==1 and goal.y>1):   
            return True
        # if the crate stuck in the far down and the goal is in the up
        if(crate.y==problem.layout.height-2 and goal.y<problem.layout.height-2):
            return True
        return False        
    
    # check if there are deadlocks
    for crate in crates:
        if(crate in goals):
            continue
        if(is_deadlock(crate)):
            return math.inf
    
    # the second part of the heuristic if there are no deadlocks
    # get the unassigned crates
    unassigned_crates = crates.difference(goals)
    sum = 0
    # get the sum of the distance between the unassigned crates and the nearest goal
    for crate in unassigned_crates:
        # get the distance to the nearest goal
        min_distance = math.inf
        for goal in goals:
            distance = manhattan_distance(crate, goal)
            if(distance < min_distance):
                min_distance = distance
        sum += min_distance
    prev_heuristic = sum
    problem.cache()["prev_heuristic"] = prev_heuristic
    return sum