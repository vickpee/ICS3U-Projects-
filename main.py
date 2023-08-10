'''

Final Project 2023
ICS3U-03
Vickie Chen

This program simulates an adventure game in Bikini Bottom. It is based off of the television show "SpongBob SquarePants"

History:
April 13th, 2023: Program Creation
June 5th, 2023: Submission

'''

#used for clearing screen
import os
#used for random number generator
import random
#used for message delay
import time
import sys
#used to import pygame system
import pygame

#shortcuts for keys
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Initialize pygame - this is required.
pygame.init()

#===============CLASSES================
#player class, for burger game
class Player(pygame.sprite.Sprite):
  """
  Represents the player's sprite
  Attributes:
    surf: sprite's surface
    rect: rectangular coordinates of the sprite
  """
  #properties of bun
  def __init__(self):
    super().__init__()
    #loading the bun image
    self.surf = pygame.image.load("bun.png")
    #setting background to clear
    self.surf.set_colorkey((255,255,255), RLEACCEL)
    #getting the rect perimeter surface
    self.rect = self.surf.get_rect()
    #spawing the sprite at a location
    self.rect.midbottom = (390,480)

    #used for the burger parts (see stackables and main functions)
    self.mostrecent = self
    self.layers = 0
    self.lives = 3
    #running = True to make the game stop/run
    self.running = True

  #updating the burger bun's positions when certain keys are pressed
  def update(self, pressed_keys): 
    """
    Move the Player sprites based on user keypresses
    Args:
      self: Player
      pressed_keys: dictionary containing the pressed keys 
    """
    #Move the Player's rectangle based on the keys pressed by the user
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-2,0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(2,0)

    # Keep player on the screen
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
        self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
        self.rect.bottom = SCREEN_HEIGHT

#fisher class, used in jellyfish game
class Fisher(pygame.sprite.Sprite):
  """
  Represents the player's sprite
  Attributes:
    surf: sprite's surface
    rect: rectangular coordinates of the sprite
  """
  def __init__(self):
    super().__init__()
    #loads jellyfish net image
    self.surf = pygame.image.load("net.png")
    #sets sprite's bg colour
    self.surf.set_colorkey((255,255,255), RLEACCEL)
    self.rect = self.surf.get_rect()
    #initial position
    self.rect.midbottom = (120,250)
    self.running = True
    #number of caught jellyfish
    self.caught = 0

  def update(self, pos): 
    """
    Move the Player sprites based on user keypresses
    Args:
      self: Player
      pressed_keys: dictionary containing the pressed keys 
    """
    #Move the Player's rectangle based on the keys pressed by the user
    pos = pygame.mouse.get_pos()
    self.rect.midtop = pos

    # Keep player on the screen
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
        self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
        self.rect.bottom = SCREEN_HEIGHT

#jellyfish class, used to spawn jellyfish
class jfishes(pygame.sprite.Sprite):
  """
  Represents the jellyfish
  Attributes:
    surf: sprite's surface
    rect: rectangular coordinates of the sprite
  """
  def __init__(self):
    super().__init__()
    #loads jellyfish image
    self.surf = pygame.image.load("jellyfish.png")

    #gets rect in random places within the screen (spawn points)
    self.rect = self.surf.get_rect(
      center=(
        random.randint(0, SCREEN_WIDTH),    
        random.randint(20, 20),  
      )
    )
    #random speed from 1-10
    self.speed = random.randint(1,10)
    
  def update(self, fisher):
    #position is shifted in y-direction only, based on the sprite's speed
    self.rect.move_ip(0, self.speed)
    #makes sure jellyfish stays on the screen
    if self.rect.top < 0: 
      self.kill()

#hearts class, used to display number of lives for burger game
class Hearts(pygame.sprite.Sprite):
  def __init__(self):
    #initial number of hearts, occurs when 3 lives
    if player.lives == 3:
      hearts = pygame.image.load("3hearts.png")
    self.surf = hearts
    self.rect = self.surf.get_rect()

  #loads different image every time the lives change
  def update(self,player):
     if player.lives == 2:
      self.surf = pygame.image.load("2hearts.png")
     elif player.lives == 1:
      self.surf = pygame.image.load("1heart.png")

