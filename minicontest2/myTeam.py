# myTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'ImprovedOffensiveAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ImprovedOffensiveAgent(CaptureAgent):
  """
  An improved offensive agent that:
  1. Efficiently collects food while avoiding enemies
  2. Uses power capsules strategically
  3. Returns home when carrying food
  4. Avoids getting trapped
  """

  def registerInitialState(self, gameState):
    """
    Initial setup of the agent.
    """
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)
    self.foodCarrying = 0

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)
    if not actions:
      return None

    # Get current state information
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    foodList = self.getFood(gameState).asList()
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    scaredGhosts = [a for a in ghosts if a.scaredTimer > 0]

    # Update food carrying status
    prevObs = self.getPreviousObservation()
    if prevObs is not None:
      prevFoodList = self.getFood(prevObs).asList()
      if len(foodList) < len(prevFoodList):
        self.foodCarrying += 1

    # Evaluate all possible actions
    values = [self.evaluate(gameState, a) for a in actions]
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    # If carrying food and near home, prioritize returning
    if self.foodCarrying > 0 and self.isNearHome(gameState, myPos):
      homeActions = []
      for action in bestActions:
        successor = self.getSuccessor(gameState, action)
        nextPos = successor.getAgentState(self.index).getPosition()
        if self.isHome(gameState, nextPos):
          homeActions.append(action)
      if homeActions:
        return random.choice(homeActions)

    return random.choice(bestActions)

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights.
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state.
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Food features
    foodList = self.getFood(successor).asList()
    features['successorScore'] = -len(foodList)

    # Compute distance to the nearest food
    if len(foodList) > 0:
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    # Enemy features
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    scaredGhosts = [a for a in ghosts if a.scaredTimer > 0]

    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      minDist = min(dists)
      features['ghostDistance'] = minDist
      if minDist < 3:  # Increased from 2 to 3
        features['ghostNearby'] = 1

    # Power capsule features
    capsules = self.getCapsules(successor)
    if len(capsules) > 0:
      minCapsuleDist = min([self.getMazeDistance(myPos, cap) for cap in capsules])
      features['capsuleDistance'] = minCapsuleDist

    # Avoid stopping
    if action == Directions.STOP:
      features['stop'] = 1

    # Avoid reversing
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev:
      features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    """
    Returns weights for the features.
    """
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    scaredGhosts = [a for a in ghosts if a.scaredTimer > 0]

    # Base weights
    weights = {
      'successorScore': 100,
      'distanceToFood': -1,
      'ghostDistance': 1,  # Reduced from 2 to 1
      'ghostNearby': -500,  # Reduced from -1000 to -500
      'capsuleDistance': -1,  # Reduced from -2 to -1
      'stop': -100,
      'reverse': -2
    }

    # Adjust weights based on game state
    if len(scaredGhosts) > 0:
      weights['ghostDistance'] = -1  # Chase scared ghosts
      weights['ghostNearby'] = 0     # Don't fear scared ghosts

    if self.foodCarrying > 0:
      weights['distanceToFood'] = 0  # Don't care about food when carrying
      weights['successorScore'] = 0  # Don't care about food when carrying

    return weights

  def isHome(self, gameState, pos):
    """
    Check if the given position is on our home side.
    """
    width = gameState.data.layout.width
    if self.red:
      return pos[0] < width / 2
    else:
      return pos[0] >= width / 2

  def isNearHome(self, gameState, pos):
    """
    Check if the given position is near our home side.
    """
    width = gameState.data.layout.width
    if self.red:
      return pos[0] < width / 2 + 2  # Within 2 units of home
    else:
      return pos[0] >= width / 2 - 2  # Within 2 units of home

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
 
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

