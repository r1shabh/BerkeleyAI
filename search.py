# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    if problem.isGoalState(state):
        return []
    
    frontier = util.Stack()
    node = (state, [], 0)
    frontier.push(node)
    explored = set([])

    while not frontier.isEmpty():
        (curr_state, action_so_far, curr_cost) = frontier.pop()
        if problem.isGoalState(curr_state):
            return action_so_far
        explored.add(curr_state)
        #print problem.getSuccessors(curr_state)
        for (state, action, cost) in problem.getSuccessors(curr_state):
            actionlist = [a for (s, a, c) in frontier.list]
            if state not in explored and action not in actionlist:
                new_action = action_so_far + [action]      
                new_node = (state, new_action, cost)
                frontier.push(new_node)
    return []
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    if problem.isGoalState(state):
        return []
    
    frontier = util.Queue()
    node = (state, [], 0)
    frontier.push(node)
    explored = set([])

    while not frontier.isEmpty():
        (curr_state, action_so_far, curr_cost) = frontier.pop()
        if problem.isGoalState(curr_state):
            return action_so_far 
        explored.add(curr_state)
        for (state, action, cost) in problem.getSuccessors(curr_state):
            stateList = [s for (s, a, c) in frontier.list]
            if state not in explored and state not in stateList:
                new_action = action_so_far + [action]
                new_node = (state, new_action, problem.getCostOfActions(new_action))
                frontier.push(new_node) 
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    frontier = util.PriorityQueue()
    paths = {}
    costs = {}
    frontier.push(state, 0)
    paths[state] = []
    costs[state] = 0
    explored = set([])
    while not frontier.isEmpty():
        curr_state = frontier.pop()
        action_so_far = paths[curr_state]
        curr_cost = costs[curr_state]
        if problem.isGoalState(curr_state):
            return action_so_far
        explored.add(curr_state)
        for (state, action, cost) in problem.getSuccessors(curr_state):
            states = [s for s in frontier.heap]
            new_action = action_so_far + [action]
            new_cost = curr_cost + cost
            if state not in explored:
                frontier.update(state, new_cost)
                if state not in paths or costs[state] > new_cost:
                    paths[state] = new_action
                if state not in costs or costs[state] > new_cost:
                    costs[state] = new_cost
                
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    cost = heuristic(state, problem)
    frontier = util.PriorityQueue()
    paths = {}
    costs = {}
    frontier.push(state, cost)
    paths[state] = []
    costs[state] = cost
    explored = set([])
    state = problem.getStartState()
    while not frontier.isEmpty():
        curr_state = frontier.pop()
        action_so_far = paths[curr_state]
        curr_cost = costs[curr_state]
        if problem.isGoalState(curr_state):
            return action_so_far
        explored.add(curr_state)
        curr_heuristic = heuristic(curr_state, problem)
        for (state, action, cost) in problem.getSuccessors(curr_state):
            if state not in explored:
                next_heuristic = heuristic(state, problem)
                new_action = action_so_far + [action]
                new_cost = curr_cost + cost + next_heuristic - curr_heuristic
                frontier.update(state, new_cost)
                if state not in paths or costs[state] > new_cost:
                    paths[state] = new_action
                if state not in costs or costs[state] > new_cost:
                    costs[state] = new_cost
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
