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
               first = 'OffensiveAgent', second = 'DefensiveAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

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
        values = [self.evaluate(gameState, a) for a in actions]
        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        return random.choice(bestActions)

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

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

class OffensiveAgent(ReflexCaptureAgent):
    """
    An offensive agent that seeks food and avoids ghosts
    """
    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        
        # Convert myPos to integers
        myPos = (int(myPos[0]), int(myPos[1]))
        
        # Visual debugging - color based on state
        if myState.isPacman:
            self.debugDraw([myPos], [0, 1, 0])  # Green for Pacman
        else:
            self.debugDraw([myPos], [1, 0, 0])  # Red for Ghost
        
        # Get food and capsules
        foodList = self.getFood(successor).asList()
        capsules = self.getCapsules(successor)
        
        # Get enemy states
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
        
        # Score feature
        features['successorScore'] = -len(foodList)
        
        # Food distance feature
        if len(foodList) > 0:
            minFoodDist = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minFoodDist
        
        # Ghost avoidance feature
        if len(ghosts) > 0:
            ghostDists = [self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]
            minGhostDist = min(ghostDists)
            features['ghostDistance'] = minGhostDist
            if minGhostDist < 3:
                features['ghostTooClose'] = 1
        
        # Capsule feature
        if len(capsules) > 0:
            minCapsuleDist = min([self.getMazeDistance(myPos, cap) for cap in capsules])
            features['distanceToCapsule'] = minCapsuleDist
        
        # Return home features
        if myState.isPacman:  # If we're on enemy side
            # Check if we're carrying food or got a capsule
            if len(foodList) < len(self.getFood(gameState).asList()) or len(capsules) < len(self.getCapsules(gameState)):
                # Calculate home direction
                centerX = int(gameState.data.layout.width / 2)
                if self.red:
                    # For red team, home is to the left of center
                    if myPos[0] > centerX:
                        features['moveLeft'] = 1
                    else:
                        features['moveLeft'] = -1
                else:
                    # For blue team, home is to the right of center
                    if myPos[0] < centerX:
                        features['moveRight'] = 1
                    else:
                        features['moveRight'] = -1
                
                # Calculate progress toward home
                if self.red:
                    features['progressHome'] = centerX - myPos[0]  # Positive when moving left
                else:
                    features['progressHome'] = myPos[0] - centerX  # Positive when moving right
                
                # If we're near the center, prioritize crossing
                if self.red:
                    # For red team, we want to be just left of center
                    if myPos[0] < centerX and abs(myPos[0] - centerX) < 2:
                        features['nearCenter'] = 1
                else:
                    # For blue team, we want to be just right of center
                    if myPos[0] > centerX and abs(myPos[0] - centerX) < 2:
                        features['nearCenter'] = 1
                
                # Visual debugging - show home direction
                if self.red:
                    homeX = centerX - 1
                else:
                    homeX = centerX + 1
                homePos = (homeX, myPos[1])
                self.debugDraw([homePos], [0, 0, 1])  # Blue for home position
        
        # Stop and reverse features
        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1
        
        return features

    def getWeights(self, gameState, action):
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        
        # Base weights
        weights = {
            'successorScore': 100,
            'distanceToFood': -2,
            'ghostDistance': 3,
            'ghostTooClose': -1000,
            'distanceToCapsule': -2,
            'stop': -100,
            'reverse': -2,
            'moveLeft': 0,
            'moveRight': 0,
            'progressHome': 0,
            'nearCenter': 0
        }
        
        # If we're carrying food or got a capsule, prioritize returning
        if myState.isPacman:
            foodList = self.getFood(successor).asList()
            capsules = self.getCapsules(successor)
            if len(foodList) < len(self.getFood(gameState).asList()) or len(capsules) < len(self.getCapsules(gameState)):
                if self.red:
                    weights['moveLeft'] = 10
                    weights['progressHome'] = 5
                else:
                    weights['moveRight'] = 10
                    weights['progressHome'] = 5
                weights['nearCenter'] = 100
                weights['distanceToFood'] = 0  # Stop seeking food when returning
        
        return weights

class DefensiveAgent(ReflexCaptureAgent):
    """
    A defensive agent that protects its territory and chases invaders
    """
    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        
        # Convert myPos to integers
        myPos = (int(myPos[0]), int(myPos[1]))
        
        # Get enemy states
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        
        # Defense feature
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0
        
        # Invader features
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            invaderPositions = [(int(a.getPosition()[0]), int(a.getPosition()[1])) for a in invaders]
            dists = [self.getMazeDistance(myPos, pos) for pos in invaderPositions]
            features['invaderDistance'] = min(dists)
        
        # Food defense feature
        foodList = self.getFoodYouAreDefending(successor).asList()
        if len(foodList) > 0:
            foodDists = [self.getMazeDistance(myPos, food) for food in foodList]
            features['distanceToFood'] = min(foodDists)
        
        # Stop and reverse features
        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1
        
        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'distanceToFood': -1,
            'stop': -100,
            'reverse': -2
        }

