import pygame

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))#vytvoření okna
pygame.display.set_caption("Block-breaker")#titulky okna

FPS = 150

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BALL_RADIUS = 7



menug = pygame.image.load("menu.jpg") # načítání obrázku menu
menurectg = pygame.Rect(0,0,500,600) # vytvoření obdélníku pro menu


menu_options = pygame.image.load("menu_options3.jpg") # načítání obrázku menu options
menu_options_rect = menurectg = pygame.Rect(0,0,500,600) # vytvoření obdélníku pro menu options




# pálka
class Paddle:  
    VEL = 6   # rychlost pálky

    def __init__(self, x, y, width, height):
        # inicializace základních proměnných pro pálku
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        

    def movement(self,keys):  # pohyb
        self.keys=keys
        if keys[pygame.K_a] and self.x >=0:
            self.x -= self.VEL
        if keys[pygame.K_d] and self.x <= WIDTH - self.width:
            self.x += self.VEL
        self.paddlerect = pygame.Rect(self.x, self.y, self.width, self.height) # vytvoření obdéln íku pro pálku

    def draw(self,win):
        pygame.draw.rect(win, WHITE, self.paddlerect) # kreslení pálky
        



class Ball: #vše spojené s míčkem + řeší se zde i všechny kolize
    def __init__(self, x, y, radius):
        # inicializace proměnných pro míček
        self.x = x
        self.y = y
        self.radius = radius
        self.vel_x = 0
        self.vel_y = 2
        self.vel_xx = 2
        self.score = 0
        self.ball_rect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2) # obdílník pro míček
        self.kolize = False
        




    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius) # kreslení na plochu WIN

    def movement(self): # řešení pohybu míčku včetně kolizí

        # Výpočet relativní pozice dopadu na pádlo -1 až 1
        difference = (self.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2)
        #print(difference//6)
        self.x += self.vel_x  # pohyb do boků
        self.y += self.vel_y  # pohyb nahoru a dolu

        # kolize se stěnami --------------------
        if self.x >= WIDTH - self.radius:
            self.x = WIDTH - self.radius # Oprava pozice při proklouznutí
            self.vel_x *= -1
        if self.x <= 0 + self.radius:
            self.x = 0 + self.radius  # Oprava pozice při proklouznutí
            self.vel_x *= -1

        if self.y <= 0:
            self.vel_y *= -1
        #-----------------------


        #kolize s pádlem -----------------------------
                
        if self.ball_rect.colliderect(paddle.paddlerect):
            
            from_top_paddle = self.ball_rect.bottom - paddle.paddlerect.top
            from_left_paddle = self.ball_rect.right - paddle.paddlerect.left
            from_right_paddle = paddle.paddlerect.right - self.ball_rect.left
            if from_top_paddle <= from_left_paddle and from_top_paddle <= from_right_paddle and self.vel_y > 0.5 and self.kolize == False: 
                self.vel_y *= -1
                self.vel_x = difference * 5
            elif from_left_paddle <= from_top_paddle and from_left_paddle <= from_right_paddle and self.vel_x >= 0 and self.kolize == False:
                if self.vel_x == 0:
                    self.vel_x = 3
                else:
                    self.x = paddle.x # když pádlo svým pohybem překryje míček, míček bude na straně mádla

                self.vel_x*=-1
                self.vel_y *= -1

            elif from_right_paddle <= from_top_paddle and from_right_paddle <= from_left_paddle and self.vel_x <= 0 and self.kolize == False:
                if self.vel_x == 0:
                    self.vel_x = -3
                else:
                    self.x = paddle.x + paddle.width # když pádlo svým pohybem překryje míček, míček bude na straně mádla

                self.vel_x*=-1
                self.vel_y *= -1

            #print(from_top_paddle, from_left_paddle, from_right_paddle)
            self.kolize = True

        if self.ball_rect.colliderect(paddle.paddlerect) == False:
            self.kolize = False

        #-----------------------------


        
        #reset hrací plochy -------------------

        if self.y  > HEIGHT:
            self.x = WIDTH//2
            self.y = HEIGHT//2
            self.vel_x = 0
            self.vel_y = 2
            self.vel_xx = 2
            self.score = 0
            paddle.x = WIDTH//2 - paddle.width //2  
            menuf()  # po prohře mě to hodí zpět do menu
            
            # vytváření nového dvojrozměrného pole pro bloky
            rectangle.block = []
            rectangle.block1 = []
            for row in range(rectangle.rows):

                block_row = []
                block_row1 = []


                for col in range(rectangle.cols):
                    
                    brick_x = col * rectangle.width + 2
                    brick_y = row * rectangle.height + 50

                    rect = pygame.Rect(brick_x, brick_y, rectangle.width, rectangle.height)
                    rect1 = [brick_x, brick_y, rectangle.width, rectangle.height]

                    block_row.append(rect)
                    block_row1.append(rect1)
                


                rectangle.block.append(block_row)
                rectangle.block1.append(block_row1)
                #-----------------------------
            
            
        
        
        self.ball_rect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2) # vytvoření obdélníku míčku pro každý jeden frame(snímek)
        
        collision_detected = False
        row_count = 0


        # procházení pole s cihlami/bloky
        for row,row1 in zip(rectangle.block,rectangle.block1):
            item_count = 0

            for item,item1 in zip(row,row1): 
                

                # Přeskočí prázdné cihly
                if item1[0] == -1:
                    item_count += 1
                    continue

                



                if self.ball_rect.colliderect(item):  # kontrola kolize míčku s blokem

                    
                    # střed míčku
                    ball_center_x = self.ball_rect.centerx
                    ball_center_y = self.ball_rect.centery

                    if ball_center_y < item.top + self.radius and self.vel_y > 0:  # Odražený míček se dostane nad blok
                        self.vel_y *= -1  # Odraz nahoru

                    elif ball_center_y > item.bottom - self.radius and self.vel_y < 0:  # Odražený míček se dostane pod blok
                        self.vel_y *= -1  # Odraz dolů

                    elif ball_center_x < item.left + self.radius and self.vel_x > 0:  # Odražený míček se dostane vlevo od bloku
                        self.vel_x *= -1  # Odraz vlevo
                    elif ball_center_x > item.right - self.radius and self.vel_x < 0:  # Odražený míček se dostane vpravo od bloku
                        self.vel_x *= -1  # Odraz vpravo
                    


                    
                    rectangle.block[row_count][item_count] = (-1, -1, -1, -1)  # přesun bloku při kolizi mimo viditelnou plochu
                    self.score += 1  # počítání skóre
                    collision_detected = True # detekovaná kolize
                    break


                item_count += 1
            if collision_detected: 
                break
            row_count += 1
            # ------------------------   


