import turtle
import math
import random


# ============================================================
#                         GAME SETUP
# ============================================================

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

GRID_SIZE = 24
MAZE_OFFSET = -288

START_LIVES = 3

# Game states
START = "start"
PLAYING = "playing"
GAME_OVER = "game_over"
COMPLETE = "complete"

game_state = START


# ============================================================
#                         SCREEN
# ============================================================

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Quiz")
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.tracer(0)


# ============================================================
#                           MAZE
# ============================================================

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


# ============================================================
#                       QUESTION BANK
# ============================================================

questions = [
    ("What is 1010 in denary?", "10", 50),
    ("What is 1111 in denary?", "15", 50),
    ("What is 5 in 4-bit binary?", "0101", 50),
    ("What is 10 in 4-bit binary?", "1010", 50),
    ("What does CPU stand for?", "central processing unit", 50),
    ("What does RAM stand for?", "random access memory", 50),
    ("What does WWW stand for?", "world wide web", 50),
    ("What does HTML stand for?", "hypertext markup language", 50),
]


# ============================================================
#                       PEN / WALL CLASS
# ============================================================

class Pen(turtle.Turtle):

    def __init__(self):
        super().__init__()

        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


# ============================================================
#                         COIN CLASS
# ============================================================

class Coin(turtle.Turtle):

    def __init__(self, x, y, value):
        super().__init__()

        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)

        self.value = value

        self.goto(x, y)

    def destroy(self):
        self.hideturtle()
        self.goto(2000, 2000)


# ============================================================
#                        PLAYER CLASS
# ============================================================

class Player(turtle.Turtle):

    def __init__(self):
        super().__init__()

        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)

        self.score = 0
        self.lives = START_LIVES

    # --------------------------------------------------------
    # Move player
    # --------------------------------------------------------

    def move(self, dx, dy):

        new_x = self.xcor() + dx
        new_y = self.ycor() + dy

        # Prevent movement through walls
        if (new_x, new_y) not in walls:

            self.goto(new_x, new_y)

    def go_up(self):
        self.move(0, GRID_SIZE)

    def go_down(self):
        self.move(0, -GRID_SIZE)

    def go_left(self):
        self.move(-GRID_SIZE, 0)

    def go_right(self):
        self.move(GRID_SIZE, 0)

    # --------------------------------------------------------
    # Collision detection
    # --------------------------------------------------------

    def is_collision(self, other):

        distance = math.sqrt(
            (self.xcor() - other.xcor()) ** 2 +
            (self.ycor() - other.ycor()) ** 2
        )

        return distance < 5

    # --------------------------------------------------------
    # Reset player statistics
    # --------------------------------------------------------

    def reset_stats(self):

        self.score = 0
        self.lives = START_LIVES


# ============================================================
#                         GAME CLASS
# ============================================================

