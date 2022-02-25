import pygame
import random
pygame.init()
WIN = pygame.display.set_mode((800,600))
pygame.display.set_caption('Three Kingdoms')
all_players = []
WHITE = (255,255,255)
BLACK = (0,0,0)
global run, pass_button
run = True
GREY = (200,200,200)
passbuttonx = 100
passbuttony = 100
passbuttonwidth = 200
passbuttonheight = 50
all_buttons = []
turn_index = None
health_limit = 4

class Button:
    
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        if name != "pass" or name != "passturn": # If it isn't the pass button
            all_buttons.append(self)
        
    def isHovering (self):
        if pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[0] < self.x + self.width and pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1] < self.y + self.height:
            return True
        else:
            return False
    def draw_self (self):
            if self.isHovering():
                pygame.draw.rect(WIN, GREY, pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(self.x, self.y, self.width, self.height), 2)
            font = pygame.font.Font('freesansbold.ttf', 22)
            text = font.render(self.name, True, BLACK)
            textRect = text.get_rect()
            textRect.center = (self.x + self.width / 2, self.y + self.height / 2)
            WIN.blit(text, textRect)
            
class Cards(Button):
    def __init__(self, x, y, width, height, owner, name):
       super().__init__(x, y, width, height, name)
       self.owner = owner

class Attack(Cards):
    def __init__(self, x, y, width, height, owner):
       super().__init__(x, y, width, height, owner, "Attack")
       
    def play (self, target):
       if not self.owner.isAttacked[0]:
               target.isAttacked = (True, "You Have Been Attacked! Play dodge?", 1)
               self.owner.cards.remove(self)
               self.owner.sort_cards()
       
class Dodge(Cards):
    def __init__(self, x, y, width, height, owner):
       super().__init__(x, y, width, height, owner, "Dodge")

    def play(self, target):
        if self.owner.isAttacked[0]:
            self.owner.isAttacked = (False, None, 0)
            self.owner.cards.remove(self)
            self.owner.sort_cards()
class DrawTwo(Cards):
    def __init__(self, x, y, width, height, owner):
       super().__init__(x, y, width, height, owner, "Draw 2")
    def play(self, target):
        if not self.owner.isAttacked[0]:
            self.owner.collect_card()
            self.owner.collect_card()
            self.owner.cards.remove(self)
            self.owner.sort_cards()

class Peach(Cards):
    def __init__(self, x, y, width, height, owner):
       super().__init__(x, y, width, height, owner, "Peach")
    def play(self, target):
        if not self.owner.isAttacked[0] and self.owner.health < health_limit:
            self.owner.health += 1
            self.owner.cards.remove(self)
            self.owner.sort_cards()

class Player:
    def __init__(self, health, playername):
       self.cards = []
       self.health = health
       all_players.append(self)
       self.isAttacked = (False, None, 0)
       self.isAttacking = (False, None, 0)
       self.name = playername
       self.button = Button(100, 100, 200, 50, self.name)
       # Display Health
    def display_health(self):
        font = pygame.font.Font('freesansbold.ttf', 22)
        text = font.render("Health: " + str(self.health), True, BLACK)
        textRect = text.get_rect()
        textRect.center = (70, 380)
        WIN.blit(text, textRect)
        # Receive X pos for each new card
    def get_x(self):
        return (len(self.cards) + 1) * 100
        # When adding cards to a player's hand
    def collect_card(self):
        # Add a random dodge or attack
        x=["Attack", "Dodge", "DrawTwo", "Peach"]
        if random.choice(x) == "Attack":
            self.cards.append(Attack(self.get_x(), 400, 100, 200, self))
        elif random.choice(x) == "Dodge":
            self.cards.append(Dodge(self.get_x(), 400, 100, 200, self))
        elif random.choice(x) == "DrawTwo":
            self.cards.append(DrawTwo(self.get_x(), 400, 100, 200, self))
        else:
            self.cards.append(Peach(self.get_x(), 400, 100, 200, self))
    
    def attacking_screen(self, statement):
            statement_font = pygame.font.Font('freesansbold.ttf', 22)
            statement_text = statement_font.render("You're attacking, click player to target", True, BLACK) # Statement of the attack
            statement_textRect = statement_text.get_rect()
            statement_textRect.center = ()
            WIN.blit(statement_text, statement_textRect)
    
    # When player is attacked
    def attacked_screen(self, statement):
            pass_button.draw_self()
            statement_font = pygame.font.Font('freesansbold.ttf', 22)
            statement_text = statement_font.render(statement, True, BLACK) # Statement of the attack
            statement_textRect = statement_text.get_rect()
            statement_textRect.center = (pass_button.x + pass_button.width / 2, pass_button.y - 50 + pass_button.height / 2)
            WIN.blit(statement_text, statement_textRect)
    def sort_cards(self):
        x = 100
        for card in self.cards:
            card.x = x
            x += 100
def sort_players():
    x = 100
    for player in all_players:
        player.button.x = x
        x += 200
test_player = Player(4, "testplayer1")
test_player.collect_card()
test_player.collect_card()
test_player.collect_card()
test_player.collect_card()

new_player = Player(4, "testplayer2")
new_player.collect_card()
new_player.collect_card()
new_player.collect_card()
new_player.collect_card()

pass_button = Button(100, 300, 200, 50, "pass")
pass_turn = Button(500, 300, 200, 50, "passturn")
first_player = random.choice(all_players)  
turn_index = all_players.index(first_player)
start_turn = True
end_turn = False
while run:
    WIN.fill(WHITE)
    player = all_players[turn_index] 
    if start_turn:
        player.collect_card()
        player.collect_card()
        start_turn = False
    if end_turn:
        font = pygame.font.Font('freesansbold.ttf', 22)
        text = font.render("End Turn! Discard Cards to Your Health Level!", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (300, 250)
        WIN.blit(text, textRect)
        if len(player.cards) <= player.health:
            if all_players[turn_index] == all_players[-1]:
                player.sort_cards()
                turn_index = 0
                start_turn = True
                end_turn = False
            else:
                player.sort_cards()
                turn_index += 1
                start_turn = True
                end_turn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if player.isAttacked[0] == True: # Test pass button
                if pass_button.isHovering():
                    player.health -= player.isAttacked[2] # Minus damage
                    player.isAttacked = (False, None, 0)
            else:
                if pass_turn.isHovering():
                    end_turn = True
            for card in player.cards:
                if card.isHovering() and end_turn == False:
                    card.play(player)
                    player.sort_cards()
                elif card.isHovering() and end_turn == True:
                    player.cards.remove(card)
                    player.sort_cards()

    player.display_health()
    if player.isAttacked[0] == True:
        player.attacked_screen(player.isAttacked[1]) # Display attacked screen
    elif player.isAttacking[0] == True:
        player.attacked_screen(player.isAttacking[1]) # Display attacking screen
    else:
        pass_turn.draw_self()      
    for card in player.cards:
        card.draw_self()
    for player in all_players:
        sort_players()
        player.button.draw_self()
    pygame.display.update()
    
pygame.quit()
