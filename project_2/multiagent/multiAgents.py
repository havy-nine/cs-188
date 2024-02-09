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

        "*** YOUR CODE HERE ***"
        
        #print(newScaredTimes)
        
        getFood = newFood.asList()
       # print(len(getFood))
        distance = 10000000
        ghost_d = 10000000
        food_d =10000000
        for i in newGhostStates:
            #print(newGhostStates) #Ghost: (x,y)=(2.0, 4.0), South
            x, y = i.getPosition()
            if newScaredTimes == [0]:
                ghost_d = min(ghost_d, manhattanDistance(newPos, (x,y)))
            else:
                ghost_d = ghost_d
            
        if ghost_d <=3: return -10000000
                
        #print(getFood)
        for i in getFood:
           # print(len(getFood))
           #food_d = min(distance, manhattanDistance(newPos,tuple(i)))
            if len(getFood)==0:
                return -1000000
            food_d = min(food_d, manhattanDistance(newPos,tuple(i)))
            #print(i)
                
        #print(successorGameState.getScore())
            
        #successorGameState.getScore()
        return 1/(food_d)-len(getFood)

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
        
       # print(gameState.getNumAgents())
        
        def minimaxScore(gameState, index, depth):
            #print(depth)
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState), 0
            
            elif index == 0: #get pacman
                bestAct = None
                maxScore = -100000000
                depth = depth 
                next_index = index +1
                acts = gameState.getLegalActions(index)
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score = minimaxScore(successors, next_index, depth)[0]
                    if maxScore < score:
                        maxScore = score
                        bestAct = act
                return (maxScore, bestAct)
            
            else:
                if index == gameState.getNumAgents()-1:
                    next_index = 0
                    depth = depth -1
                else:
                    next_index = index + 1
                    depth = depth
                    
                bestAct = None
                minScore = 100000000
                acts = gameState.getLegalActions(index)
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score = minimaxScore(successors, next_index, depth)[0]
                    if minScore > score:
                        minScore = score
                        bestAct = act
                        
                return (minScore, bestAct)
                    
                #ghost
        
        return minimaxScore(gameState, 0, self.depth)[1]
        
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1000000
        beta = 1000000
        def alphaBeta(gameState, index, depth, alpha, beta):
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState), 0
            
            elif index == 0: #get pacman
                bestAct = None
                maxScore = -100000000
                depth = depth 
                next_index = index +1
                acts = gameState.getLegalActions(index)
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score = alphaBeta(successors, next_index, depth, alpha, beta)[0]
                    if maxScore < score:
                        maxScore = score
                        bestAct = act
                    if score > beta:
                        return score, act
                    if maxScore > alpha:
                        alpha = score
                return (maxScore, bestAct)
            
            else:
                if index == gameState.getNumAgents()-1:
                    next_index = 0
                    depth = depth -1
                else:
                    next_index = index + 1
                    depth = depth
                    
                bestAct = None
                minScore = 100000000
                acts = gameState.getLegalActions(index)
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score = alphaBeta(successors, next_index, depth, alpha, beta)[0]
                    if minScore > score:
                        minScore = score
                        bestAct = act
                    if minScore < alpha:
                        return score, act
                    if minScore < beta:
                        beta = score
                        
                return (minScore, bestAct)
                    
                #ghost
        
        return alphaBeta(gameState, 0, self.depth, alpha, beta)[1]


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
        legalAction = gameState.getLegalActions()
        
        def expectimax(gameState, index, depth):
            #print(depth)
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState), 0
            
            elif index == 0: #get pacman
                bestAct = None
                maxScore = -100000000
                depth = depth 
                next_index = index +1
                acts = gameState.getLegalActions(index)
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score = expectimax(successors, next_index, depth)[0]
                    if maxScore < score:
                        maxScore = score
                        bestAct = act
                return (maxScore, bestAct)
            
            else:
                if index == gameState.getNumAgents()-1:
                    next_index = 0
                    depth = depth -1
                else:
                    next_index = index + 1
                    depth = depth
                    
                bestAct = None
                minScore = 100000000
                acts = gameState.getLegalActions(index)
                score = 0
                for act in acts:
                    successors = gameState.generateSuccessor(index, act)
                    score += expectimax(successors, next_index, depth)[0]                    
   
                return (score/len(acts), None)
                    
                #ghost
        
        return expectimax(gameState, 0, self.depth)[1]
        
        
        
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    I get variable about current position: pos_xy, current food : Food, current ghoststates: GhostState,
    If ghost is scared : ScaredTimes.
    At first, I find manhattan distance between ghostStates and current position
    If this distance is close, it is unstable position. So the final return takes -1/ghost_distance.
    
    But if ghost got scared, it can get much more score to eat ghost. So the return when ghost is scared takes +1/ghost_distance.
    I add variable -len(getFood) since it is better to eat good than not to eat food. 
    If ghost_distance is vary close(like under 3), it is vary dangerous situation so return -10000000.
    Get food_distance with manhattan distance, and add +1/food_distance to final return variable. 
    """
    "*** YOUR CODE HERE ***"
    pos_xy = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    getFood = Food.asList()
       # print(len(getFood))
    
    ghost_d = 10000000
    food_d = 10000000
    for i in GhostStates:
        #print(newGhostStates) #Ghost: (x,y)=(2.0, 4.0), South
        x, y = i.getPosition()
        
        if ScaredTimes == [0]:
            ghost_d = min(ghost_d, manhattanDistance(pos_xy, (x,y)))
        else:
            ghost_d = min(ghost_d, manhattanDistance(pos_xy, (x,y)))
            return 1/ghost_d +1/(food_d)*0.5
            
    if ghost_d <=2: return -10000000
                
        #print(getFood)
    for i in getFood:
           # print(len(getFood))
           
        food_d = min(food_d, manhattanDistance(pos_xy,tuple(i)))
            
    return -1/ghost_d+1/(food_d)-len(getFood)
    
# Abbreviation
better = betterEvaluationFunction
