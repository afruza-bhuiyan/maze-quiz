#setting the maze
import turtle
import math
import random

wn = turtle.Screen()#show a window turtle screen
wn.bgcolor("black")#sets background colour as black
wn.title("Maze Quiz")#names the window 
wn.setup(700,700)#sets the size of the window
wn.tracer(0)

#questions
def questions():
    questions = ["1", "2", "3", "4", "5"]
    questions[random.randint(0, len(questions)-1)] = "question"
    if questions == ["question", "2", "3", "4", "5"]:
        question = 1
    elif questions == ["1", "question", "3", "4", "5"]:
        question = 2
    elif questions == ["1", "2", "question", "4", "5"]:
        question = 3
    elif questions == ["1", "2", "3", "question", "5"]:
        question = 4
    elif questions == ["1", "2", "3", "4", "question"]:
        question = 5
    #cycling through questions and checking answers (adds point if correct)
    if question == 1:
        ans1=input("What is 0001+0001 in denary? ")
        if ans1 == ("0010"):
            player.gold += coin.gold
            print ("Player Gold: {}".format(player.gold))
        else:
            print("Player Gold: {}".format(player.gold))
    elif question == 2:
        ans2=input("What is 15 in 4-bit binary? ")
        if ans2 == ("1111"):
            player.gold += coin.gold
            print ("Player Gold: {}".format(player.gold))
        else:
            print("Player Gold: {}".format(player.gold))
    elif question == 3:
        ans3=input("What does WWW stand for in computing? ")
        if ans3 == ("world wide web"):
            player.gold += coin.gold
            print ("Player Gold: {}".format(player.gold))
        else:
            print("Player Gold: {}".format(player.gold))
    elif question == 4:
        ans4=input("What is 1010 in denary? ")
        if ans4 == ("10"):
            player.gold += coin.gold
            print ("Player Gold: {}".format(player.gold))
        else:
            print("Player Gold: {}".format(player.gold))
    else:
        ans5=input("What is 0101+0101 in denary? ")
        if ans5 == ("1010"):
            player.gold += coin.gold
            print ("Player Gold: {}".format(player.gold))
        else:
            print("Player Gold: {}".format(player.gold))

#create pen
class Pen(turtle.Turtle): #creates a class called pen as turtle
    def __init__(self): #refers to the object
        turtle.Turtle.__init__(self)#initialise the object
        self.shape("square")#makes the shape of the maze walls square
        self.color("white")#makes the colour of the walls white
        self.penup()#don't show line
        self.speed(0)#animation speed (fastest)

#create player
class Player(turtle.Turtle): #creates a class called pen as turtle
    def __init__(self): #refers to the object itself
        turtle.Turtle.__init__(self)#initialise the object
        self.shape("square")#makes the shape of the maze walls square
        self.color("blue")#makes the square blue
        self.penup()#don't show lines
        self.speed(0)#animation speed (fastest)
        self.gold=0

    def go_up(self):#defined go up
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24 #add 24 to the y coordinate

        #check if the space has a wall
        if (move_to_x, move_to_y) not in walls: # if there is no wall on x,y 
            self.goto(move_to_x, move_to_y)#go to x,y coordinates

    def go_down(self):#defined go down
        #calculate spot to move 
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24 #minus 24 from the y coordinate

        #check if the space has a wall
        if (move_to_x, move_to_y) not in walls: # if there is no wall on x,y 
            self.goto(move_to_x, move_to_y)#go to x,y coordinates

    def go_right(self):#defined go right
        #calculate spot to move 
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()#add 24 to the x coordinate

        #check if the space has a wall
        if (move_to_x, move_to_y) not in walls: # if there is no wall on x,y 
            self.goto(move_to_x, move_to_y)#go to x,y coordinates

    def go_left(self):#defined go left
        #calculate spot to move 
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor() #minus from to the x coordinate

        #check if the space has a wall
        if (move_to_x, move_to_y) not in walls: # if there is no wall on x,y 
            self.goto(move_to_x, move_to_y)#go to x,y coordinates

    def is_collision(self, other):#defines collision of another object with itself
        a = self.xcor()-other.xcor()#a is the x coordinates of self-other
        b = self.ycor()-other.ycor()#b is the y coordinates of self-other
        distance = math.sqrt((a ** 2) + (b ** 2))#distance set as math square root

        if distance < 5: # if the distance is less than 5
            return True #return as it has collided
        else: #if not
            return False#return as not collided 

