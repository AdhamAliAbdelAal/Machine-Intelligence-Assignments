from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented
import copy

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        # get all actions
        actions = self.mdp.get_actions(state)
        # if terminal state, return 0  
        if self.mdp.is_terminal(state):
            return 0
        else:
            # initialize best utility to be -inf
            best_utility = float('-inf')
            for action in actions:
                action_utility = 0
                # get all successors
                successors = self.mdp.get_successor(state, action)
                for successor, prob in successors.items():
                    # get reward and utility
                    reward = self.mdp.get_reward(state, action, successor)
                    utility = self.utilities[successor]
                    # compute current utility
                    current_utility = prob * (reward + self.discount_factor * utility)
                    # add to action utility
                    action_utility += current_utility
                # update best utility
                best_utility = max(best_utility, action_utility)
            return best_utility
                    
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        temp = copy.deepcopy(self.utilities)
        # initialize max_change to be 0
        max_change = 0.0
        states = self.mdp.get_states()
        for state in states:
            # compute bellman equation
            temp[state] = self.compute_bellman(state)
            # update max_change
            max_change = max(max_change, abs(self.utilities[state] - temp[state]))
        # update utilities with temp utilities
        self.utilities = temp
        # check convergence
        if max_change <= tolerance:
            return True
        else:
            return False

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        for i in range(iterations):
            # update utilities
            if self.update(tolerance):
                # return number of iterations 1-indexed
                return i+1
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        if self.mdp.is_terminal(state):
            return None
        else:
            # get all actions
            actions = self.mdp.get_actions(state)
            # initialize best utility to be -inf
            best_utility = float('-inf')
            best_action = None
            for action in actions:
                action_utility = 0
                # get all successors
                successors = self.mdp.get_successor(state, action)
                # compute utility for each successor
                for successor, prob in successors.items():
                    reward = self.mdp.get_reward(state, action, successor)
                    utility = self.utilities[successor]
                    # compute current utility
                    # add to action utility
                    action_utility += prob * (reward + self.discount_factor * utility)
                if action_utility > best_utility:
                    # update best utility and action
                    best_utility = action_utility
                    best_action = action
            return best_action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