class Rectangle: # vytváření a kreslení cihliček/bloků
    def __init__(self):
        # inicializace proměnných pro bloky
        self.rows = 3
        self.cols = 7
        self.width = WIDTH // self.cols
        self.height = 30
        self.block = []
        self.block1 = []
       


    def create_bricks(self):
        # cykly pro vytvoření dvojrozměrého pole bloků
        for row in range(self.rows):

            block_row = []
            block_row1 = []


            for col in range(self.cols):
                
                brick_x = col * self.width + 2
                brick_y = row * self.height + 50

                rect = pygame.Rect(brick_x, brick_y, self.width, self.height)
                rect1 = [brick_x, brick_y, self.width, self.height]

                block_row.append(rect)
                block_row1.append(rect1)
                


            self.block.append(block_row)
            self.block1.append(block_row1)
        # -------------


        #print(self.block1)
        
        

    def draw_bricks(self,win):
        # kreslení bloků
        for row in self.block:
            for block in row:
                pygame.draw.rect(win,WHITE,block)
                pygame.draw.rect(win,BLACK,block,1)#okraj bloků




paddle = Paddle(WIDTH//2-40,HEIGHT-10-20,80,20) 
ball = Ball(WIDTH//2, HEIGHT//2, 5)
rectangle = Rectangle()
rectangle.create_bricks()


beh = True
options = False

def options_menu(Options): # funkce pro menu_optiions == options po zmáčknutí tlačítka
    options = Options
    while options:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options = False
                menuf()
                break


        WIN.fill(BLACK) # vyplnění plochy černou barvou
                

        WIN.blit( menu_options ,menu_options_rect)  # kreslení na plochu 
        pygame.display.update()


def menuf():  # funkce pro vytvoření menu

    global beh, options, menu

    menu = True
    while menu:
        x = 0
        y = 0
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                beh = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Kliknutí myší
                x, y = event.pos  # Získání souřadnic kliknutí
                #print(f"Kliknuto na pozici: ({x}, {y})")   

        mouserect = pygame.Rect(x,y,1,1) # obdélník pro myš na zjištění kolize s obdelníkem tlačítek
        tlacitko1 = pygame.Rect(148,366,203,70) # tlačítko options obdélník
        tlacitko2 = pygame.Rect(148,475,203,80) # tlačítko start obdélník
        


        if mouserect.colliderect(tlacitko2): # kontrola kolize s tlačítkem2/start 
            menu = False # konec cyklu menu
        
        if mouserect.colliderect(tlacitko1): # kontrola kolize s tlačítkem2/start 
            menu = False 
            options = True
            #print("ano")
            options_menu(options)
            

        
        WIN.fill(BLACK) # vyplnění plochy černou barvou
        

        WIN.blit( menug ,menurectg) # kreslení obrázku menu na plochu(WIN)
        
        #pygame.draw.rect(WIN,WHITE,tlacitko2)

        #pygame.draw.rect(WIN,WHITE,tlacitko1)

        pygame.display.update() #update okna/plochy

    
menuf() # při spuštění se zavolá funkce pro menu


run = True

while run == True and beh == True:  # cyklus pro hlavní hru + kontrola toho, jestli hráč nechtěl náhodou v menu odejít
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # kontrola, jestli nechce hráč odejít
            run = False
            break 
    keys = pygame.key.get_pressed()
    
    paddle.movement(keys) # funkce pro pohyb pálky 
    ball.movement() # funkce pro pohyb míčku 
    WIN.fill(BLACK)  # vyplnění obrazovky/plochy černou 

    paddle.draw(WIN) # kreslení pálky 
    ball.draw(WIN) # kreslení míčku
    rectangle.draw_bricks(WIN) # kreslení bloků/cihliček
        # TEXT
    
    font = pygame.font.Font('freesansbold.ttf', 25) # font a výška pro skóre
    player_score = str(ball.score) + "/21" # string pro aktuální skóre
    text = font.render(player_score, True, WHITE) # vytvoření textu
    textRect = text.get_rect() # získání obdélníku pro text

    textRect.center = (WIDTH // 2, 25) # získání středu obdélníku textu

    if ball.score == 21:  # kontrola, zda hráč vyhrál
        font1 = pygame.font.Font('freesansbold.ttf', 50)    # font a výška pro skóre
        won = "YOU WON" # string pro výhru
        text1 = font1.render(won, True, WHITE, BLACK) # vytvoření textu
        WONRect = text1.get_rect() # získání obdélníku pro text
        WONRect.center = (WIDTH // 2, HEIGHT // 2) # získání středu obdélníku textu 
        WIN.blit(text1, WONRect) # kreslení textu pro výhru


    WIN.blit(text, textRect) # kreslení textu pro skóre

    


    pygame.display.update() # update plochy


pygame.quit() # odchod z programu