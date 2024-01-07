from tkinter import *
from random import randint
import numpy as np
import time
import winsound

# some constants
COLORS = ['white', 'maroon', 'red', 'yellow', 'grey', 'white']
EMPTY = 0
BODY = 1
FOOD = 2
HEAD = 3
WALL = 4

# board
BOARD = np.array([
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])

HEIGHT = len(BOARD)
WIDTH = len(BOARD[0])
# Array that represents the snake. First element is the head of snake.


while True:
    Snake_intital_body = randint(1, HEIGHT - 1)
    if BOARD[Snake_intital_body, Snake_intital_body] == 0 and BOARD[Snake_intital_body, Snake_intital_body + 1] == 0:
        default_location = [(Snake_intital_body, Snake_intital_body), (Snake_intital_body, Snake_intital_body + 1)]
        break

while True:
    food = (randint(1, HEIGHT - 1), randint(1, HEIGHT - 1))
    if BOARD[food[0], food[1]] == 0:
        break

# Initial position of the snake and food
# checks if the spawn points are empty spaces on the board only then they are allowed


CELL_WIDTH = 32
width = WIDTH * CELL_WIDTH
height = HEIGHT * CELL_WIDTH
# GUI Parameters

# functions to get every direction of position x
LEFT = lambda x: (x[0], x[1] - 1)
RIGHT = lambda x: (x[0], x[1] + 1)
UP = lambda x: (x[0] - 1, x[1])
DOWN = lambda x: (x[0] + 1, x[1])


