
# coding: utf-8

# # Get the treasures in the maze with Djikstra !

# ### 1 ) Create a maze with random walls.  Probability about ~ 0.8 for having walls.
# ### 2 ) There are treasures in the maze. We have to get them as fast as possible => salesman traveller problem
# ### 3 ) Tournament between 2 players in the maze who must get as many treasures as possible (eventually by disturbing the opponent)

# ### 1)  Generate randomly a maze from a size-n graph with p probability of having holes

import random
from IPython.display import display
from math import sqrt, floor


def generate_maze_graph(n, p):
    g = {(i, j): set() for i in range(n) for j in range(n)}
    
    # Open Down on (i, j)
    for i in range(n-1):
        for j in range(n):
            if random.random() > p:
                g[(i, j)].add((i+1, j))
                g[(i+1, j)].add((i, j))
    
    # Open Right on (i, j)
    for i in range(n):
        for j in range(n-1):
            if random.random() > p:
                g[(i, j)].add((i, j+1))
                g[(i, j+1)].add((i, j))
    
    return g


# ### Symmetrical generating

# In[2]:

def generate_symmetric_graph(n, p):
    g = {(i, j): set() for i in range(n) for j in range(n)}
    
    # Open Down on (i, j)
    for i in range(n-1):
        for j in range(i,n):
            if random.random() > p:
                g[(i, j)].add((i+1, j))
                g[(i+1, j)].add((i, j))
                g[(j,i)].add((j, i+1))
                g[(j, i+1)].add((j, i))
    
    # Open Right on (i, j)
    for i in range(n):
        for j in range(i, n-1):
            if random.random() > p:
                g[(i, j)].add((i, j+1))
                g[(i, j+1)].add((i, j))
                g[(j,i)].add((j+1, i))
                g[(j+1, i)].add((j, i))
    
    return g


# Test

graph_dm = generate_symmetric_graph(15,0.3)
print(graph_dm)


# ### Generate the trasures to find

def generate_objects(graph, size, number) :
    listObjects = []
    while len(listObjects) < number :
        line = random.randrange(0,size)
        col = random.randrange(0,size)
        listNeighbours = []
        if line > 0 :
            listNeighbours.append((line-1,col))
        if col > 0 :
            listNeighbours.append((line,col-1))
        if line < size-1 :
            listNeighbours.append((line+1,col))
        if col < size-1 :
            listNeighbours.append((line,col+1))
        if all(x in graph[(line,col)] for x in listNeighbours) :
            listObjects.append((line,col))
    return listObjects
        


# ## Class Maze
# 
# #### Creates a maze from a graph. Possesses a Display function

class Maze:
    def __init__(self, graph, size) :
        self.graph = graph
        self.position = (size-1,0)
        self.objects = generate_objects(graph,size,10)
    
    def _repr_html_(self):
        return self.html_maze()

    def html_maze(self):
        size = floor(sqrt(len(self.graph)))
        base_style = "border: 1px solid black; margin: 0; height: 20px; width: 20px"
        html = "<table> <tr>"

        for i in range(size):
            for j in range(size):
                
                style = base_style
                children = self.graph[(i,j)]

                for (io, jo) in children :
                    if (io,jo) == (i+1,j) :
                        style += '; border-bottom: 1px solid white'
                    if (io,jo) == (i,j+1) :
                        style += '; border-right: 1px solid white'
                    if (io,jo) == (i-1,j) :
                        style += '; border-top: 1px solid white'
                    if (io,jo) == (i,j-1) :
                        style += '; border-left: 1px solid white'

                if self.position == (i,j) :
                    style += '; background-color: #44d9ff'
                        
                if(i,j) in self.objects :
                    style += '; background-color: yellow'

                html += "<td style='"+ style+"'> </td>"

            html += "</tr>"
        html += "</html>"
        return html


# Test

maze = Maze(graph_dm,15)
print(maze.objects)
display(maze)


# ### 2) Programming player A who will try to get the fastest the superior half of the treasures
# #### a) Calculate the shortest paths between [position initiale + positions de tous les objets]. Use RFW ou N-Dijkstra
# #### b) Calculate "a kind of" salesman problem on these paths (because not all treasures will be taken into account)


# You can use global variable to save information for your next move call
to_do_path = []


# Djikstra Algorithm
def get_distances(graph, my_position):
    # Initialisation
    # all_nodes = [(i, j) for i in range(graph.n) for j in range(graph.n)]
    to_check = set(list(graph.keys()))
    distances = {x : float("inf") for x in graph}
    distances[my_position] = 0
    predecessors = {}
    
    while len(to_check) > 0:
        a = min(list(to_check), key=lambda x: distances[x])
        to_check.remove(a)
        
        # for b in graph.neighbours(a) :
        for b in graph[a] :
            if b in to_check :
                if distances[a]+1 < distances[b] :
                    distances[b] = distances[a]+1
                    predecessors[b] = a
        
    return (distances, predecessors);
    
# Create the path from a start point to an end point (without start point)
def make_path_from_distances(distances, predecessors, start, end) :
    path = []
    current_point = end
    while current_point != start :
        path.append(current_point)
        current_point = predecessors[current_point]
    return path[::-1]
    
    
# Uses a Gluton strategy
def next_move(graph, points, my_path, enemy_path):
    global to_do_path

    # graph: an object representing the maze
    #   graph.n : size of the maze
    #   call graph.neighbours((i, j)) to get possible moves from a position (i, j)
    # points: list of positions of remaining points to collect
    # my_path: list of positions you have been to until now (my_path[-1] is your current position)
    # enemy_path: list of positions your enemy have been to until now.

    # return your next move. Should be one of graph.neighbours(my_path[-1])
        
    # If I am on my way to get a treasure and this treasure has not been taken yet by my opponent
    if len(to_do_path) > 0 and to_do_path[-1] in points:
        my_next_point = to_do_path[0]
        del(to_do_path[0])
        
    else:
        (my_d, my_p) = get_distances(graph, my_path[-1])
        (enemy_d, enemy_p) = get_distances(graph, enemy_path[-1])
        
        my_next_targets = sorted(points, key = lambda x : my_d[x])
        enemy_next_target = min(points, key = lambda x : enemy_d[x])
        
        # Si le plus proche de moi est encore plus proche de mon adversaire : je vais au point suivant
        if len(points) > 1 and my_next_targets[0] == enemy_next_target and my_d[my_next_targets[0]] < enemy_d[enemy_next_target] :
            to_do_path = make_path_from_distances(my_d, my_p, my_path[-1], my_next_targets[1])
        
        else :
            to_do_path = make_path_from_distances(my_d, my_p, my_path[-1], my_next_targets[0])
            
        #print(enemy_next_target)
        my_next_point = to_do_path[0]
        del(to_do_path[0])
    
    return(my_next_point)

# Test
next_move(maze.graph, [(10, 10), (2, 2), (9, 4), (1, 0), (3, 7), (6, 14), (6, 1)]
, [(14,0),(14,1),(14,2),(13,2),(13,3),(13,4),(14,4),(14,5),(14,6),(13,6),(13,7),(13,8)], [(0,14),(0,13)])



