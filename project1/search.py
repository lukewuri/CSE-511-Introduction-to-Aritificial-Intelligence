# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        # type: () -> object
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    fringe = util.Stack()
    fringe.push((problem.getStartState(), [], []))

    node = problem.getStartState()
    if problem.isGoalState(node):
        return [node]
    frontier = util.Stack()
    explored = []
    frontier.push((node, [], []))

    while True:
        if frontier.isEmpty():
            return []  # Failure
        node, direction_list, path = frontier.pop()
        explored.append(node)
        if problem.isGoalState(node):
            return direction_list
        for position, direction, weight in problem.getSuccessors(node):

            if position not in path and position not in explored:
                frontier.push((position, direction_list + [direction], path + [node]))


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "* YOUR CODE HERE *"

    node = problem.getStartState()
    if problem.isGoalState(node):
        return [node]
    frontier = util.Queue()
    explored = []
    frontier.push((node, [], 0))

    while True:
        if frontier.isEmpty():
            return []  # Failure
        node, direction_list, path_cost = frontier.pop()
        if node not in explored:
            explored.append(node)
            for position, direction, cost in problem.getSuccessors(node):
                if position not in explored:
                    if problem.isGoalState(position):
                        return direction_list + [direction]
                    frontier.push((position, direction_list + [direction], path_cost + cost))



def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "* YOUR CODE HERE *"
    node = (problem.getStartState(), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(node, 0)
    explored = []

    while True:
        if frontier.isEmpty():
            return []  # Failure
        node, direction_list, path_cost = frontier.pop()
        if problem.isGoalState(node):
            return direction_list
        if node not in explored:
            explored.append(node)
            for position, direction, cost in problem.getSuccessors(node):
                frontier.push((position, direction_list + [direction], path_cost + cost), path_cost + cost)

            #we can just do this because we cant remove from our PQ



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "* YOUR CODE HERE *"
    node = (problem.getStartState(), [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []
    frontier = util.PriorityQueue()
    frontier.push(node, heuristic(problem.getStartState(), problem))
    explored = []
    while True:
        if frontier.isEmpty():
            return []  # Failure
        node, direction_list, path_cost = frontier.pop()
        if problem.isGoalState(node):
            return direction_list
        if node not in explored:
            explored.append(node)
            for position, direction, cost in problem.getSuccessors(node):
                total_cost = cost + path_cost
                frontier.push((position, direction_list + [direction], total_cost), total_cost + heuristic(position, problem))




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