#stackables class, used for burger game ingredients
class Stackables(pygame.sprite.Sprite):
  """
  Represents the stackable foods
  Attributes:
    surf: sprite's surface
    rect: rectangular coordinates of the sprite
  """
  def __init__(self):
    super().__init__()
    #loading all the images/ingredients in the burger game
    stack1 = pygame.image.load("leaf.png")
    stack2 = pygame.image.load("tomato.png")
    stack3 = pygame.image.load("patty.png")
    stack4 = pygame.image.load("topbun.png")
    stack5 = pygame.image.load("bomb.png")
    stack6 = pygame.image.load("cheese.png")
    #putting ingredients into a list to randomly pick from
    ingredients = [stack1, stack2, stack3, stack4, stack5, stack6, stack5, stack5, stack4]
    #picking a number in from 0 - the length of the list
    randingredient = random.randint(0, len(ingredients)-1)
    #using this number as the index number, then choosing an ingredient from the ingredients list to spawn
    self.surf = ingredients[randingredient]

    #setting types, will be used later to end the game
    if self.surf == stack4:
      self.type = "bun"
    elif self.surf == stack5:
      self.type = "bomb"
    else:
      self.type = 'ingredient'

    #setting background to clear for all objects
    self.surf.set_colorkey((255,255,255), RLEACCEL)

    #random spawn points for images
    self.rect = self.surf.get_rect(
      center=(
        random.randint(0, SCREEN_WIDTH),    
        random.randint(-20, -5),  
      )
    )
    #constant speed of 1
    self.speed = 1
    
  def update(self,player):
    """Updates the position of the stackable sprite, stacking it onto the previous item"""
    #position is shifted in y-direction only, based on the sprite's speed
    self.rect.move_ip(0, self.speed)

    #when the bomb touches the burger
    if self.speed == 0:     
      if self.type == "bomb":
        #sets kpatty to False at 9 lives
        if player.layers == 9:
          player.kpatty = False
        #takes off all layers/counter
        player.layers = 0
        #resents counter message 
        print("uh oh! you caught a bomb. now you have to restart from 0!\nIngredient Counter:\n0")
        #subtracts one life
        player.lives -= 1
        #when lives = 0, player dies
        if player.lives == 0:
          #sets kpatty to False
          player.kpatty = False
          #running is False
          player.running = False
          #resets lives for next time the game is played
          player.lives = 3

        #kills all items when a bomb is touched
        for item in stackGrp:
          item.kill()
          player.mostrecent = player     

      #when a top bun touched the burger
      elif self.type == "bun":
        #adds bun to top of burger
        self.rect.x = player.rect.x + 3
        #if the burger is at 8th layers, and the ninth is a burger top, the game ends and the player wins
        if player.layers == 9:
          #kpatty is True, this will be useful for other functions
          player.kpatty = True
          player.running = False
          #resets lives for next time the game is played
          player.lives = 3
          
      else:
        #appends the newest ingredient touched to the top of the burger, in an appropriate position
        self.rect.x = player.rect.x + 3 
        player.kpatty = False
    
    #if off screen, kill/destroy the object
    if self.rect.bottom < 0: 
      self.kill()
  
#===============MAIN=================
#clears screen after messages
def clear():
  """This clears the screen.
  Args:
    None
  Returns:
    None
  """
  os.system('clear')

#function for spongebob's home
def spongebPineapple(foundBurger):
  """
  This represents the Pineapple location.
  Args:
    foundBurger: bool
  Returns:
    choice: str
  """
  #prints welcome message
  print("Welcome to SpongeBob's humble abode! Enjoy your stay in his pineapple! Checking your inventory...")
  #loads bg image
  bg = pygame.image.load("home.jpg") 
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  time.sleep(2)
  #checks for item from burger game (if foundBurger is True)
  if foundBurger == True:
    #prints message and loads hooray picture
    bg = pygame.image.load("hooray (1).png")
    print("\nHooray! You have a burger for Spongebob! You found a special item!")
  else:
    #prints message and loads hungry picture if foundBurger is False
    bg = pygame.image.load("hungry.jpg")
    print("\nHmm...Spongebob seems to be craving something to eat... a Krabby Patty in particular! ")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  
  time.sleep(2)
  #prints choices for next location
  print("""
Where would you like to go next? Your options are: 
  (r) Patrick's Rock
  (f) Jellyfish Fields
  (b) Sandy's Bubble
  (k) KrustyKrab 
  (q) Quit (If you think you have found all the hidden objects, press q!)""")
  #lets user input an option
  choice = input()
  #while loop if the choice is invalid, then asks user to choose again
  while choice not in ['f','r','b','k','K','B','F','R','q','Q']:
    choice = input("That's not an option! Please try again. Enter r, f, b, k or q:")
  #returns choice to main function
  return choice.lower()

