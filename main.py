 
import pygame
import pygame.locals
import sys
from random import randint
from time import sleep

# 0 = vide    BLACK
# 1 = rocher  WHITE
# 2 = bombe   RED
# 3 = joueur  GREEN
# 4 = explosion

def generation(l,h,nbrbombe=2):
    
    new_l = l*4
    new_h = h*4

    terrain = [list() for x in range(new_l)]
    for i in range(len(terrain)):
        terrain[i] = [0 for x in range(new_h)]

    for y in range(len(terrain)):
        for i in range(len(terrain[0])):
            case = randint(0,1)
            terrain[y][i] = case
    i = 0
    while i <= nbrbombe:
        bombe = [randint(1, len(terrain)-1), randint(0, len(terrain[0])-1)]
        if terrain[bombe[0]][bombe[1]] == 2:
            continue
        terrain[bombe[0]][bombe[1]] = 2
        i+=1


    #Joueur
    global J
    Jx = x = randint(0,new_l-1)
    Jy = y = randint(0,new_h-1)
    J = [x,y]
    terrain[x][y] = 3
    
    #compas
    global compas_pos
    while terrain[x][y]:
        x = randint(max(Jx-(l//2),0),min(new_l-1,Jx+(l//2)))
        y = randint(max(Jy-(h//2),0),min(new_h-1,Jy+(h//2)))
        compas_pos = (x,y)
    terrain[x][y] = 7 
    
    #map
    global map_pos
    while terrain[x][y]:
        x = randint(max(Jx-(l*2),0),min(new_l-1,Jx+(l*2)))
        y = randint(max(Jy-(h*2),0),min(new_h-1,Jy+(h*2)))
        map_pos = (x,y)
    terrain[x][y] = 9
    
    #gold
    global gold_pos
    while terrain[x][y]:
        x = randint(0,new_l-1)
        y = randint(0,new_h-1)
        gold_pos = (x,y)
    terrain[x][y] = 4

    return terrain


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
THEME = (204, 204, 204)#(102, 102, 153)
fontpath = "FONT/CONSOLA.TTF"

gridsize = [10,10] # min 10x10
width = height = 20
margin = 5
frame = 60

nbrbombe = int(0.2*(gridsize[0]*gridsize[1]))
nbrgold  = 1

info_width = 40
info_width += margin*2
text_height = 40


Jspeed = 5
Jspeed_time = frame // Jspeed

explode = fake_explode = False
explode_time = fake_explode_time = 0

anim_speed = frame//2

x_shift = 0
y_shift = 0   

J = compas_pos = gold_pos = map_pos = [0,0]
terrain = generation(gridsize[0],gridsize[1],nbrbombe)
Jb = 5
Jc = 0
Jm = 0
Jg = 0
miner_text = "Hey, bienvenue dans Bomber Miner !"

 
bomb = pygame.image.load('SPRITE/bomb.png')
bomb = pygame.transform.scale(bomb, (width,height))

rock = pygame.image.load('SPRITE/rock.png')
rock = pygame.transform.scale(rock, (width,height))

fake_rock = pygame.image.load('SPRITE/rock.png')
fake_rock = pygame.transform.scale(fake_rock, (width,height))

miner = pygame.image.load('SPRITE/miner.png')
miner = pygame.transform.scale(miner, (width,height))

background = pygame.image.load('SPRITE/background.png')
background = pygame.transform.scale(background, (width+margin+margin,height+margin+margin))

black = pygame.image.load('SPRITE/black.png')
black = pygame.transform.scale(black, (width,height))

explosion = pygame.image.load('SPRITE/explosion.png')
explosion = pygame.transform.scale(explosion, (width,height))

fake_explosion = pygame.image.load('SPRITE/explosion.png')
fake_explosion = pygame.transform.scale(fake_explosion, (width,height))

gold = pygame.image.load('SPRITE/gold.png')
gold = pygame.transform.scale(gold, (width,height))

compas = pygame.image.load('SPRITE/compas.png')
compas = pygame.transform.scale(compas, (width,height))

crossed_background = pygame.image.load('SPRITE/crossed_background.png')
crossed_background = pygame.transform.scale(crossed_background, (width,height))

map = pygame.image.load('SPRITE/map.png')
map = pygame.transform.scale(map, (width,height))

miner_head = pygame.image.load('SPRITE/miner_head.png')
miner_head = pygame.transform.scale(miner_head, (width*2,height*2))

bag_top = pygame.image.load('SPRITE/bag_top.png')
bag_top = pygame.transform.scale(bag_top, (info_width,height))
bag_bot = pygame.image.load('SPRITE/bag_bot.png')
bag_bot = pygame.transform.scale(bag_bot, (info_width,height))
bag_middle = pygame.image.load('SPRITE/bag_middle.png')
bag_middle = pygame.transform.scale(bag_middle, (info_width,height))

SPRITE = [None, rock, bomb, miner, fake_rock,explosion,gold,compas,crossed_background,map,fake_explosion]

rotate = False
block_entity = (1,3,4,5)
broke_entity = (0,1,2,4)


def retry():
    global terrain
    global gridsize
    global nbrbombe
    global J
    global Jb, Jc, Jm, Jg
    global x_shift, y_shift
    global miner_text
    
    #x_shift = 0
    #y_shift = 0
    terrain = generation(gridsize[0],gridsize[1],nbrbombe)
    Jb = 5
    Jc = 0
    Jm = 0
    Jg = 0
    miner_text = "Et c'est repartit :)"

pygame.init()


    
# Set the width and height of the screen [width, height]
size = ((width+margin) * gridsize[0] + margin + info_width , (height+margin) * gridsize[1] + margin + text_height)
screen = pygame.display.set_mode(size)

#background = pygame.transform.scale(background, (((width+margin) * gridsize[0] + margin + info_width),(height+margin) * gridsize[1] + margin))
 
pygame.display.set_caption("Bomber Miner")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------


while not done:
    
    # --- Main event loopget
    if Jspeed_time < frame//Jspeed:
        Jspeed_time +=1
        
    if Jg:
        miner_text = "Enfin, je suis riche ! Recommencer : [R]"
    
    x_shift = J[0]//gridsize[0]
    y_shift = J[1]//gridsize[1]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if Jb:
                    Jb -=1
                    if randint(0,1):
                        miner_text = "BOOM"
                    
                    if J[1]+1 < len(terrain[J[0]]):
                        if terrain[J[0]][J[1]+1] in broke_entity:
                            
                            if J[1]+1 >= gridsize[1]*(y_shift+1):
                                if terrain[J[0]][J[1]+1] == 4:
                                    terrain[J[0]][J[1]+1] = 6
                                else:
                                    terrain[J[0]][J[1]+1] = 0
                            else:
                                if terrain[J[0]][J[1]+1] == 4:
                                    terrain[J[0]][J[1]+1] = 10
                                else:                                
                                    terrain[J[0]][J[1]+1] = 5

                    if J[1]-1 >= 0:
                        if terrain[J[0]][J[1]-1] in broke_entity:
                                                 
                            
                            if J[1]-1 < gridsize[1]*(y_shift):
                                if terrain[J[0]][J[1]-1] == 4:
                                    terrain[J[0]][J[1]-1] = 6
                                else:
                                    terrain[J[0]][J[1]-1] = 0
                            else: 
                                if terrain[J[0]][J[1]-1] == 4:
                                    terrain[J[0]][J[1]-1] = 10
                                else:
                                    terrain[J[0]][J[1]-1] = 5

                    if J[0]+1 < len(terrain):
                        if terrain[J[0]+1][J[1]] in broke_entity:
                                                      
                            
                                
                            if J[0]+1 >= gridsize[0]*(x_shift+1):
                                if terrain[J[0]+1][J[1]] == 4:
                                    terrain[J[0]+1][J[1]] = 6
                                else:
                                    terrain[J[0]+1][J[1]] = 0 
                            else:
                                if terrain[J[0]+1][J[1]] == 4:
                                    terrain[J[0]+1][J[1]] = 10
                                else:                                
                                    terrain[J[0]+1][J[1]] = 5

                    if J[0]-1 >= 0:
                        if terrain[J[0]-1][J[1]] in broke_entity:
     
                            if J[0]-1 < gridsize[0]*(x_shift):
                                if terrain[J[0]-1][J[1]] == 4:
                                    terrain[J[0]-1][J[1]] = 6
                                else:
                                    terrain[J[0]-1][J[1]] = 0
                            else:
                                if terrain[J[0]-1][J[1]] == 4:
                                    terrain[J[0]-1][J[1]] = 10
                                else:                                
                                    terrain[J[0]-1][J[1]] = 5
            


            if event.key == pygame.K_r:
                retry()
            if event.key == pygame.K_p:
                print("-----------DEBUG-----------")
                print(f"Joueur_pos : {J[0]},{J[1]}")
                print(f"compas_pos : {compas_pos[0]},{compas_pos[1]}")
                print(f"gold_pos   : {gold_pos[0]},{gold_pos[1]}")
                print(f"map_pos    : {map_pos[0]},{map_pos[1]}")
                print(f"terrain    : {len(terrain)} x {len(terrain[0])}")
                print(f"gridsize   : {gridsize[0]} x {gridsize[1]}") 
                print(f"x_shift    : {x_shift}")
                print(f"y_shift    : {y_shift}") 

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = pos[0]//(width+margin) + (x_shift*gridsize[0]), pos[1]//(height+margin) + (y_shift*gridsize[1])   
            if x < (x_shift+1)*gridsize[0] :
                if terrain[x][y] == 0:
                    terrain[x][y] = 8 
                elif terrain[x][y] == 8:
                    terrain[x][y] = 0                 
                print(f"Column : {x} Row : {y} Entity : {terrain[x][y]}")    
    
    keys = pygame.key.get_pressed()
    
    for pressed in keys:
        if pressed: 
            new_pos = False
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                new_pos = [J[0]-1,J[1]]
                rotate  = True
        
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_pos = [J[0]+1,J[1]]
                rotate = False
        
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                new_pos = [J[0],J[1]-1]
           
        
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_pos = [J[0],J[1]+1]

            
            if new_pos:
                if Jspeed_time >= frame//Jspeed:
                    SPRITE[3] = pygame.transform.flip(miner, rotate, False)
                    
                    if 0 <= new_pos[0] < len(terrain) and 0 <= new_pos[1] < len(terrain[J[0]]):
                        if terrain[new_pos[0]][new_pos[1]] not in block_entity:
                        
                            #bomb      
                            if terrain[new_pos[0]][new_pos[1]] == 2:
                                Jb +=2
                                miner_text = "J'adore les bombes."
                            #compas
                            if terrain[new_pos[0]][new_pos[1]] == 7:
                                miner_text = "J'ai enfin retrouvé ma boussole !"
                                Jc = 1 
                            #map
                            if terrain[new_pos[0]][new_pos[1]] == 9:
                                miner_text = "Les coordonnées du trésor !!"
                                Jm = 1  
                            #gold
                            if terrain[new_pos[0]][new_pos[1]] == 6:
                                Jg = 1                            
                            
                            
                            if terrain[J[0]][J[1]] != 8: 
                                terrain[J[0]][J[1]] = 0
                            
                            terrain[new_pos[0]][new_pos[1]] = 3            
                            J = new_pos
                            Jspeed_time = 0
                        else:
                            miner_text = "Quelque chose bloque le passage."
                    else:
                        miner_text = "Impossible d'aller plus loin..."            
    
    
            

 
    # --- Game logic should go here
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(THEME)

    left = top = margin
    
    if explode:
        explode_time += 1
    if fake_explode:
        fake_explode_time += 1    
    
    for y in range(gridsize[1] * y_shift, min(gridsize[1]*(y_shift+1),len(terrain[0]))):
        for x in range(gridsize[0] * x_shift, min(gridsize[0]*(x_shift+1),len(terrain))):
            
            screen.blit(background, (left-margin, top-margin))
                        
            if terrain[x][y] == 5:
                explode = True
                
                if explode_time >= anim_speed:
                    terrain[x][y] = 0
                    explode = False
            
            
            if terrain[x][y] == 10:
                fake_explode = True
                
                if fake_explode_time >= anim_speed:
                    terrain[x][y] = 6
                    fake_explode = False            
                    
            if terrain[x][y]:
                screen.blit(SPRITE[terrain[x][y]], (left, top))
            
            left += width + margin
        
        top += width + margin
        left = margin
    
    if not explode:
        explode_time = 0
    
    if not fake_explode:
        fake_explode_time = 0    
        
    # --- Drawing the bag
   
    screen.blit(bag_top, ((width+margin) * gridsize[0] + margin, 0))
    for i in range(1,((height+margin) * gridsize[1] + margin)//height):
        screen.blit(bag_middle, ((width+margin) * gridsize[0] + margin, height * i))
    screen.blit(bag_bot,((width+margin) * gridsize[0] + margin, ((height+margin) * gridsize[1] + margin)-height))
    
    #put item in it
    
    left = size[0] - info_width
    top  = margin+height
    screen.blit(bomb, (left + info_width//2, top))

    font = pygame.font.Font(fontpath, 20)
    txt  = font.render(str(Jb), True, BLACK)
    rect = txt.get_rect(topright=(left+ info_width//2, top+3)) #setattr(rect, "center",   )
    screen.blit(txt, rect)
    
    
    #compas
    if Jc:
        font = pygame.font.Font(fontpath, 12)
        
        #Display player pos
        txt  = font.render(f"{J[0]},{J[1]}", True, BLACK)
        top  = (margin+height) * gridsize[1] - height+margin
        rect = txt.get_rect(center=(left+info_width//2, top)) 
        screen.blit(txt, rect)    
        
        #Display compas
        top = top - height - margin*2
        screen.blit(compas, (left+info_width//3, top))
        
        #Display map size
        #top = top - margin*2
        #txt  = font.render(f"{len(terrain)}x{len(terrain[0])}", True, BLACK)
        #rect = txt.get_rect(center=(left+info_width//2, top))         
        #screen.blit(txt, rect)
        
    #map
    if Jm:
        font = pygame.font.Font(fontpath, 12)
        top  = (margin+height) * gridsize[1] - height*2 - margin
        
        #Display gold pos
        txt  = font.render(f"{gold_pos[0]},{gold_pos[1]}", True, BLACK)
        top  = top - margin*4
        rect = txt.get_rect(center=(left+info_width//2, top)) 
        screen.blit(txt, rect)   
        
        #Display map
        top = top - margin*6
        screen.blit(map, (left+info_width//3, top))
    
    #gold
    if Jg:
        top  = (margin+height) * gridsize[1] - height*2 - margin*11
        #Display gold
        top = top - margin*6
        screen.blit(gold, (left+info_width//3, top))        
        
   
    #drawing head
    top = (margin+height) * gridsize[1] + margin
    screen.blit(miner_head, (left, top))
    
    #drawing the bulle
    pygame.draw.rect(screen,WHITE,pygame.Rect(0,top + margin, size[0]-info_width, text_height-10),0,10,border_bottom_right_radius=0)
    pygame.draw.rect(screen,BLACK,pygame.Rect(0,top + margin, size[0]-info_width, text_height-10),3,10,border_bottom_right_radius=0)
    
    #typing text
    font = pygame.font.Font(fontpath, 10)
    txt  = font.render(miner_text, True, BLACK) # max 41 char
    rect = txt.get_rect(center=((size[0]-info_width)//2, top + text_height//2)) 
    screen.blit(txt, rect)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(frame)
 
# Close the window and quit.
pygame.quit()