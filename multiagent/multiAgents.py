# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        if(successorGameState.isWin()):
            return float('inf')
        
        if(successorGameState.isLose()):
            return float('-inf')

        foodList = newFood.asList()

        if(foodList):
            closest = min((util.manhattanDistance(newPos, pellet)) for pellet in foodList)
            food_proximity_factor = -closest
        else:
            food_proximity_factor = 0

        num_food = len(foodList)
        food_factor = -num_food

        # print("Ghost states:", list(g.getPosition() for g in newGhostStates))
        # print("Scared Times:", newScaredTimes)

        if newGhostStates:
            closest_ghost = min([util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer == 0], default=float('inf'))
            if(closest_ghost < 5):
                ghost_proximity_factor = closest_ghost
            else:
                ghost_proximity_factor = 100
        else:
            ghost_proximity_factor = 100

        if capsules:
            closest_capsule = min(util.manhattanDistance(newPos, capsule) for capsule in capsules)
            capsule_proximity_factor = -closest_capsule
        else:
            capsule_proximity_factor = 0

        scared_factor = sum(newScaredTimes)
        score = food_proximity_factor + food_factor*100 + ghost_proximity_factor*100 + scared_factor + capsule_proximity_factor
        # print("Score:", score)
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        nextStates = [gameState.generateSuccessor(0, a) for a in actions]
        minimaxValues = [self.Minimax(s, index=1, depth=0) for s in nextStates]

        maxValue = max(minimaxValues)
        actionIndex = minimaxValues.index(maxValue)

        # print(actions[actionIndex])
        return actions[actionIndex]

    def AtDepth(self, numAgents, index, depth):
        return depth == self.depth

    def Minimax(self, gameState: GameState, index, depth):
        """
        Recursive function to find the Minimax value of a given node
        """
        numAgents = gameState.getNumAgents()

        if self.AtDepth(numAgents, index, depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        if index == numAgents - 1:
            nextIndex = 0
            nextDepth = depth + 1
        else:
            nextIndex = index + 1
            nextDepth = depth

        actions = gameState.getLegalActions(index)
        if not actions:
            print(gameState.getGhostPositions())
            util.pause()
        nextStates = [gameState.generateSuccessor(index, a) for a in actions]
        minimaxValues = (self.Minimax(s, nextIndex, nextDepth) for s in nextStates)

        if index == 0:
            return max(minimaxValues)
        else:
            return min(minimaxValues)
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        nextStates = [gameState.generateSuccessor(0, a) for a in actions]
        alpha = float('-inf')
        beta = float('inf')

        v = float('-inf')
        action = None
        for i, s in enumerate(nextStates):
            minimax = self.Minimax(s, 1, 0, alpha, beta)
            if minimax > v:
                v = minimax
                action = actions[i] 
            if v > beta:
                return actions[i]
            alpha = max(alpha, v)

        return action
    
    def MinValue(self, gameState: GameState, index, depth, alpha, beta):
        actions = gameState.getLegalActions(index)
        numAgents = gameState.getNumAgents()

        if index == numAgents - 1:
            nextIndex = 0
            nextDepth = depth + 1
        else:
            nextIndex = index + 1
            nextDepth = depth

        v = float('inf')
        for a in actions:
            s = gameState.generateSuccessor(index, a)
            v = min(v, self.Minimax(s, nextIndex, nextDepth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def MaxValue(self, gameState: GameState, index, depth, alpha, beta):
        actions = gameState.getLegalActions(index)
        numAgents = gameState.getNumAgents()

        if index == numAgents - 1:
            nextIndex = 0
            nextDepth = depth + 1
        else:
            nextIndex = index + 1
            nextDepth = depth
        
        v = float('-inf')
        for a in actions:
            s = gameState.generateSuccessor(index, a)
            v = max(v, self.Minimax(s, nextIndex, nextDepth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def AtDepth(self, numAgents, index, depth):
        return depth == self.depth

    def Minimax(self, gameState: GameState, index, depth, alpha, beta):
        """
        Recursive function to find the Minimax value of a given node
        """
        numAgents = gameState.getNumAgents()

        if self.AtDepth(numAgents, index, depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if index == 0:
            return self.MaxValue(gameState, index, depth, alpha, beta)
        else:
            return self.MinValue(gameState, index, depth, alpha, beta)
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        nextStates = [gameState.generateSuccessor(0, a) for a in actions]
        minimaxValues = [self.Expectimax(s, index=1, depth=0) for s in nextStates]

        maxValue = max(minimaxValues)
        actionIndex = minimaxValues.index(maxValue)

        # print(actions[actionIndex])
        return actions[actionIndex]

    def AtDepth(self, numAgents, index, depth):
        return depth == self.depth

    def Expectimax(self, gameState: GameState, index, depth):
        """
        Recursive function to find the Expectimax value of a given node
        """
        numAgents = gameState.getNumAgents()

        if self.AtDepth(numAgents, index, depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if index == 0:
            return self.MaxValue(gameState, index, depth)
        else:
            return self.ExpValue(gameState, index, depth)

    def MaxValue(self, gameState: GameState, index, depth):
        actions = gameState.getLegalActions(index)
        numAgents = gameState.getNumAgents()

        if index == numAgents - 1:
            nextIndex = 0
            nextDepth = depth + 1
        else:
            nextIndex = index + 1
            nextDepth = depth
        
        nextStates = [gameState.generateSuccessor(index, a) for a in actions]
        expectimaxValues = (self.Expectimax(s, nextIndex, nextDepth) for s in nextStates)
        return max(expectimaxValues)
    
    def ExpValue(self, gameState: GameState, index, depth):
        actions = gameState.getLegalActions(index)
        numAgents = gameState.getNumAgents()

        if index == numAgents - 1:
            nextIndex = 0
            nextDepth = depth + 1
        else:
            nextIndex = index + 1
            nextDepth = depth
        
        nextStates = [gameState.generateSuccessor(index, a) for a in actions]
        expectimaxValues = [self.Expectimax(s, nextIndex, nextDepth) for s in nextStates]
        return sum(expectimaxValues) / len(list(expectimaxValues))

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()

    "*** YOUR CODE HERE ***"
    if(currentGameState.isWin()):
        return float('inf')
    
    if(currentGameState.isLose()):
        return float('-inf')

    # what makes a good state
    # minimum amounts of food
    # minimum distance from food
    # minimum amounts of pellets

    foodList = food.asList()

    edges = []
    for i in range(len(foodList)):
        for j in range(i + 1, len(foodList)):
            dist = util.manhattanDistance(foodList[i], foodList[j])
            edges.append((dist, i, j))

    edges.sort()

    parent = list(range(len(foodList)))

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]
    
    mst_sum = 0
    for dist, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            mst_sum += dist

    closest = min((util.manhattanDistance(pos, pellet)) for pellet in foodList)
    food_dist = -(mst_sum + closest)

    score = food_dist - len(foodList) + currentGameState.getScore()*100
    # print("score:", score)
    return score

# Abbreviation
better = betterEvaluationFunction