#function for krustykrab
def KrustyKrab(kpatty):
  """
  This represents the Krusty Krab location.
  Args:
    foundBurger: bool
  Returns:
    choice: str
  """
  #TODO: Main game loop
  player.running = True
  #loads background and prints ingredients
  bg = pygame.image.load("krustykrab.jpg")
  print("Welcome to the Krusty Krab, Bikini Bottom's beloved fast food restaurant! To obtain one of Spongebob's secret items, you must catch catch 8 ingredients on his burger! Once the ingredient counter gets to 8, catch a burger top bun to complete the level. You get three chances, if you touch a bomb, However, be aware, as catching more than 8 ingredients take all your lives! \n\nIngredient Counter:")
  #kills all items from previous attempt at burger game
  for item in stackGrp:
          item.kill()
          player.mostrecent = player
    
  while player.running == True:
    for event in pygame.event.get(): #every user input --> an event. This gets each of the events in a list.
      if event.type == ADDFOOD:
        # Create the new food and add it to sprite groups
        stackables = Stackables()
        stackGrp.add(stackables)    
        addedGrp.add(stackables)

    #key shortcuts for movement
    pressed_keys = pygame.key.get_pressed()

    #updating the sprites based on the keys pressed
    player.update(pressed_keys)
    #updating the hearts and stackables based on the player
    stackGrp.update(player)
    hearts.update(player)
   
    screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
    screen.blit(player.surf, player.rect) #draw player
    screen.blit(hearts.surf, hearts.rect) #draw hearts

    #drawing the stackables
    for entity in stackGrp:
      screen.blit(entity.surf, entity.rect)

    #drawing the stackables again so they don't disappear from the group entirely
    for entity in addedGrp:
      screen.blit(entity.surf, entity.rect)
  
    clock.tick(100)
    pygame.display.flip()

    #sensing collision with the most recently added ingredient/player and the falling object
    collide = pygame.sprite.spritecollideany(player.mostrecent,addedGrp)
    
    if collide != None:
      #setting object speed to 0
      collide.speed=0
      #adding/removing from groups
      playerGrp.add(collide)
      addedGrp.remove(collide)
      #setting new y-coordinated for the most recent object that fell
      collide.rect.y = player.mostrecent.rect.y - 30
      player.mostrecent = collide
      #adding to layer count
      player.layers += 1
      #printing the layer count
      print(player.layers)

  #seeing if kpatty is True, then displaying different images (based on True/False)
  if player.kpatty == True:
    bg = pygame.image.load("kpattyfound.jpg")
  else:
    bg = pygame.image.load("kpattyNOTfound.jpg")
  screen.blit(bg, (0,0))
  pygame.display.flip()
  player.layers = 0

  time.sleep(2)
  print("""
  Where would you like to go next? Your options are: 
    (p) SpongeBob's Pineapple
    (r) Patrick's Rock
    (q) Quit (If you think you have found all the hidden objects, press q!)
    """)
    #lets user input a choice
  choice = input()
    #while loop if user's selection is invalid
  while choice not in ['p','r','P','R','q','Q']:
    choice = input("That's not an option! Please try again. Enter p, r or q: ")
  #returns choice and kpatty
  kpatty = player.kpatty
  return choice.lower(), kpatty

#function for sandy's home
def sandyBubble(foundJFish, yum):
  """
  This represents the Bubble location.
  Args:
    foundJFish: bool
  Returns:
    choice: str
    foundJFish: bool
  """
  #prints welcome message
  bg = pygame.image.load("sandy.jpg")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  print("Ah, finally some fresh air! Sandy loves to play in her yard and in the grass!")
  time.sleep(2)

  if yum == True:
    print("Yay! You have a Jellyfish for Sandy! As a token of appreciation, she gives you one of SpongeBob's hidden items!")
    foundJFish = True
  #informs user/gives a hint that Sandy wants something if user does not have a jellyfish (from jellyfishFields in inv[1])
  else:
    print("Sandy seems to be looking for something... Come back later!")
    
  
  time.sleep(2)
  #prints choices for next location
  print("""
    Where would you like to go next? Your options are: 
    (p) SpongeBob's Pineapple
    (r) Patrick's Rock 
    (q) Quit (If you think you have found all the hidden objects, press q!)
    """)
  #lets user input a choice
  choice = input()
  #while loop if user's choice is invalid
  while choice not in ['p','r','P','R','q','Q']:
    choice = input("That's not an option! Please try again. Enter p or r: ")
    #returns choice and foundJFish
  return choice.lower(), foundJFish

