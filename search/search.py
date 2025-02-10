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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    visited = set()
    stack = util.Stack()
    stack.push((problem.getStartState(), []))
    
    while not stack.isEmpty():
        top = stack.pop()
        state = top[0]
        path = top[1]

        visited.add(state)
        
        if problem.isGoalState(state):
            return path

        for successor in problem.getSuccessors(state):
            next_state, action, _ = successor
            # print("Successor to", state, ": ", successor)
            if next_state not in visited:
                # print("Pushing", next_state)
                stack.push((next_state, path + [action]))

    # We should always find a happy path before here
    assert(False)

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    visited = set()
    queue = util.Queue()
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():
        front = queue.pop()
        state = front[0]
        path = front[1]

        if state in visited:
            continue
        
        visited.add(state)

        if problem.isGoalState(state):
            return path
        
        for successor in problem.getSuccessors(state):
            next_state, action, _ = successor
            # print("Successor to", state, ": ", successor)
            if next_state not in visited:
                # print("Pushing", next_state)
                queue.push((next_state, path + [action]))

    # We should always find a happy path before here
    assert(False)


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = set()
    queue = util.PriorityQueue()
    init_cost = 0
    queue.push((problem.getStartState(), [], init_cost), init_cost)

    while not queue.isEmpty():
        front = queue.pop()
        state = front[0]
        path = front[1]
        cost = front[2]

        if state in visited:
            # print("Already visited: ", state)
            continue

        # print(state)
        visited.add(state)

        if problem.isGoalState(state):
            return path
        
        for successor in problem.getSuccessors(state):
            next_state, action, next_cost = successor
            # print("Successor to", state, ": ", successor)
            if next_state not in visited:
                # print("Pushing", next_state)
                queue.push((next_state, path + [action], cost + next_cost), cost + next_cost)

        # print("Is queue empty: ", queue.isEmpty())

    # We should always find a happy path before here
    assert(False)  

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    def aStar(item: tuple[any, list[any], int]):
        state, _, cost = item
        return cost + heuristic(state, problem)
    
    visited = set()
    queue = util.PriorityQueueWithFunction(aStar)
    init_cost = 0
    queue.push((problem.getStartState(), [], init_cost))

    while not queue.isEmpty():
        front = queue.pop()
        state, path, cost = front

        if state in visited:
            continue

        # print(state)
        visited.add(state)

        if problem.isGoalState(state):
            return path
        
        for successor in problem.getSuccessors(state):
            next_state, action, next_cost = successor
            # print("Successor to", state, ": ", successor)
            if next_state not in visited:
                # print("Pushing", next_state)
                queue.push((next_state, path + [action], cost + next_cost))

    assert(False)




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
