import pygame,sys

from random import randint


def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = test_font.render(f"Score:{current_time}", False, 'Black')
    score_rect = score_surf.get_rect(topleft=(0, 0))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom==300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)

        return obstacle_list
    return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom<300:
        player_surface = player_jump
    else:
        player_index+=0.1
        if player_index>=len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]



pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf',50)

game_active = False
start_time = 0
score = 0

#Convert all the png loaded images to a format pygame can easily work with
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#Pass AA as second argument to get smooth font.
text_surface = test_font.render("Runner", False, 'Black' )
text_rect = text_surface.get_rect(center = (400,50))
# test_surface.fill('Red')



#Obstacles

#Snail
snail_surface1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_surface2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_surfaces = [snail_surface1,snail_surface2]
snail_surface_index = 0
snail_surface = snail_surfaces[snail_surface_index]
# snail_rect = snail_surface.get_rect(midbottom = (800,300))
# snail_x_pos = 600


#Fly
fly_surface1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_surface2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_surfaces = [fly_surface1,fly_surface2]
fly_surface_index = 0
fly_surface = fly_surfaces[fly_surface_index]

obstacle_rect_list = []




#Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png')
player_surface = player_walk[player_index]
# player_surface1 = pygame.transform.flip(player_surface1,True,False)
# player_surface1 = pygame.transform.scale(player_surface1, (100, 100))
# using rectangles to place the object properly . We can have a contact b/w 2 rectangles.
#We have ground set at  (0,300) so we place the rectangle's y-axis at 300.
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.2)

bg_music = pygame.mixer.Sound('audio/music.wav')

bg_music.set_volume(0.2)


#Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale2x(player_stand)
# player_stand = pygame.transform.scale(player_stand,(150,150))
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center= (400,200))
start_text = test_font.render("Pixel Runner",False, "#50E59C")
start_text_rect = start_text.get_rect(center = (400,50))
instructions = test_font.render("Press space to start the game",False, "#50E59C")
instructions_rect = instructions.get_rect(center = (400,350))





#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
#Trigger the timer after every 1500 ms

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


while True:

    #Check for all the events which include player inputs...
    for event in pygame.event.get():
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("Mouse down")

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("Collision")

        if game_active:
            bg_music.play(loops = -1)
            if  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom>=300:
                player_gravity = -20
                jump_sound.play()


            if event.type == pygame.QUIT:

                #The pygame.quit counters the .init so the further while loop would throw an error if continued
                pygame.quit()
                sys.exit()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 700
                start_time = pygame.time.get_ticks()//1000
        if game_active:
            if event.type == obstacle_timer:
                n = randint(0,2)
                if n:
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))


            #Snail animations
            if event.type == snail_animation_timer:
                if snail_surface_index == 0: snail_surface_index = 1
                else: snail_surface_index = 0
                snail_surface = snail_surfaces[snail_surface_index]


            #Fly animations
            if event.type == fly_animation_timer:
                if fly_surface_index == 0: fly_surface_index = 1
                else: fly_surface_index = 0
                fly_surface = fly_surfaces[fly_surface_index]







    if game_active:
        # Block image transfer - Putting one surface on another
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(text_surface,text_rect)
        display_score()

        score = display_score()

        # screen.blit(snail_surface,snail_rect)
        # if snail_rect.left< -100: snail_rect.left = 800
        # snail_rect.left+=-5



        #Player
        player_gravity+=1
        player_rect.y+=player_gravity
        player_rect.bottom = min(player_rect.bottom, 300)
        player_animation()
        screen.blit(player_surface,player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        game_active = collisions(player_rect,obstacle_rect_list)

        display_score()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(start_text,start_text_rect)
        obstacle_rect_list = []
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_msg = test_font.render(f"You score is: {score}", False, "#50E59C")
        score_msg_rect = score_msg.get_rect(center=(400,330))

        if score==0:
            screen.blit(instructions, instructions_rect)
        else:
            screen.blit(score_msg,score_msg_rect)



    '''When using the classes, pygame.keys is a great option but for general stuff like closing the game, etc
     the event loop is an ideal place'''

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]: print("jump")


    #rect1.colliderect(rect2) is used for detection collisions b/w rectangles. Returns bool value

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_p
    # os):
    #     print(pygame.mouse.get_pressed())


    #Updates the frame to display the changes
    pygame.display.update()
    #Tels that pygame shouldn't run more than 60 times per second
    clock.tick(60)