class MazeQuiz:

    def __init__(self):

        self.pen = Pen()
        self.player = Player()

        self.walls = []
        self.coins = []

        self.used_questions = []

        self.hud = turtle.Turtle()
        self.hud.hideturtle()
        self.hud.penup()
        self.hud.color("white")

        self.message = turtle.Turtle()
        self.message.hideturtle()
        self.message.penup()
        self.message.color("white")

    # --------------------------------------------------------
    # Clear maze
    # --------------------------------------------------------

    def clear_maze(self):

        for coin in self.coins:
            coin.destroy()

        self.coins.clear()
        self.walls.clear()

        self.pen.clear()

    # --------------------------------------------------------
    # Convert maze coordinates
    # --------------------------------------------------------

    def get_screen_position(self, x, y):

        screen_x = MAZE_OFFSET + (x * GRID_SIZE)
        screen_y = -MAZE_OFFSET - (y * GRID_SIZE)

        return screen_x, screen_y

    # --------------------------------------------------------
    # Set up maze
    # --------------------------------------------------------

    def setup_level(self):

        self.clear_maze()

        for y in range(len(level_1)):

            for x in range(len(level_1[y])):

                character = level_1[y][x]

                screen_x = MAZE_OFFSET + (x * GRID_SIZE)
                screen_y = 288 - (y * GRID_SIZE)

                # Wall
                if character == "X":

                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()

                    self.walls.append(
                        (screen_x, screen_y)
                    )

                # Player starting position
                elif character == "P":

                    self.player.goto(
                        screen_x,
                        screen_y
                    )

                # Coin
                elif character == "C":

                    coin = Coin(
                        screen_x,
                        screen_y,
                        50
                    )

                    self.coins.append(coin)

        self.update_hud()

        wn.update()

    # --------------------------------------------------------
    # Ask question
    # --------------------------------------------------------

    def ask_question(self):

        available_questions = [
            q for q in questions
            if q not in self.used_questions
        ]

        # If all questions have been used, allow them again
        if not available_questions:

            self.used_questions.clear()
            available_questions = questions

        question, correct_answer, question_value = random.choice(
            available_questions
        )

        self.used_questions.append(
            (question, correct_answer, question_value)
        )

        answer = wn.textinput(
            "Maze Quiz",
            question
        )

        if answer is not None:

            answer = answer.strip().lower()
            correct_answer = correct_answer.strip().lower()

            if answer == correct_answer:

                self.player.score += question_value

                self.show_message(
                    "Correct! +{} points".format(question_value)
                )

            else:

                self.player.lives -= 1

                self.show_message(
                    "Incorrect! The answer was: {}".format(
                        correct_answer
                    )
                )

        # Restore keyboard focus
        wn.getcanvas().focus_force()
        wn.listen()

    
    # --------------------------------------------------------
    # Check coin collisions
    # --------------------------------------------------------

    def check_coin_collision(self):

        for coin in self.coins[:]:

            if self.player.is_collision(coin):

                self.ask_question()

                coin.destroy()

                self.coins.remove(coin)

                self.update_hud()

                return

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    def update_hud(self):

        self.hud.clear()

        self.hud.goto(-330, 315)

        self.hud.write(
            "Score: {}    Lives: {}    Coins: {}".format(
                self.player.score,
                self.player.lives,
                len(self.coins)
            ),
            font=("Arial", 14, "bold")
        )

    # --------------------------------------------------------
    # Display temporary message
    # --------------------------------------------------------

    def show_message(self, text):

        self.message.clear()

        self.message.goto(0, -325)

        self.message.write(
            text,
            align="center",
            font=("Arial", 14, "bold")
        )

        wn.update()

        # Keep message visible briefly
        wn.ontimer(
            self.clear_message,
            1500
        )

    def clear_message(self):

        self.message.clear()

    # --------------------------------------------------------
    # Check if game is complete
    # --------------------------------------------------------

    def check_game_complete(self):

        if len(self.coins) == 0:

            self.game_complete()

    # --------------------------------------------------------
    # Game over
    # --------------------------------------------------------

    def game_over(self):

        global game_state

        game_state = GAME_OVER

        self.clear_maze()

        self.hud.clear()

        self.player.hideturtle()

        self.message.clear()

        self.message.goto(0, 80)

        self.message.write(
            "GAME OVER",
            align="center",
            font=("Arial", 32, "bold")
        )

        self.message.goto(0, 25)

        self.message.write(
            "Final Score: {}".format(
                self.player.score
            ),
            align="center",
            font=("Arial", 18, "normal")
        )

        self.message.goto(0, -25)

        self.message.write(
            "Press R to restart",
            align="center",
            font=("Arial", 16, "normal")
        )

        wn.update()

    # --------------------------------------------------------
    # Complete game
    # --------------------------------------------------------

    def game_complete(self):

        global game_state

        game_state = COMPLETE

        self.clear_maze()

        self.hud.clear()

        self.player.hideturtle()

        self.message.clear()

        self.message.goto(0, 80)

        self.message.write(
            "CONGRATULATIONS!",
            align="center",
            font=("Arial", 28, "bold")
        )

        self.message.goto(0, 25)

        self.message.write(
            "You completed the Maze Quiz!",
            align="center",
            font=("Arial", 18, "normal")
        )

        self.message.goto(0, -25)

        self.message.write(
            "Final Score: {}".format(
                self.player.score
            ),
            align="center",
            font=("Arial", 18, "normal")
        )

        self.message.goto(0, -75)

        self.message.write(
            "Press R to play again",
            align="center",
            font=("Arial", 16, "normal")
        )

        wn.update()

    # --------------------------------------------------------
    # Start game
    # --------------------------------------------------------

    def start_game(self):

        global game_state

        game_state = PLAYING

        self.message.clear()

        self.player.reset_stats()
        self.player.showturtle()

        self.used_questions.clear()

        self.setup_level()

        wn.getcanvas().focus_force()
        wn.listen()

    # --------------------------------------------------------
    # Start screen
    # --------------------------------------------------------

    def show_start_screen(self):

        self.message.clear()

        self.message.goto(0, 120)

        self.message.write(
            "MAZE QUIZ",
            align="center",
            font=("Arial", 32, "bold")
        )

        self.message.goto(0, 65)

        self.message.write(
            "Collect coins and answer computing questions!",
            align="center",
            font=("Arial", 15, "normal")
        )

        self.message.goto(0, 20)

        self.message.write(
            "Use the arrow keys to move.",
            align="center",
            font=("Arial", 15, "normal")
        )

        self.message.goto(0, -25)

        self.message.write(
            "Correct answers earn points.",
            align="center",
            font=("Arial", 15, "normal")
        )

        self.message.goto(0, -70)

        self.message.write(
            "You have 3 lives.",
            align="center",
            font=("Arial", 15, "normal")
        )

        self.message.goto(0, -130)

        self.message.write(
            "Press ENTER to start",
            align="center",
            font=("Arial", 18, "bold")
        )

        wn.update()

    # --------------------------------------------------------
    # Restart game
    # --------------------------------------------------------

    def restart(self):

        self.start_game()