# snake class
class Snake:
    def __init__(self, board, locations=default_location, virtual=False):

        self.locations = locations
        self.board = board
        self.virtual = virtual
        self.score = 0

    def play(self):
        winsound.PlaySound("RokuSnakeOST.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
        #winsound.PlaySound("ImperialMarch60.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

        powerlevel = 0

        while self.alive():  # checks if alive#

            if not ( self.is_the_path_safe()):  # if no path to food and its not safe to eat then chase tail#
                movement = self.tail_search()
                powerlevel += 1
                # print("paths ran around", run)
            else:  # chase food if safe and safe to eat#
                # print("food safe", run)
                movement = self.food_search()
            print(powerlevel)

            if powerlevel > 9000: #the powerlevel can't be over 9000#
                break

            self.change_positions(movement)

        # Create a StringVar object to store a string value
        var = StringVar()
        # Create a Label widget with some attributes, including the textvariable set to var
        label = Label(banana, textvariable=var, relief=RIDGE, bd=5, padx=5, pady=5, bg="light green")
        # Set the value of var to self.score using the set() method
        var.set(self.score)
        # Pack the Label widget into the banana window
        label.pack()

        print('Score: ', self.score)

    def is_there_valid_path(self, head, goal):
        valid_path = False
        # assume there is not

        result = self.a_star_algorithm(goal)
        # find all the valid moves to the source

        for d in self.possible_moves_list(head):

            if result[d(head)] > 0:
                valid_path = True

        # if there are any possible moves
        # return true
        return valid_path

    def is_the_path_safe(self):
        # basically check if we take this path to eat food
        # will snake survive
        global food

        virtual_environment = self.board.copy()  # copying the board#

        food_pos = food  # storing the location of the food#

        virtual_locations = []

        for l in self.locations:
            virtual_locations.append(l)

        virtual_snake = Snake(virtual_environment, virtual_locations,
                              virtual=True)  # creates a new instance of the Snake class, with the following arguments to check the moves of the virtualy snake without actually moving the snake#

        while virtual_snake.alive() and food_pos == food:  # while food is not eaten and the snake is alive we will chase the food and move the virtual snake in that direction#

            m = virtual_snake.food_search()

            virtual_snake.change_positions(m)

        food = food_pos  # food location is same as previously#

        if not (virtual_snake.is_there_valid_path(virtual_snake.head(),
                                                  virtual_snake.tail())):  # to check if the snake dies or not#
            return False
        else:
            return True

    def a_star_algorithm(self, source):
        # alot of it is similar to the bfs code but with heuristics

        # source represents the starting position of the search.
        global food
        result = self.board.copy()
        result[result != 0] = -1
        # sets value as -1 if it's not empty

        distance = 0

        queue = []

        queue.append(source)
        # keep track of the cells that need to be visited

        visited = set()

        while len(queue) > 0:
            position = queue.pop(0)
            
            visited.add(position)
            # marks the goal as an visited position

            distance += 1

            for d in self.possible_moves_list(position):

                # if move isn't done already, add it to visited and update the distance
                if d(position) not in visited:

                    queue.append(d(position))
                    visited.add(d(position))
                    result[d(position)] = distance


        # return grid with shortest path distances from source
        return result

    def tail_search(self):
        distances = self.a_star_algorithm(self.tail())  # the snake tries to find it tail applying A* algorithmn#

        max_distance = -float("inf")

        head_loc = self.head()  # storing head#

        longest_move = None

        for d in self.possible_moves_list(head_loc):  # gets all the moves it can go#

            current_dis = distances[d(head_loc)]  # gets the longest path to the tail #

            if current_dis > max_distance:
                max_distance = current_dis
                longest_move = d

        return longest_move

    def food_search(self):
        distances = self.a_star_algorithm(food)  # stores the shortest direction of the food#

        head_loc = self.head()

        shortest_move = None

        min_distance = float("inf")

        for d in self.possible_moves_list(head_loc):

            current_dis = distances[d(head_loc)]  # the distance of the nearest food item from the head of the snake#

            if min_distance > current_dis:  # gets the shortest distance#
                min_distance = current_dis
                shortest_move = d

        return shortest_move

    # move one step forward the given direction
    def change_positions(self, direction):
        head_loc = self.head()
        tail_loc = self.tail()

        head = [direction(head_loc)]  # gives the new row and column value of the head #

        self.board[tail_loc] = 0  # making the location of the tail empty on the board as we move the tail#

        temp_tail = tail_loc  # setting the value of the tail#
        # move the snake
        self.locations = head + self.locations[
                                :-1]  # saving the values of the head till the second last value of the snakes body#

        if head_loc == food:
            self.locations = self.locations + [temp_tail]
            # the snake grow one block by adding tail to the snakes body

            self.make_food()
            # regenerate the food

            self.score += 1
            # incrementing score#


        self.update_board()  # updates the board#

    # update board
    def update_board(self):
        for body_part in self.locations:
            # for every piece of the body this loop runs#
            self.board[body_part] = 1
            # updates the body of the snake#

        self.board[self.head()] = 3  # updates the head#
        self.board[food] = 2  # updates the food#

        if not self.virtual:  # if board is not virtual it will update the map
            self.update_canvas()

    # validate a movement
    def possible_moves_list(self, location):
        # list to store possible moves
        movement = []
        # loop through the possible moves and add to list of it is valid
        for d in [LEFT, RIGHT, UP, DOWN]:
            # if location doesnt exceeds boards size limits, then valid
            if not ((location[0] >= len(self.board)) or (location[1] >= len(self.board[0])) or (location[0] < 0) or (
                    location[1] < 0)):
                next_loc = self.board[d(location)]
                # validate move if the next_loc val is empty or food
                if next_loc == 0 or next_loc == 2:
                    movement.append(d)
        # return list of valid moves
        return movement

    # place food randomly
    def make_food(self):
        # pick the global variable of food
        global food
        flag = True
        # keep on generating a position for the food, until you get a open location
        while flag:
            location_food = (randint(0, HEIGHT - 1),
                             randint(0, WIDTH - 1))  # finding the location of the food within the range of the board#
            if self.board[
                location_food] == 0:  # checking to see if the location isnt a wall or the body of the snake itself#
                food = location_food
                flag = False

    def alive(self):
        # if the amount of valid moves is greater than zero, then the snake is alive
        head = self.head()
        movement_available = len(self.possible_moves_list(head))
        if movement_available != 0:
            return True
        else:
            False

    def head(self):
        # tells position of head
        return self.locations[0]

    def tail(self):
        # tells position of tail
        return self.locations[-1]

    # draw GUI
    def update_canvas(self):

        canvas.delete('all')
        # Clear the canvas by deleting all items on it

        canvas.config(width=width, height=height)
        # Set the size of the canvas dimensions

        for i in range(WIDTH):
            # Loop through the rows of the board

            for j in range(HEIGHT):
                # Loop through the columns of the board

                x_val = i * CELL_WIDTH
                y_val = j * CELL_WIDTH
                # calc the x + y coordinates for the top left corner of the cell

                current_pos = self.board[j][i]
                # Get current cell val on the board

                color = COLORS[current_pos]
                # Get the color for the current cell based on value

                canvas.create_rectangle(x_val, y_val, x_val + CELL_WIDTH, y_val + CELL_WIDTH, fill=color,
                                        outline='white')
                # Create a rectangle on canvas for the current cell
                # with the specified dimensions

        # Update canvas to show the new items that were added
        canvas.update()


if __name__ == '__main__':
    banana = Tk()
    banana.title('AI Chasing Snake')
    # create the main window and name it

    canvas = Canvas(banana, bg="black")
    canvas.pack()
    # create a canvas and present in the main window

    main_snake = Snake(BOARD)
    main_snake.play()
    # apply the Snake class to main_snake and call it

    winsound.PlaySound("The Price is Right Losing Horn - Sound Effect (HD).wav", winsound.SND_ASYNC)
    # close the main window and ustilise the ending sound
    banana.mainloop()