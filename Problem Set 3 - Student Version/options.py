# This file contains the options that you should modify to solve Question 2

def question2_1():
    # discount factor 0.1 to make the agent care more about the immediate reward (1) than the future reward (10)
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": 0
    }

def question2_2():
    # noise 0.02 to make the agent fears of falling into the -10 path
    # discount factor 0.1 to make the agent care more about the immediate reward (1) than the future reward (10)
    # living reward -0.1 to make the agent avoid staying in the same state and keep moving towards the goal
    return {
        "noise": 0.02,
        "discount_factor": 0.1,
        "living_reward": -0.1
    }

def question2_3():
    # discount factor 0.9 to make the agent care more about the future reward (10) than the immediate reward (1)
    return {
        "noise": 0,
        "discount_factor": 0.9,
        "living_reward": 0
    }

def question2_4():
    # noise 0.2 to make the agent fears of falling into the -10 path
    # discount factor 1 to make the agent care more about the future reward (10) than the immediate reward (1)
    # living reward -0.1 to make the agent avoid staying in the same state and keep moving towards the goal
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }

def question2_5():
    # high living reward to make the agent avoid moving towards the goal and stay in the game
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 100
    }

def question2_6():
    # high negative living reward to make the agent try to go to any terminal state as soon as possible
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100
    }