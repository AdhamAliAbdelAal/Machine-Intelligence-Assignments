from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented



#TODO: Import any modules you want to use
from queue import Queue,PriorityQueue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    frontier: Queue[S] = Queue()
    paths : Queue[list[A]] = Queue()
    frontier.put(initial_state)
    paths.put([])
    explored = set()
    while not frontier.empty():
        state = frontier.get()
        path = paths.get()
        if state in explored:
            continue
        explored.add(state)
        actions = problem.get_actions(state)
        for action in actions:
            successor = problem.get_successor(state, action)
            new_path = list(path)
            new_path.append(action)
            if problem.is_goal(successor):
                return new_path
            if successor not in explored:
                frontier.put(successor)
                paths.put(new_path)
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    frontier: list[S] = []
    paths : list[A] = []
    frontier.append(initial_state)
    paths.append([])
    explored = set()
    while len(frontier) > 0:
        state = frontier.pop()
        path = paths.pop()
        if problem.is_goal(state):
            return path
        if state in explored:
            continue
        explored.add(state)
        actions = problem.get_actions(state)
        for action in actions:
            successor = problem.get_successor(state, action)
            new_path = list(path)
            new_path.append(action)
            if successor not in explored:
                frontier.append(successor)
                paths.append(new_path)
    return None

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    counter:int =0
    frontier: PriorityQueue[(float,int,S)] = PriorityQueue()
    paths : PriorityQueue[(float,int,list[A])] = PriorityQueue()
    frontier.put((0,counter,initial_state))
    paths.put((0,counter,[]))
    counter+=1
    explored = set()
    while not frontier.empty():
        cost,_,state = frontier.get()
        _,_,path = paths.get()
        if problem.is_goal(state):
            return path
        if state in explored:
            continue
        explored.add(state)
        actions = problem.get_actions(state)
        for action in actions:
            successor = problem.get_successor(state, action)
            new_path = list(path)
            new_path.append(action)
            if successor not in explored:
                curr_cost = problem.get_cost(state,action)
                frontier.put((cost+curr_cost,counter,successor))
                paths.put((cost+curr_cost,counter,new_path))
                counter+=1
    return None


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    counter:int =0
    frontier: PriorityQueue[(float,int,S)] = PriorityQueue()
    paths : PriorityQueue[(float,int,list[A])] = PriorityQueue()
    frontier.put((0+heuristic(problem,initial_state),counter,initial_state))
    paths.put((0+heuristic(problem,initial_state),counter,[]))
    counter+=1
    explored = set()
    while not frontier.empty():
        cost,_,state = frontier.get()
        _,_,path = paths.get()
        if problem.is_goal(state):
            return path
        if state in explored:
            continue
        explored.add(state)
        actions = problem.get_actions(state)
        h = heuristic(problem,state)
        for action in actions:
            successor = problem.get_successor(state, action)
            new_path = list(path)
            new_path.append(action)
            if successor not in explored:
                curr_cost = problem.get_cost(state,action)
                curr_h = heuristic(problem,successor)
                frontier.put((cost+curr_cost+curr_h-h,counter,successor))
                paths.put((cost+curr_cost+curr_h-h,counter,new_path))
                counter+=1
    return None
    


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    counter:int =0
    frontier: PriorityQueue[(float,int,S)] = PriorityQueue()
    paths : PriorityQueue[(float,int,list[A])] = PriorityQueue()
    frontier.put((heuristic(problem,initial_state),counter,initial_state))
    paths.put((heuristic(problem,initial_state),counter,[]))
    counter+=1
    explored = set()
    while not frontier.empty():
        _,_,state = frontier.get()
        _,_,path = paths.get()
        if problem.is_goal(state):
            return path
        if state in explored:
            continue
        explored.add(state)
        actions = problem.get_actions(state)
        for action in actions:
            successor = problem.get_successor(state, action)
            new_path = list(path)
            new_path.append(action)
            if problem.is_goal(state):
                return path
            if successor not in explored:
                curr_h = heuristic(problem,successor)
                frontier.put((curr_h,counter,successor))
                paths.put((curr_h,counter,new_path))
                counter+=1
    return None