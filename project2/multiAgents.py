# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
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

  def evaluationFunction(self, currentGameState, action):
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
    #pacman is a v, <, >, ^ depending on orientation, ghost is G, . is food
    newPos = successorGameState.getPacmanPosition() # pacman position of successor
    newFood = successorGameState.getFood() #not sure? more than 5 food
    newGhostStates = successorGameState.getGhostStates() #tuple of all ghosts
    #in following form: Ghost: (x,y)=(3.0, 5.0), East
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if Directions.STOP in action:
        return float("-inf")

    currentFoodList = currentGameState.getFood().asList()
    dist = float("inf")

    for ghostState in newGhostStates:
        if ghostState.getPosition() == newPos:
            return float("-inf")#pacman is about to be got

    for foodPos in currentFoodList:
        if manhattanDistance(foodPos, newPos) < dist:
            dist = manhattanDistance(newPos, foodPos)

    if dist == 0:
        return float("inf") #go to food dot
    return 1.0/dist #reciprocal

    #print newFood[1]
    #print newGhostStates[0]
    #print newScaredTimes

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

  def minimax_decision(self, gameState, index, depth):
    if index >= gameState.getNumAgents():
      index = 0
      depth += 1

    if depth == self.depth:
      return self.evaluationFunction(gameState)

    if index == 0:
      return self.max_value(gameState, index, depth)
    else:
      return self.min_value(gameState, index, depth)

    #return 'None'

  def max_value(self, gameState, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [float('-inf'), Directions.STOP]
    actions = gameState.getLegalActions(index)

    for action in actions:
      if action == Directions.STOP:
        continue

      successor = gameState.generateSuccessor(index, action)
      cur_val = self.minimax_decision(successor, index+1, depth)

      val_and_action = [max(val_and_action[0], cur_val), action]

    if depth == 0:
      return val_and_action[1]
    else:
      return val_and_action[0]


  def min_value(self, gameState, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [float('inf'), Directions.STOP]
    actions = gameState.getLegalActions(index)

    for action in actions:
      if action == Directions.STOP:
        continue

      successor = gameState.generateSuccessor(index, action)
      cur_val = self.minimax_decision(successor, index+1, depth)

      val_and_action = [min(val_and_action[0], cur_val), action]

    return val_and_action[0]

  def getAction(self, gameState):


    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    return self.minimax_decision(gameState, 0, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    return self.minimax_decision(gameState, float('-inf'), float('inf'), 0, 0)

  def minimax_decision(self, gameState, a, b, index, depth):
    if index >= gameState.getNumAgents():
      index = 0
      depth += 1

    if depth == self.depth:
      return self.evaluationFunction(gameState)
    #if Pacman
    if index == 0:
      return self.max_value(gameState, a, b, index, depth)
    #if Ghost
    else:
      return self.min_value(gameState, a, b, index, depth)

    # return 'None'

  def max_value(self, gameState, a, b, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [float('-inf'), Directions.STOP]
    actions = gameState.getLegalActions(index)

    for action in actions:
      if action == Directions.STOP:
        continue

      successor = gameState.generateSuccessor(index, action)

      #cur_val is Min-Value(Result(s,a), a, b)
      cur_val = self.minimax_decision(successor, a, b, index + 1, depth)

      val_and_action = [max(val_and_action[0], cur_val), action]
      #take the max between val and the current val
      a = max(a, val_and_action[0])
      if (val_and_action[0] > b):
        if depth == 0:
          # if depth == 0 return the action
          return val_and_action[1]
        else:
          # else return the value
          return val_and_action[0]


    if depth == 0:
      #if depth == 0 return the action
      return val_and_action[1]
    else:
      #else return the value
      return val_and_action[0]



  def min_value(self, gameState, a, b, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [float('inf'), Directions.STOP]

    #Get min's legal actions
    actions = gameState.getLegalActions(index)

    for action in actions:
      if action == Directions.STOP:
        continue


      successor = gameState.generateSuccessor(index, action)
      cur_val = self.minimax_decision(successor, a, b, index + 1, depth)

      val_and_action = [min(val_and_action[0], cur_val), action]
      b = min(b, val_and_action[0])
      if (val_and_action[0] < a):
        return val_and_action[0]
    return val_and_action[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def minimax_decision(self, gameState, index, depth):
    if index >= gameState.getNumAgents():
      index = 0
      depth += 1

    if depth == self.depth:
      return self.evaluationFunction(gameState)

    if index == 0:
      return self.max_value(gameState, index, depth)
    else:
      return self.min_value(gameState, index, depth)

    #return 'None'

  def max_value(self, gameState, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [float('-inf'), Directions.STOP]
    actions = gameState.getLegalActions(index)

    for action in actions:
      if action == Directions.STOP:
        continue

      successor = gameState.generateSuccessor(index, action)
      cur_val = self.minimax_decision(successor, index+1, depth)

      val_and_action = [max(val_and_action[0], cur_val), action]

    if depth == 0:
      return val_and_action[1]
    else:
      return val_and_action[0]

  def min_value(self, gameState, index, depth):
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    val_and_action = [0, Directions.STOP]
    actions = gameState.getLegalActions(index)

    expected = 0
    count = 0


    for action in actions:

      if action != Directions.STOP:
        successor = gameState.generateSuccessor(index, action)
        cur_val = self.minimax_decision(successor, index + 1, depth)
        val_and_action = [val_and_action[0], action]

        count += 1
        expected += cur_val



    return expected/count



  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return self.minimax_decision(gameState, 0, 0)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  cur_position = currentGameState.getPacmanPosition()
  cur_food_list = currentGameState.getFood().asList()
  cur_food_count = currentGameState.getNumFood()
  cur_ghost_states = currentGameState.getGhostStates()
  cur_capsules = currentGameState.getCapsules()
  cur_score = currentGameState.getScore()
  ghost_dist = []

  for ghost in cur_ghost_states:
    ghost_pos = ghost.getPosition()
    if cur_position == ghost_pos:
      return float('-inf') # it is really bad if pacman is hit by a ghost
    ghost_dist.append(manhattanDistance(cur_position, ghost_pos))  #total distance from ghosts, being further is good

  min_ghost_dist = max(ghost_dist)

  if cur_food_count == 0:
    return float('inf')  #if we take the last pellet that is really good

  total_food_dist = []
  for food_loc in cur_food_list:
    total_food_dist.append(manhattanDistance(cur_position, food_loc))

  min_food_dist = max(total_food_dist)

  total_cap_dist = []
  for cap in cur_capsules:
    total_cap_dist.append(manhattanDistance(cur_position, cap))

  recip_cap_dist = 0
  if len(total_cap_dist) != 0:
    total_cap_dist = max(total_cap_dist)
    recip_cap_dist = 1.0 / (total_cap_dist)

  num_ghosts = len(cur_ghost_states)
  recip_ghost_dist = 1.0/(min_ghost_dist)  # using average ghost dist
  recip_food_dist = 1.0/(min_food_dist)
  recip_food_count = 1.0/cur_food_count
  if ghost.scaredTimer == 0:
    recip_ghost_dist *= -1
  ret_val = cur_score + 20*recip_ghost_dist + 20*recip_food_dist + 5*recip_cap_dist

  return ret_val

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
