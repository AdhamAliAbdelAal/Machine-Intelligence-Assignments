from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    hue = heuristic(game, state, 0)
    # check if terminal
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    # check if max depth
    if max_depth == 0:
        return hue, None 
    # get actions
    actions = game.get_actions(state)
    # define min and max functions
    def min_function(state: S) -> Tuple[float, A]:
        value = float('inf')
        action = None
        for a in actions:
            successor = game.get_successor(state, a)
            v, _ = minimax(game, successor, heuristic, max_depth- 1)
            # minimize value
            if v < value:
                value = v
                action = a
        return value, action
    
    def max_function(state: S) -> Tuple[float, A]:
        value = float('-inf')
        action = None
        for a in actions:
            successor = game.get_successor(state, a)
            v, _ = minimax(game, successor, heuristic, max_depth-1)
            # maximize value
            if v > value:
                value = v
                action = a
        return value, action
    # get turn
    turn = game.get_turn(state)
    # if my turn, maximize else minimize
    if turn == 0:
        return max_function(state)
    else:
        return min_function(state)

        



# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:

    def solve(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
            hue = heuristic(game, state, 0)
            terminal, values = game.is_terminal(state)
            if terminal:
                return values[0], None
            if max_depth == 0:
                return hue, None 

            actions = game.get_actions(state)
            def min_function(state: S, alpha: float, beta: float) -> Tuple[float, A]:
                value = float('inf')
                action = None
                for a in actions:
                    successor = game.get_successor(state, a)
                    v, _ = solve(successor, max_depth- 1, alpha, beta)
                    # prune
                    if(v <= alpha):
                        return v, a
                    # update my beta
                    beta = min(beta, v)
                    if v < value:
                        value = v
                        action = a
                return value, action
            
            def max_function(state: S, alpha: int, beta: int) -> Tuple[float, A]:
                value = float('-inf')
                action = None
                for a in actions:
                    successor = game.get_successor(state, a)
                    v, _ = solve(successor, max_depth- 1, alpha, beta)
                    # prune
                    if(v >= beta):
                        return v, a
                    # update my alpha
                    alpha = max(alpha, v)
                    if v > value:
                        value = v
                        action = a
                return value, action
            turn = game.get_turn(state)
            if turn == 0:
                return max_function(state, alpha, beta)
            else:
                return min_function(state, alpha, beta)
    # initialize alpha and beta with -inf and inf
    return solve(state, max_depth, float('-inf'), float('inf'))

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def solve(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
            hue = heuristic(game, state, 0)
            terminal, values = game.is_terminal(state)
            if terminal:
                return values[0], None
            if max_depth == 0:
                return hue, None 

            actions = game.get_actions(state)
            def min_function(state: S, alpha: float, beta: float) -> Tuple[float, A]:
                value = float('inf')
                action = None
                # sort actions based on heuristic
                def order(a):
                    successor = game.get_successor(state, a)
                    v = heuristic(game, successor, 0)
                    return v
                # sort ascending
                actions.sort(key=order)
                for a in actions:
                    successor = game.get_successor(state, a)
                    v, _ = solve(successor, max_depth- 1, alpha, beta)
                    if(v <= alpha):
                        return v, a
                    beta = min(beta, v)
                    if v < value:
                        value = v
                        action = a
                return value, action
            
            def max_function(state: S, alpha: int, beta: int) -> Tuple[float, A]:
                value = float('-inf')
                action = None
                # sort actions based on heuristic
                def order(a):
                    successor = game.get_successor(state, a)
                    v = heuristic(game, successor, 0)
                    return v
                # sort descending
                actions.sort(key=order, reverse=True)
                for a in actions:
                    successor = game.get_successor(state, a)
                    v, _ = solve(successor, max_depth- 1, alpha, beta)
                    if(v >= beta):
                        return v, a
                    alpha = max(alpha, v)
                    if v > value:
                        value = v
                        action = a
                return value, action
            turn = game.get_turn(state)
            if turn == 0:
                return max_function(state, alpha, beta)
            else:
                return min_function(state, alpha, beta)
    return solve(state, max_depth, float('-inf'), float('inf'))

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    hue = heuristic(game, state, 0)
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    if max_depth == 0:
        return hue, None 

    actions = game.get_actions(state)
    def expectation_function(state: S) -> float:
        value = 0
        for a in actions:
            successor = game.get_successor(state, a)
            v, _ = expectimax(game, successor, heuristic, max_depth- 1)
            value += v
        # get the expectation by dividing by the number of actions
        return value/len(actions), None
    
    def max_function(state: S) -> Tuple[float, A]:
        value = float('-inf')
        action = None
        for a in actions:
            successor = game.get_successor(state, a)
            v, _ = expectimax(game, successor, heuristic, max_depth-1)
            if v > value:
                value = v
                action = a
        return value, action
    turn = game.get_turn(state)
    # if my turn, maximize else get expectation
    if turn == 0:
        return max_function(state)
    else:
        return expectation_function(state)