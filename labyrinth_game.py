from IPython.display import display
# coding: utf-8

# # Labyrinth game made on 27/02/2017 by Sarah Gross

# ## Requirements
# 
# ### A labyrith, represented as a matrix, is given. Starting from a given point, reach the way out without ever turning left.

# ## Matrice 

# In[88]:

matrix_dm = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
]

start_dm = (12,10)
end_dm = (12, 2)


# ## Class Maze
# 
# #### Defines a labyrinth from a matrix with a starting and ending point. Possesses a display function.


class Maze:
    def __init__(self, matrix, start, end) :
        self.matrix = matrix
        self.start = start
        self.end = end
        self.position = (10000000,1000000)
    
    def _repr_html_(self):
        return self.html_maze()
    
    def display_position(self, position) :
        self.position = position
        display(self)
    
    def html_maze(self) :
        size = len(self.matrix)
        base_style = "border: 1px solid black; margin: 0; height: 20px; width: 20px;"
        html = "<table>"
        for i in range(size) :
            html += "<tr>"
            for j in range(size) :
                style = base_style
                if self.end == (i,j) :
                    style += '; background-color: #f4ecb0'
                if self.start == (i,j) :
                    style += '; background-color: #ddf2da'
                if self.position == (i,j) :
                    style += '; background-color: #44d9ff'
                if self.matrix[i][j] == 1 :
                    style += "; background-color: grey"
                html += "<td style='"+ style+"'> </td>"

            html += "</tr>"
            
        html += "</table>"
        return html


# ## Class Player
# 
# #### Enables a player to be positionned and move around. We give him an initial position and direction, this class possesses moving functions (straight and right) in a labyrith passed as argument.

# Implementation of player movements

class Player:
    
    # Initialisation
    def __init__(self, start) :
        self.position = start
        self.direction = 'up'
    
    def can_go_straight(self, maze):
        matrix = maze.matrix
        if self.direction == 'up' :
            return (self.position[0] > 0 and matrix[self.position[0]-1][self.position[1]] == 0)

            
        elif self.direction == 'right' :
            return (self.position[1] < len(matrix)-1 and matrix[self.position[0]][self.position[1]+1] == 0)
        
        elif self.direction == 'down' :
            return (self.position[0] < len(matrix)-1 and matrix[self.position[0]+1][self.position[1]] == 0)
            
        else :
            return (self.position[1] > 0 and matrix[self.position[0]][self.position[1]-1] == 0)

    def go_straight(self, maze):
        matrix = maze.matrix
        if self.direction == 'up' :
            self.position = (self.position[0]-1,self.position[1])
            
        elif self.direction == 'right' :
            self.position = (self.position[0],self.position[1]+1)
        
        elif self.direction == 'down' :
            self.position = (self.position[0]+1,self.position[1])
            
        else :
            self.position = (self.position[0],self.position[1]-1)
            
    def can_go_right(self, maze):
        matrix = maze.matrix
        if self.direction == 'up' :
            return (self.position[1] < len(matrix)-1 and matrix[self.position[0]][self.position[1]+1] == 0)
            
        elif self.direction == 'right' :
            return (self.position[0] < len(matrix)-1 and matrix[self.position[0]+1][self.position[1]] == 0)
        
        elif self.direction == 'down' :
            return (self.position[1] > 0 and matrix[self.position[0]][self.position[1]-1] == 0)
            
        else :
            return (self.position[0] > 0 and matrix[self.position[0]-1][self.position[1]] == 0)

    def go_right(self, maze):
        matrix = maze.matrix
        if self.direction == 'up' :
            self.position = (self.position[0],self.position[1]+1)
            self.direction = 'right'
            
        elif self.direction == 'right' :
            self.position = (self.position[0]+1,self.position[1])
            self.direction = 'down'
        
        elif self.direction == 'down' :
            self.position = (self.position[0],self.position[1]-1)
            self.direction = 'left'
            
        else :
            self.position = (self.position[0]-1,self.position[1])
            self.direction = 'up'


# ## Class Game
# 
# #### Starts the labyrinth game by passing as argument at initialization time : the matrix, the starting and ending points.
# #### We lauch the game with play function. We go all the way up to the next intersection (and not just one by one step, otherwise we would have to write "straight" so many times).

# In[91]:

class Game :
    
    def __init__(self, maze) :
        self.maze = maze
        self.player = Player(maze.start)
        
    # Makes the player go in the direction in argument
    def go_verbose(self, direction) :
        if (direction == 'straight' or direction == 'S' or direction == 's') :
            if self.player.can_go_straight(self.maze) : 
                self.player.go_straight(self.maze)
                print("done\n")
            else :
                print("This direction is not possible. You can go : ")
                if self.player.can_go_right(self.maze) :
                    print("right ")
                else :
                    print("nowhere. You are blocked !!")
                print("\n")
            
        elif (direction == 'right' or direction == 'R' or direction == 'r'):
            if self.player.can_go_right(self.maze) : 
                self.player.go_right(self.maze)
                print("done\n")
            else :
                print("This direction is not possible. You can go : ")
                if self.player.can_go_straight(self.maze) :
                    print("straight ")
                else :
                    print("nowhere. You are blocked !!")
                print("\n")
        else :
            print("This direction is not allowed. Please pick straight or right.")
    
    # Draw our position in labyrinth
    def draw_position(self) :
        size = len(self.maze)
        string = "_" * (size+2) + "\n"
        for i in range(size) :
            string += "|"
            for j in range(size) :
                if self.player.position == (i,j) :
                    string += 'o'
                    continue
                if self.end == (i,j) :
                    string += '*'
                    continue
                if self.maze[i][j] == 0 :
                    string += " "
                else :
                    string += "#"
            string += "|\n"
        string += "_" * (size+2)
        print(string)
                
                
    def play(self) :
        print("Welcome to the Labyrith game ! \n You start at position ", self.maze.start, ". \n")
        self.maze.display_position(self.player.position)
        print("You can go straight or right by writing 'straight'/'s', 'right'/'r'. \n")
        print("To end the game, write 'end' or 'quit'. \n\n")
        not_end = True
        while(not_end) :
            action = input("\nNext action : \n")
            if (action == "end" or action == "quit"):
                not_end = False
            else :
                self.go_verbose(action)
                # Tant qu'on ne peut aller que tout droit pas besoin de demander l'avis de l'utilisateur
                while(self.player.can_go_straight(self.maze) and not self.player.can_go_right(self.maze)) :
                    self.player.go_straight(self.maze)
                self.maze.display_position(self.player.position)
            if self.player.position == self.maze.end :
                print("Congratulations !! You have reached the end of the maze !")
                not_end = False


# ## Test of the game

def game_labyrinth(matrix, start, end) :
    maze = Maze(matrix, start, end)
    game = Game(maze)
    game.play()


game_labyrinth(matrix_dm, start_dm, end_dm)