#create coin
class Coin(turtle.Turtle): #creates a class called coin as turtle
    def __init__(self, x, y): #refers to the object
        turtle.Turtle.__init__(self)#initialise the object
        self.shape("circle")#makes the shape of the coin circles
        self.color("gold")#makes the colour of the coin gold
        self.penup()#don't show line
        self.speed(0)#animation speed (fastest)
        self.gold = 100#assigns 100 points to the coin
        self.goto(x, y)#goes to the coordinate

    def destroy(self):#creates a class called destroy in itself
        self.goto(2000,2000) #couldn't destroy it so moved off the screen
        self.hideturtle()#hides the coin

#create levels list
levels = [""]

#define level 1
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXX      XXXX CX",
"X  XXXXXXXX  XXXXXXXX  X",
"X        XX  XXXXXXXX  X",
"X        XX  XXX       X",
"XXXXXXX  XX  XXX  XXXXXX",
"XXXXXXX  XX  XXX  XXXXXX",
"XC XXXX  XX  XXX  XXXXXX",
"X  XXXX           XXXXXX",
"X        XXXXXXXXXXXXXXX",
"X            XXXXXXXXXXX",
"XXXXXXXXX    XXXXXX   CX",
"XXXXXXXXXX   XXXXXX    X",
"XXX  XXXXX   XXXXXXX   X",
"XXX                    X",
"XXX       XXXXXXXXXXXXXX",
"XXXXXXX   XXXXXXXXXXXXXX",
"XXXXXXXX   XXXXXXXX  CXX",
"XXX CXXX   XXXXXXXX   XX",
"XX   XXX   XXXXXXX   XXX",
"XX                    XX",
"XXXX    XXXXXXXXXXXXXXXX",
"XXXX    XXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXX",
]

#add coins list
coins = []

#add maze to maze list
levels.append(level_1)

#create level setup function
def setup_maze(level):#define setup_maze as
    for y in range(len(level)):#for every row in the level
        for x in range(len(level[y])):#for every line in each rows
            #get character at each x,y coordinate
            character = level[y][x]
            #calculate the screen x, y coordinates
            screen_x = -288 + (x*24)#the formula for calculating x-coordinate
            screen_y = 288 - (y*24)#the formula for calculating y-coordinate

            #check if it is an X(representing a wall)
            if character =="X":#if the character is X
                pen.goto(screen_x, screen_y)#go to that coordinate
                pen.stamp()#place a white square
                #add coordinates to wall list
                walls.append((screen_x, screen_y))

             #check if it is P(player)
            if character == "P":#if the character is P
                player.goto(screen_x, screen_y)#go and put there

            #check if it is a C(coin)
            if character =="C":#if the character is C
                coins.append(Coin(screen_x, screen_y))#go and put there

#create class instances
pen = Pen()
player = Player()

#create wall coordinate list
walls = [] 

#set up the level
setup_maze(levels[1])

#keyboard steps
turtle.listen()
turtle.onkey(player.go_left,"Left")#go left on player class moves to the left
turtle.onkey(player.go_right,"Right")#go right on player class moves to the right
turtle.onkey(player.go_up,"Up")#go up on player class moves up
turtle.onkey(player.go_down,"Down")#go down on player class moves down

#turn off screen updates
wn.tracer(0)#stops code animation

#main game loop
while True:
    #check for player collision with coin
    #iterate through coin list
    for coin in coins[:]:
        if player.is_collision(coin):
            #ask a question
            questions()
            #destroy the coin
            coin.destroy()
            #remove the coin from the coin list
            coins.remove(coin)
    #update screen
        
    wn.update()
