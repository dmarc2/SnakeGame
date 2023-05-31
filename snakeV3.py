import random as rand
import time
import pygame

BLOCK_SIZE = 20
START_COORDS = [(10,15), (9,15), (8,15)]    #The starting coordinates of the snake's initial 3 body parts
FONT_SIZE = 25
ROOTW = 600         #Width of the window 
ROOTH = 650         #Height of the window 
CANVASW = 600       #Width of the canvas
CANVASH = 600       #Height of the canvas
labelInitX = ROOTW/2
labelInitY = 0
scoreXOffset = -30
highscoreXOffset = -60

#This class is used to represent the blocks in the game
# such as the snake's body parts and the food
class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    #Function to draw a block
    def draw(self, surface:pygame.Surface):
        pygame.draw.rect(surface, self.color, (self.x*BLOCK_SIZE, self.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

#this class is the object for the food.
class Food(Block):
    def __init__(self, color):
        super().__init__(rand.randint(0, CANVASW/BLOCK_SIZE - 1),rand.randint(0, CANVASH/BLOCK_SIZE - 1),color)

#This class is the object for the snake.
class Snake:
    def __init__(self, color):
        self.color = color
        self.direction = "Right"
        self.body = [Block(x,y, color) for (x,y) in START_COORDS]  #head of snake is the first element in the body list

    #Function to draw the snake
    def draw(self, surface: pygame.Surface):
        for block in self.body:
            block.draw(surface) 

#This class extends the tkinter.Frame class and is used
#to create the main window of the application, which is a 
#snake game.
class SnakeGame:
    #Constructor
    def __init__(self):
        #Pygame initialized here!
        pygame.init()
        self.gameSurface = pygame.display.set_mode((ROOTW,ROOTH))
        pygame.display.set_caption('Snake Game')
        self.gameSurface.fill("lightgrey")

        self.snake = Snake("#03ed0a") #initialize the snake
        self.food = Food("red") #initialize the food
        self.score = 0      #initialize player's current score to 0
        self.highscore = self.getHighscore()    #initialize highscore to score saved in file
        self.gameHasStarted = False
        self.keepGameRunning = True
        self.highscoreWasBeaten = False

        #Set font and size
        #self.font = pygame.font.Font(None, FONT_SIZE)
        self.font = pygame.font.SysFont("Helvetica", FONT_SIZE)

        #Create labels for score and highscore
        self.scoreLabel = self.font.render('Score: ' + str(self.score),True,'black')
        self.highscoreLabel = self.font.render('High Score: ' + str(self.highscore),True,'black')

        #Create the canvas for the game
        self.canvas = pygame.Surface((CANVASW, CANVASH))

        self.initScene()
        #End of constructor

    def initScene(self):
        self.gameSurface.blit(self.scoreLabel,(labelInitX+scoreXOffset,labelInitY))
        self.gameSurface.blit(self.highscoreLabel,(labelInitX+highscoreXOffset,labelInitY+25))
        self.food.draw(self.canvas)
        self.snake.draw(self.canvas)
        self.gameSurface.blit(self.canvas,(0,50))
        pygame.display.update()

    def moveSnake(self):
        #Update the body of the snake by starting from tail end
        # and setting each body part's (x,y) coordinates to the
        # coordinates of the body part before it, all the way
        # to the snake's head where it stops.
        for i in range(len(self.snake.body) - 1, 0, -1):
            self.snake.body[i].x = self.snake.body[i-1].x
            self.snake.body[i].y = self.snake.body[i-1].y

        #Now move the head of the snake based on the direction it's going
        if self.snake.direction == "Up":
            self.snake.body[0].y -= 1
        elif self.snake.direction == "Down":
            self.snake.body[0].y += 1
        elif self.snake.direction == "Left":
            self.snake.body[0].x -= 1
        elif self.snake.direction == "Right":
            self.snake.body[0].x += 1

        #Check if the snake has hit itself
        for i in range(1, len(self.snake.body)):
            if self.snake.body[0].x == self.snake.body[i].x and self.snake.body[0].y == self.snake.body[i].y:
                self.keepGameRunning = False

        #Check if the snake has hit the wall
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= CANVASW/BLOCK_SIZE or self.snake.body[0].y < 0 or self.snake.body[0].y >= CANVASH/BLOCK_SIZE:
            self.keepGameRunning = False
            
        #Check if the snake has hit the food
        if self.snake.body[0].x == self.food.x and self.snake.body[0].y == self.food.y:
            #Increment score
            self.score += 1
            self.scoreLabel = self.font.render('Score: ' + str(self.score),True,'black')

            #Give the food new coordinates
            self.food.x = rand.randint(0, CANVASW/BLOCK_SIZE - 1) 
            self.food.y = rand.randint(0, CANVASH/BLOCK_SIZE - 1) 

            #Append new tail block to the snake's body with the coordinates of what's now the old tail
            self.snake.body.append(Block(self.snake.body[len(self.snake.body) - 1].x, self.snake.body[len(self.snake.body) - 1].y, self.snake.color))
            #If current score is higher than the high score update the high score label as well
            # and signal that the high score was beaten.
            if self.score > self.highscore:
                #Update highscore
                self.highscore = self.score
                self.highscoreLabel = self.font.render('High Score: ' + str(self.highscore),True,'black')
                if not self.highscoreWasBeaten:
                    self.highscoreWasBeaten = True

    #This function defines the entry point, or game loop, for the game.
    def gameLoop(self):
        while self.keepGameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.clicked(event)

            if self.gameHasStarted:
                self.moveSnake()
                self.gameSurface.fill("lightgrey")
                self.gameSurface.blit(self.scoreLabel,(labelInitX+scoreXOffset,labelInitY))
                self.gameSurface.blit(self.highscoreLabel,(labelInitX+highscoreXOffset,labelInitY+25))
                self.canvas.fill("black")
                self.food.draw(self.canvas)
                self.snake.draw(self.canvas)
                self.gameSurface.blit(self.canvas,(0,50))
                pygame.display.update()
                time.sleep(0.1)
        
        #Save highscore if beaten
        if self.highscoreWasBeaten:
            self.saveHighscore()
        #Close the window
        pygame.quit()

    def getHighscore(self):
        highscore = 0
        with open("highscore.txt", "r") as file:
            highscore = int(file.readline())
        return highscore

    def saveHighscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

    #Event handler function for keyboard events. Used to handle events
    # when the arrow keys are pressed.
    def clicked(self, event):
        keyPressed = event.key
        if keyPressed == pygame.K_UP and self.snake.direction != "Down":
            self.snake.direction = "Up"
        elif keyPressed == pygame.K_DOWN and self.snake.direction != "Up":
            self.snake.direction = "Down"
        elif keyPressed == pygame.K_LEFT and self.snake.direction != "Right":
            self.snake.direction = "Left"
        elif keyPressed == pygame.K_RIGHT and self.snake.direction != "Left":
            self.snake.direction = "Right"
        elif keyPressed == pygame.K_ESCAPE:
            self.keepGameRunning = False

        #If game hasn't started, then a press of any key will start the game.
        if not self.gameHasStarted:
            self.gameHasStarted = True

#Main function Here!
def main():
    app = SnakeGame()
    app.gameLoop()

if __name__ == "__main__":
    main()