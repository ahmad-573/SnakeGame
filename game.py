import pygame
import random
import time
from pygame.locals import *

import PIL
from PIL import Image

im = Image.open("resources/square.png")

SIZE = im.size[0]
print(SIZE)
Grid_X = 500
Grid_Y = 500
BG_color = (250,250,250)
text = (106,13,173)

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.png").convert_alpha()
        self.i = random.randint(0,(Grid_X-1)//SIZE) * SIZE
        self.j = random.randint(0,(Grid_Y-1)//SIZE) * SIZE
        generated = False
            
    
    def draw(self):
        self.parent_screen.fill(BG_color)
        self.parent_screen.blit(self.apple,(self.i,self.j))
        pygame.display.flip()

    def move(self):
        self.i = random.randint(0,(Grid_X-1)//SIZE) * SIZE
        self.j = random.randint(0,(Grid_Y-1)//SIZE) * SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/square.png").convert_alpha()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'
        self.steps = 0

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(0,self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1] % Grid_X
            self.y[i] = self.y[i-1] % Grid_Y

        if self.direction == 'up':
            self.y[0] -= SIZE
        
        if self.direction == 'down':
            self.y[0] += SIZE

        
        if self.direction == 'left':
            self.x[0] -= SIZE
        
        if self.direction == 'right':
            self.x[0] += SIZE
        
        self.x[0] = self.x[0] % Grid_X
        self.y[0] = self.y[0] % Grid_Y
        
        self.draw()
        time.sleep(0.1)

    def colliding(self):
        head_x = self.x[0]
        head_y = self.y[0]
        for i in range(1,self.length):
            if self.x[i] == head_x and self.y[i] == head_y:
                return True
        return False
        
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((Grid_X, Grid_Y))
        self.surface.fill(BG_color)
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        generated = False
        while not generated:
            i = 0
            self.apple.move()
            for i in range(0,self.snake.length):
                if self.apple.i == self.snake.x[i] and self.apple.j == self.snake.y[i]:
                    break
                i+=1
            if i == self.snake.length:
                generated = True
        self.apple.draw()

    def play(self):
        #self.background()
        self.apple.draw()
        self.display_score()
        self.snake.walk()
        pygame.display.flip()

        if self.eating():
            self.snake.increase_length()
            generated = False
            while not generated:
                i = 0
                self.apple.move()
                for i in range(0,self.snake.length):
                    if self.apple.i == self.snake.x[i] and self.apple.j == self.snake.y[i]:
                        break
                    i+=1
                if i == self.snake.length:
                    generated = True
    def eating(self):
        if abs(self.snake.x[0] - self.apple.i) < SIZE and abs(self.snake.y[0] - self.apple.j) < SIZE:
            return True
        
        return False
    
    def colliding(self):
        head_x = self.snake.x[0]
        head_y = self.snake.y[0]
        for i in range(1,self.snake.length):
            if self.snake.x[i] == head_x and self.snake.y[i] == head_y:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.snake.length}",True,text)
        self.surface.blit(score, (370,10))
        pygame.display.flip()

    def show_game_over(self):
        #self.background()
        self.surface.fill(BG_color)
        font = pygame.font.SysFont('arial', 15)
        line1 = font.render(f"Game Over!! Your Score is: {self.snake.length}", True, text)
        self.surface.blit(line1,(60,200))
        line2 = font.render(f"Press 'Enter' to play again. Press 'Escape' to exit.", True, text)
        self.surface.blit(line2,(40,300))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def background(self):
        im = pygame.image.load("resources/back.png")
        self.surface.blit(im,(0,0))
    
    def run(self):
        running  = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            
            if not pause:
                self.play()
                if self.colliding():
                    self.show_game_over()
                    pause = True
            if pause:
                self.reset()
            time.sleep(0.01)
    

if __name__ == "__main__":
    game = Game()
    game.run()