# ============================================================
#                       CREATE GAME
# ============================================================

game = MazeQuiz()

# The player uses the game's wall list
walls = game.walls


# ============================================================
#                       KEYBOARD INPUT
# ============================================================

def move_up():

    if game_state == PLAYING:
        game.player.move(
            0,
            GRID_SIZE
        )


def move_down():

    if game_state == PLAYING:
        game.player.move(
            0,
            -GRID_SIZE
        )


def move_left():

    if game_state == PLAYING:
        game.player.move(
            -GRID_SIZE,
            0
        )


def move_right():

    if game_state == PLAYING:
        game.player.move(
            GRID_SIZE,
            0
        )


def start():

    if game_state == START:
        game.start_game()


def restart():

    if game_state in (GAME_OVER, COMPLETE):
        game.restart()


# ============================================================
#                       KEY BINDINGS
# ============================================================

wn.listen()

wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(move_up, "Up")
wn.onkey(move_down, "Down")

wn.onkey(start, "Return")
wn.onkey(restart, "r")


# ============================================================
#                         START SCREEN
# ============================================================

game.show_start_screen()


# ============================================================
#                       MAIN GAME LOOP
# ============================================================

def game_loop():

    wn.listen()

    if game_state == PLAYING:

        # Check whether player collected a coin
        game.check_coin_collision()

        # Check whether player has lost all lives
        if game.player.lives <= 0:

            game.game_over()

        # Check whether all coins have been collected
        elif len(game.coins) == 0:

            game.check_game_complete()

    wn.update()

    # Run the game loop again
    wn.ontimer(game_loop, 50)


game_loop()

wn.mainloop()