#function for patrick's home
def patRock(patThink):
  """
  This represent the Rock location.
  Args:
    patThink: bool
  Returns:
    choice: str
    patThink: bool
  """
  bg = pygame.image.load("patrock.jpg")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  #prints welcome message
  print("Welcome to Patrick's Rock! Patrick loves to stay at home... staring enlessly into space... Oh there he is now!!\n")
  time.sleep(3)
  bg = pygame.image.load("guesser.jpg")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  print("Patrick wants to play a game with you! Try and guess what's on his mind right now!")
  waiting = True
  #https://www.youtube.com/watch?v=32l6YqAPyYo
  while waiting:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        left, right, middle = pygame.mouse.get_pressed()
        #getting coordinate positions of mouse when clicked
        coords = []
        coords.append(pygame.mouse.get_pos()[0])
        coords.append(pygame.mouse.get_pos()[1])

        #checking if mouse's coordinates are within the photo's range
        for i in range(1,len(coords),2):
          if coords[i]>60 and coords[i]<255:

            #incorrect image is clicked, waiting is false
            if coords[i-1]>45 and coords[i-1]<240:
              bg = pygame.image.load("bodybuilding.jpg")
              print("\nThat is incorrect! Try again later!")
              waiting = False
    
            if coords[i-1]>300 and coords[i-1]<500:
              bg = pygame.image.load("pathungry.jpg")
              print("\nThat is incorrect! Try again later!")
              waiting = False

            #correct image is clicked, correct image is posted, then waiting is set to False and the item is found (patThink)
            if coords[i-1]>560 and coords[i-1]<755:
              bg = pygame.image.load("patcorrect.jpg")
              print("\nYou got it!! As a reward, Patrick has given you one of SpongeBob's hidden items!")
              waiting = False
              patThink = True
            
        screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
        pygame.display.flip()

  #prints options for next location
  print("""
Where would you like to go next? Your options are: 
  (p) SpongeBob's Pineapple
  (f) Jellyfish Fields
  (b) Sandy's Bubble
  (q) Quit (If you think you have found all the hidden objects, press q!)""")

  #lets user select a choice
  choice = input()
  #while loop if user's choice is invalid
  while choice not in ['f','p','b', 'B','F','P','q','Q']:
    choice = input("That's not an option! Please try again. Enter r, f, b, k or q:")
  #returns choice and patThink
  return choice.lower(), patThink

#function for jellyfish fields
def jellyfishFields(jFish):
  """
  This represent the Rock location.
  Args:
    jFish: bool
  Returns:
    choice: str
    jFish: bool
  """
  #prints welcome message
  print("Welcome to Bikini Bottom's largest Jellyfishing Field! Be careful! Sometimes, the jellyfish like to sting...\n")
  bg = pygame.image.load("jfishfields.jpg")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  #waits two seconds before next message
  time.sleep(2)
  #random choice (1/2) if jFish = False
  if random.choice([0,1]) == 0 and jFish == False:
    #prints found jellyfish message
    bg = pygame.image.load("field.jpg")
    print("The jellyfish are awake! Use the net to capture jellyfish by clicking on them! Once you get to 12, you will be awarded a special prize!")
    #number of jellyfish caught
    caughtfish = 0
    
    while fisher.running == True:
        for event in pygame.event.get(): #every user input --> an event. This gets each of the events in a list.
          if event.type == ADDJELLYFISH:
            #adding the jellyfish to a group
            jelly = jfishes()
            fishGrp.add(jelly)

          #getting the position of the mouse for the net
          mouse = pygame.mouse.get_pos()
          #updating net position(fisher) based on mouse pos
          fisher.update(mouse)
          #updating jellyfish based on fisher
          fishGrp.update(fisher)
       
          screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
          screen.blit(fisher.surf, fisher.rect) #draw player

          #drawing the jellyfish in fishGrp
          for entity in fishGrp:
            screen.blit(entity.surf, entity.rect)
          
          clock.tick(100)
          pygame.display.flip()

          #collision detection
          collide = pygame.sprite.spritecollideany(fisher,fishGrp)
          if collide != None:
            #killing the caught jellyfish
            collide.kill()
            caughtfish += 1
            #printing number of jellyfish caught
            print(caughtfish)
            
          #when number of jellyfish needed is reached
          if caughtfish == 12:
              jFish = True
              #drawing background once the number of jellyfish caught has been achieved
              bg = pygame.image.load("wonjelly.jpg")
              screen.blit(bg, (0,0))
              pygame.display.flip()
              #stops game
              fisher.running = False
    #prints congrats message
    print("Congratulations! You caught all the jellyfish!")
  else:
    print("Hmmm.. seems like the jellyfish aren't here right now. Come back later!")
  
  time.sleep(2)
  #prints next locations
  print("""
  Where would you like to go next? Your options are: 
  (p) SpongeBob's Pineapple
  (r) Patrick's Rock 
  (q) Quit (If you think you have found all the hidden objects, press q!)
    """)
  #lets user input a choice
  choice = input()
  #while loop if user's choice is invalid
  while choice not in ['p','r','P','R', 'q', 'Q']:
    choice = input("That's not an option! Please try again. Enter p or r: ")
  #returns choice and jFish
  return choice.lower(), jFish

