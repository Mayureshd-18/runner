import pygame,sys

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf',50)

#Convert all the png loaded images to a format pygame can easily work with
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#Pass AA as second argument to get smooth font.
text_surface = test_font.render("Runner", False, 'Black' )
# test_surface.fill('Red')

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x_pos = 600

while True:

    #Check for all the events which include player inputs...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            #The pygame.quit counters the .init so the further while loop would throw an error if continued
            pygame.quit()
            sys.exit()


    # Block image transfer - Putting one surface on another
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))

    screen.blit(snail_surface,(snail_x_pos,260))
    if snail_x_pos< -100:
        snail_x_pos = 800

    snail_x_pos+=-4




    #Updates the frame to display the changes
    pygame.display.update()
    #Tels that pygame shouldn't run more than 60 times per second
    clock.tick(60)


