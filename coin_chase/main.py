########################################
# Coin chase v1.0                      #
########################################
# Welcome to coin chase! A tiny pygame.#
# In Coin chase you have to chase after#
# coins while avoiding Piru the ghost, #
# who is chasing after you instead.    #
# Piru also likes to steal your coins  #
# if you are too hard to catch! Collect#
# 25 points to turn the lights back on #
# and get rid of Piru.                 #
########################################
# Laurens Veltman 12-2021

#Import and initialize pygame
import pygame
import random
import math

pygame.init()
pygame.display.set_caption('Coin-chase v1.0')

#Functions related to the functioning of the main function. 
class Game:
    def set_window(heigth: int, width: int):
        window = pygame.display.set_mode((width, heigth))
        return window

    def draw(object: object):
        window.blit(object.image, (object.x, object.y))

    #Renders part of the game-over screen.
    def game_over(winner):
        winner.update_coin_loc()
        Game.draw(winner) 
        text = game_font.render(f"Game over", True, (255, 0, 0))
        window.blit(text, ((640//2 - 60, 480//2 -50)))
        text = game_font.render(f"Press any key to exit", True, (255, 0, 0))
        window.blit(text, ((640//2 - 100, 480//2 + 30)))
        pygame.display.flip()
        clock.tick(60)


#Initialize a coin.
class Coin:
    def __init__(self, velocity = 1, image = pygame.image.load("coin.png")):
        self.image = image
        self.width = self.image.get_width()
        self.heigth = self.image.get_height()
        self.x = random.randint(0,640-self.width)
        self.y = random.randint(0,480-self.heigth)
        self.x_vel = random.choice([-1,1])
        self.y_vel = random.choice([-1,1])
        self.velocity = velocity

    #Checks if object x,y coordinate overlap with an entity's hitbox and assigns one point to that entity.
    #Sets random new coordinates and x,y velocity if caught.
    def check_if_caught(self, players):
        for entity in players:
            if self.x in entity.hitbox[0] and self.y in entity.hitbox[1]:
                entity.points += 1
                self.x, self.y = random.randint(0,640-self.width), random.randint(0,480-self.heigth)
                self.x_vel, self.y_vel = random.choice([-self.velocity,self.velocity]), random.choice([-self.velocity,self.velocity])

    #Coordinates are updated based on own velocity. Velocity changes if a corner is reached.
    def update_coin_loc(self):
        if self.x+self.width >= 640 and self.x_vel > 0:
            self.x_vel = -self.velocity
        if self.y+self.heigth >= 480 and self.y_vel > 0:
            self.y_vel = -self.velocity
        if self.x <= 0 and self.x_vel < 0:
            self.x_vel = self.velocity
        if self.y <= 0 and self.y_vel < 0:
            self.y_vel = self.velocity 
        self.y += self.y_vel
        self.x += self.x_vel


#Initialize a player or monster.
class Player:
    def __init__(self, image, velocity = 1, is_monster = 0, x = 0, y = 0):
        self.image = image
        self.width = self.image.get_width()
        self.heigth = self.image.get_height()
        self.x = x
        self.y = y
        self.hitbox = list()
        self.points = 0
        self.velocity = velocity
        self.is_monster = is_monster
    
    #Coordinates are updated based on the user input, the player can't leave the screen.
    def update_player_loc(self, target_x: int, target_y: int):
        if self.x > target_x:
            if self.x >= 0:
                self.x -= self.velocity
        if self.x < target_x:
            if self.x <= 640-self.width:
                self.x += self.velocity
        if self.y > target_y:
            if self.y >= 0:
                self.y -= self.velocity
        if self.y < target_y:
            if self.y <= 480-self.heigth:
                self.y += self.velocity

    #Coordinates are updated based on what it is currently chasing.
    def update_monster_loc(self,chase):
        if self.x > chase.x:
            self.x -= self.velocity
        if self.x < chase.x:
            self.x += self.velocity
        if self.y > chase.y:
            self.y -= self.velocity
        if self.y < chase.y:
            self.y += self.velocity

    #Determine most favorable target. Coin is prefered if player is far.
    def chase_target(self, coin: Coin, player: object):
        player_distance = math.sqrt(abs((player.x - self.x)*2 + (player.y - self.y)*2))
        coin_distance = math.sqrt(abs((coin.x - self.x)*2 + (coin.y - self.y)*2))
        if player_distance <= coin_distance * 2:
            return player
        else:
            return coin

    #The 'hitbox' is updated by initializing a x & y coordinate range based on the width and heigth of the entity. 
    def update_hitbox(self):
        self.hitbox = list()
        player_xbox = []
        player_ybox = []
        for i in range(self.x-(self.width//2), self.x+((self.width+1)//2)):
            player_xbox.append(i)
        for j in range(self.y-(self.heigth//2), self.y+((self.heigth+1)//2)):
            player_ybox.append(j)
        self.hitbox = [player_xbox, player_ybox] 

    #the entity gains 3 points if it catches the x,y coordinate of the target in it's hitbox.
    def check_if_caught(self, players):
        for entity in players:
            if entity.is_monster == 1 and self.x in entity.hitbox[0] and self.y in entity.hitbox[1]:
                entity.points += 3
                entity.x, entity.y = 0,0
                self.x, self.y = 640-self.width//2, 480-self.heigth//2
                window.fill((100, 0, 0))


#Global variables
robot_img = pygame.image.load("robot.png")
monster_img = pygame.image.load("monster.png")
clock = pygame.time.Clock()
points = -1
heigth = 480
width = 640
target_x = 0
target_y = 0
window = Game.set_window(heigth,width)
game_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40)
#Entities
coin = Coin()
player = Player(robot_img, velocity = 2, x=width//2-robot_img.get_width() , y=heigth//2)
player.update_hitbox()
players = [player]
monsters = list()

#Title screen
while points == -1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_x = event.pos[0]-player.width/2
            target_y = event.pos[1]-player.heigth/2
        if event.type == pygame.QUIT:
            exit()
    window.fill((255, 255, 255))
    Game.draw(player)
    text = title_font.render(f"Welcome to Coin-Chase", True, (255, 0, 0))
    window.blit(text, ((640//2 - 200, 480//2 -200)))
    text = game_font.render(f"Press the robot to start", True, (255, 0, 0))
    window.blit(text, ((640//2 - 120, 480//2 -50)))
    text = game_font.render(f"Collect the coins & avoid Piru", True, (255, 0, 0))
    window.blit(text, ((640//2  - 140, 480//2 +100)))
    text = game_font.render(f"Good luck!", True, (255, 0, 0))
    window.blit(text, ((640//2 - 70, 480//2 +130)))
    pygame.display.flip()
    if target_x in player.hitbox[0] and target_y in player.hitbox[1]:
        points += 1

#Main game
while True:
    #Check user input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            target_x = event.pos[0]-player.width/2
            target_y = event.pos[1]-player.heigth/2
        if event.type == pygame.QUIT:
            exit()

    #Update fill brightness
    window.fill((10*points,10*points,10*points))
    
    #Update player data        
    points = player.points
    player.update_player_loc(target_x,target_y)
    player.update_hitbox()
    player.check_if_caught(monsters)
    Game.draw(player)

    #Spawns the monster upon score == 3
    if points == 3 and len(monsters) == 0:
        monsters.append(Player(monster_img, is_monster = 1, x = 640//2, y = 480//2))

    #Update monster data
    for monster in monsters:
        points -= monster.points
        chase = monster.chase_target(coin,player)
        monster.update_monster_loc(chase)
        monster.update_hitbox()
        coin.check_if_caught(monsters)
        Game.draw(monster)

    #Check for game over     
    if points < 0 or points >= 25:
        if points < 0:
                filling = (0, 0, 0)
                winner = Coin(image = monster_img)
        elif points >= 25:
                filling = (250, 250, 250)
                winner = Coin(image = robot_img)
        while True:
            #Game over animation
            window.fill((filling))
            Game.game_over(winner)
            #Exit upon keypress
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print('Game over')
                    exit()
                if event.type == pygame.QUIT:
                    exit() 

    #Update coin 
    coin.check_if_caught(players)
    coin.check_if_caught(monsters)
    coin.update_coin_loc()
    Game.draw(coin)

    text = game_font.render(f"Points: {points}", True, (255, 0, 0))
    window.blit(text, (550, 0))
    pygame.display.flip()
    clock.tick(60)