#==== MAIN ====

#sets screen height and width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#sets all objects in inv to False to start
inv = [False, False, False, False]
 
bg = pygame.image.load("background.jpg")
screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
pygame.display.flip()

#pygame events
ADDFOOD = pygame.USEREVENT + 1
ADDJELLYFISH = pygame.USEREVENT + 2

#intervals for events to occur
pygame.time.set_timer(ADDFOOD, 2500)
pygame.time.set_timer(ADDJELLYFISH, 900)

#setting classes and names
player = Player()
hearts = Hearts()
fisher = Fisher()

#setting names and creating groups for items
playerGrp = pygame.sprite.Group()
#adding the player to the player group
playerGrp.add(player)
stackGrp = pygame.sprite.Group()
addedGrp = pygame.sprite.Group()
fishGrp = pygame.sprite.Group()
clock = pygame.time.Clock()

#prints start message
print("""
Spongebob has been robbed of Mr. Krabs' precious secret formula!! To find it, you must retrieve 4 hidden objects in the city! Good luck, Spongebob is counting on you!""")
#prints starting location options
print("""
  Where would you like to start? Your options are: 
    (p) SpongeBob's Pineapple
    (r) Patrick's Rock
    (f) Jellyfish Fields
    (b) Sandy's Bubble
    (k) KrustyKrab 
    (q) Quit (If you think you have found all the hidden objects, press q!) """)

#lets user input a choice
choice = input("\nEnter p, r, f, b, k or q: ")
#while loop if user's choice is invalid
while choice not in ['f','r','b','k','K','B','F','R','q','Q','p','P']:
  choice = input("Invalid! Enter p, r, f, b, k or q: ")

#clears screen
clear()

while choice != 'q':
  if choice == 'p':
    #no parameters for SpongeBob's Pineapple, returns user's choice for next location
    choice = spongebPineapple(inv[0])
  elif choice == 'f':
    #returns user's choice and jFish is True if the jellyfish was found (sets inv[1] to True)
    choice, inv[1] = jellyfishFields(inv[1])
  elif choice == 'b':
    #returns user's choice and foundJFish is True if user already had a jellyfish (sets inv[2] to True)
    choice, inv[2] = sandyBubble(inv[2], inv[1])
  elif choice == 'k':
    #returns user's choice and kpatty is True if user selects the Krabby Patty option from menu (sets inv[0] to True)
    choice, inv[0] = KrustyKrab(inv[0])
  elif choice == 'r':
    #returns user's choice and patThink is True if user selects the correct answer to Patrick's question (sets inv[3] to True)
    choice, inv[3] = patRock(inv[3])
  #clears screen after each function is executed
  clear()

if choice == 'q':
  if inv == [True, True, True, True]:
    #sets bg to winner image if game is complete, and prints winning message
    bg = pygame.image.load("winner.jpg")
    print("Congrats! You have complete Spongebob Squarepants' Super Spectacular Quirky Quest Game!")
  else:
    #sets bg to lose image if game is incomplete, and prints losing message
    bg = pygame.image.load("lose.jpg")
    print("YOU LOST!!! That's too bad! Try again some other time!")
  screen.blit(bg, (0,0)) #bg image displayed with top left corner at 0,0
  pygame.display.flip()
  #keeps image for ten seconds
  time.sleep(10)
  
#game ends
pygame.quit()