import pygame
import random
import time

#resolution. if u change these, it's gonna look like ass
window_x = 1080
window_y = 720

#these will be swappable depending on dark/light mode
black = pygame.Color(0, 0, 0)
white = pygame.Color(200, 200, 200)

#game over text and fruit color are constant
red = pygame.Color(255, 0, 0)
blue = pygame.Color(100, 127, 255)

#snake colors will be pickable
green = pygame.Color(0, 255, 0)
pink = pygame.Color(255, 105, 180)
yellow = pygame.Color(255, 255, 0)
orange = pygame.Color(255, 165, 0)

#for snake2 only
brown = pygame.Color(150, 75, 0)

#colors used for menus
light = pygame.Color(170, 170, 170)
dark = pygame.Color(100, 100, 100)
menucolor = pygame.Color(60, 25, 60)

#create list of rocks for later use and initiate it with a dummy value 
#i dont think this really matters but it makes my vsc plugins happy
#purposefully put the coordinate out of bounds to prevent issues
rocks_list = [[window_x+1, window_y+1]]

#the act of creation comes with many burdens. handle them
pygame.init()
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

#play music
pygame.mixer.init()
pygame.mixer.music.load("chickendancesong.mp3")
pygame.mixer.music.play(-1)

def game(chosen_font, difficulty, color, lightmode, highscore, coop, audio):

    #initiate these so that we may access them later as local variables
    highscore_improve = False
    rock_spawned = False
    score = 0
    initialcolor = color

    #this is you. you are a snake. positions derived from start
    #snake spawn is a given, to prevent player frustration/confusion ie. build expectation
    snake_position = [50, 50]
    snake_body = [[50, 50],[40, 50],[30, 50],[20, 50]]

    #initial direction derived from the above (start position, body)
    direction = 'RIGHT'
    change_to = direction

    #create second snake for multiplayer games
    if coop == True:
        snake2_position = [window_x - 50, 50]
        snake2_body = [[window_x - 50, 50], [window_x - 40, 50], [window_x - 30, 50], [window_x - 20, 50]]
        direction2 = 'LEFT2'
        change_to_2 = direction2
        #co op fruit and rock spawning
        fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
        rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)
        #add rock position to list
        rocks_list.append(rock_position)
    
    #spawn initial fruit and rocks
    else:
        fruit_position = gen_fruit(snake_body, rocks_list)
        rock_position = gen_rocks(rocks_list, snake_body, fruit_position)
        #add rock position to list
        rocks_list.append(rock_position)
        
        #handle drawing score stuff for not-coop mode
        #N.B.: these 4 steps (font -> surface -> rect -> blit) happen constantly
        #throughout the program. this is the only time they have comments
        def show_score(color, font, size):
            #prep font
            score_font = pygame.font.SysFont(font, size)
            #render surace object
            score_surface = score_font.render('Total points: ' + str(score), True, color)
            #create rectangle
            score_rect = score_surface.get_rect()
            #draw score in window using blit
            game_window.blit(score_surface, score_rect)

        #also draw high score
        def show_highscore(color, font, size):
            highscore_font = pygame.font.SysFont(font, size)
            highscore_surface = highscore_font.render('High score: ' + str(highscore), True, color)
            highscore_rect = highscore_surface.get_rect()
            #handles offset for highscore
            highscore_rect.midtop = (window_x - 100, 0)
            game_window.blit(highscore_surface, highscore_rect)
    fruit_active = True

    #the game has to end somehow
    def game_over(highscore_improve, winner):

        #generate font for ending text
        big_text = pygame.font.SysFont(chosen_font, 50)
        small_text = pygame.font.SysFont(chosen_font, 20)
        color = initialcolor
        
        if coop == False:
            #prep small text to prompt closing the screen
            #(position and size calculated dynamically)
            game_over_smalltext = small_text.render('Press q to quit, r to restart or m for menu.', True, red)
            game_over_small = game_over_smalltext.get_rect()
            game_over_small.midtop = (window_x / 2, 2 * window_y / 5 + window_y / 10)
            game_window.blit(game_over_smalltext, game_over_small)
        
            #prep big text to talk about end score
            #(position and size calculated dynamically)
            if score == 1:
                game_over_bigtext = big_text.render('You scored ' + str(score) + ' point.', True, red)
                game_over = game_over_bigtext.get_rect()
                game_over.midtop = (window_x / 2, 2 * window_y / 5)
                game_window.blit(game_over_bigtext, game_over)
            else:
                game_over_bigtext = big_text.render('You scored ' + str(score) + ' points.', True, red)
                game_over = game_over_bigtext.get_rect()
                game_over.midtop = (window_x / 2, 2 * window_y / 5)
                game_window.blit(game_over_bigtext, game_over)

            #if a high score was improved, inform the user of this
            if score == highscore and highscore_improve == True:
                highscore_text = pygame.font.SysFont(chosen_font, 35)
                highscore_text_render = highscore_text.render('That was a high score! NICE :D', True, red)
                highscore_text_rect = highscore_text_render.get_rect()
                highscore_text_rect.midtop = (window_x / 2, 3 * window_y / 5)
                game_window.blit(highscore_text_render, highscore_text_rect)

            #if a high score was tied, taunt the user. do better next time noob
            elif score == highscore and highscore_improve == False:
                highscore_text = pygame.font.SysFont(chosen_font, 35)
                highscore_text_render = highscore_text.render('Oof, so close... Better luck next time!', True, red)
                highscore_text_rect = highscore_text_render.get_rect()
                highscore_text_rect.midtop = (window_x / 2, 3 * window_y / 5)
                game_window.blit(highscore_text_render, highscore_text_rect)

        #co-op doesn't need to talk about score,
        #so the game can restart automatically
        else:
            game_over_smalltext = small_text.render('Game is restarting...', True, red)
            game_over_small = game_over_smalltext.get_rect()
            game_over_small.midtop = (window_x / 2, 2 * window_y / 5 + window_y / 10)
            game_window.blit(game_over_smalltext, game_over_small)
            if winner == "draw":
                game_over_bigtext = big_text.render("It's a draw. Everyone loses!", True, red)
                game_over = game_over_bigtext.get_rect()
                game_over.midtop = (window_x / 2, 2 * window_y / 5)
                game_window.blit(game_over_bigtext, game_over)
            if winner == "Player 2":
                game_over_bigtext = big_text.render("The winner is player 2!", True, red)
                game_over = game_over_bigtext.get_rect()
                game_over.midtop = (window_x / 2, 2 * window_y / 5)
                game_window.blit(game_over_bigtext, game_over)
            if winner == "Player 1":
                game_over_bigtext = big_text.render("The winner is player 1!", True, red)
                game_over = game_over_bigtext.get_rect()
                game_over.midtop = (window_x / 2, 2 * window_y / 5)
                game_window.blit(game_over_bigtext, game_over)

        pygame.display.flip()
        
        #for single player we wait for user input to kill game_window 
        #so they may fawn over their score for as long as they like
        if coop == False:
            for event in pygame.event.get():
                #exit game if exit button to close window is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #look for the requested keypresses (q,r,m)
                if event.type == pygame.KEYDOWN:
                    #death
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    #run it again
                    if event.key == pygame.K_r:
                        rocks_list.clear()
                        game(chosen_font, difficulty, color, lightmode, highscore, coop, audio)
                    #back to menus
                    if event.key == pygame.K_m:
                        rocks_list.clear()
                        start_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio)

        #for coop we kill the game after a certain amount of time
        #highscores are still carried in case of mode switches
        else:
            time.sleep(5)
            #clear list of rocks before a restart
            rocks_list.clear()
            start_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio)

    while True:
        if pygame.mixer.music.get_busy == False and audio == True:
            pygame.mixer.music.load("chickendancesong.mp3")
            pygame.mixer.music.play(-1)
        
        if audio == False:
            pygame.mixer.music.pause()

        fruit_eaten = pygame.mixer.Sound("heavyeating.mp3")
        #pygame style input handling
        if coop == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'
                    if event.key == pygame.K_w:
                        change_to = 'UP'
                    if event.key == pygame.K_s:
                        change_to = 'DOWN'
                    if event.key == pygame.K_a:
                        change_to = 'LEFT'
                    if event.key == pygame.K_d:
                        change_to = 'RIGHT'

        #inputs are split for coop. wasd for player1, arrow keys for player2.
        #player2 has a 2 appended to their directions etc. as to not accidently move player1.
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to_2 = 'UP2'
                    if event.key == pygame.K_DOWN:
                        change_to_2 = 'DOWN2'
                    if event.key == pygame.K_LEFT:
                        change_to_2 = 'LEFT2'
                    if event.key == pygame.K_RIGHT:
                        change_to_2 = 'RIGHT2'
                    if event.key == pygame.K_w:
                        change_to = 'UP'
                    if event.key == pygame.K_s:
                        change_to = 'DOWN'
                    if event.key == pygame.K_a:
                        change_to = 'LEFT'
                    if event.key == pygame.K_d:
                        change_to = 'RIGHT'
    
        #only update the direction if we're not turning 180 degrees
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if coop == True:
            if change_to_2 == 'UP2' and direction2 != 'DOWN2':
                direction2 = 'UP2'
            if change_to_2 == 'DOWN2' and direction2 != 'UP2':
                direction2 = 'DOWN2'
            if change_to_2 == 'LEFT2' and direction2 != 'RIGHT2':
                direction2 = 'LEFT2'
            if change_to_2 == 'RIGHT2' and direction2 != 'LEFT2':
                direction2 = 'RIGHT2'

        #movement takes the last input and applies it to the snake's position
        #the snake's position is an array with two coordinates, x and y
        #bc it's not mentioned anywhere else, a block is 10,10 in size
        #ie. moving one block to right means u move 10,0, left -10,0, up/down 0,-10/0,10
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        if coop == True:
            if direction2 == 'UP2':
                snake2_position[1] -= 10
            if direction2 == 'DOWN2':
                snake2_position[1] += 10
            if direction2 == 'LEFT2':
                snake2_position[0] -= 10
            if direction2 == 'RIGHT2':
                snake2_position[0] += 10

        #the snake moves by adding a new snake_position into the list
        #the body is 'simply' a list of positions that it currently exists on
        snake_body.insert(0, list(snake_position))
        if coop == False:
            #the snake grows when the head position matches the fruit position
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 1
                pygame.mixer.Sound.play(fruit_eaten)
                if score > highscore:
                    highscore_improve = True
                    highscore = score
                fruit_active = False
                rock_spawned = False
            #if the snake didn't match a fruit, remove the end
            #because moving adds an entry to the list, we pop the last part of the list
            #that way our size stays the same
            else:
                snake_body.pop()
        #in coop the goal isnt to score points. the goal is to win
        #we can omit high score type functionality
        else:
            snake2_body.insert(0, list(snake2_position))
            if snake2_position[0] == fruit_position[0] and snake2_position[1] == fruit_position[1]:
                #in coop score is only used to spawn more rocks
                score += 1
                pygame.mixer.Sound.play(fruit_eaten)
                fruit_active = False
                rock_spawned = False
            else:
                snake2_body.pop()

            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                #in coop score is only used to spawn more rocks
                score += 1
                fruit_active = False
                rock_spawned = False
            else:
                snake_body.pop()

        #spawn extra rocks every 5 points
        if score % 5 == 1 and rock_spawned == False:
            if coop == False:
                rock_position = gen_rocks(rocks_list, snake_body, fruit_position)
            else:
                rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)
            rocks_list.append(rock_position)
            #comment out the next line to debug rock spawning algorithm   
            rock_spawned = True

        #if there is no fruit, create more fruit
        if coop == False:
            if fruit_active == False:
                fruit_position = gen_fruit(snake_body, rocks_list)
                #comment out the next line if u need to debug the fruit generation algorithm
                fruit_active = True
        else:
            if fruit_active == False:
                fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
                #comment out the next line if u need to debug the fruit generation algorithm
                fruit_active = True

        #start drawing graphics
        #first draw background color depending on light/darkmode
        if lightmode == False:
            game_window.fill(black)
        else:
            game_window.fill(white)    
        
        #then loop through snake's body and draw each bit
        for pos in snake_body:
            #if the player is doing well, show cool visuals
            if highscore_improve == True:
                color = iterate_rainbow(color)
            pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], 10, 10))
        if coop == True:
            for pos in snake2_body:
                pygame.draw.rect(game_window, brown, pygame.Rect(pos[0], pos[1], 10, 10))
    
        #now draw fruit and rocks
        pygame.draw.rect(game_window, blue, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
        for rock in rocks_list:
            if lightmode == False:
                pygame.draw.rect(game_window, light, pygame.Rect(rock[0], rock[1], 10, 10))
            else:
                pygame.draw.rect(game_window, black, pygame.Rect(rock[0], rock[1], 10, 10))            

        #code to draw head of snake
        if direction == "UP":
            snake_head = pygame.image.load("snakehead_up.png")
            game_window.blit(snake_head, (snake_position[0] - 5, snake_position[1] - 20))
        elif direction == "RIGHT":
            snake_head = pygame.image.load("snakehead_right.png")
            game_window.blit(snake_head, (snake_position[0] + 10, snake_position[1] - 5))
        elif direction == "LEFT":
            snake_head = pygame.image.load("snakehead_left.png")
            game_window.blit(snake_head, (snake_position[0] - 20, snake_position[1] - 5))
        elif direction == "DOWN":
            snake_head = pygame.image.load("snakehead_down.png")
            game_window.blit(snake_head, (snake_position[0] - 5, snake_position[1] + 10))

        if coop == True:
            if direction2 == "UP2":
                snake2_head = pygame.image.load("snakehead_up.png")
                game_window.blit(snake2_head, (snake2_position[0] - 5, snake2_position[1] - 20))
            elif direction2 == "RIGHT2":
                snake2_head = pygame.image.load("snakehead_right.png")
                game_window.blit(snake2_head, (snake2_position[0] + 10, snake2_position[1] - 5))
            elif direction2 == "LEFT2":
                snake2_head = pygame.image.load("snakehead_left.png")
                game_window.blit(snake2_head, (snake2_position[0] - 20, snake2_position[1] - 5))
            elif direction2 == "DOWN2":
                snake2_head = pygame.image.load("snakehead_down.png")
                game_window.blit(snake2_head, (snake2_position[0] - 5, snake2_position[1] + 10))

        #here we begin to look for death conditions.
        #we begin with co-op in case of draws. we handle these first
        #this is bc of the linear nature of code
        if coop == True:

            #check if both snakes are hitting walls at the same time
            #case: both snakes x-coords out of bounds
            if (snake_position[0] < 0 or snake_position[0] > window_x - 10) and (snake2_position[0] < 0 or snake2_position[0] > window_x - 10):
                game_over(highscore_improve, "draw")
            #case: both snakes y-coords out of bounds
            if (snake_position[1] < 0 or snake_position[1] > window_y - 10) and (snake2_position[1] < 0 or snake2_position[1] > window_y - 10):
                game_over(highscore_improve, "draw")
            #case: snake1 x-coords, snake2 y-coords
            if (snake_position[0] < 0 or snake_position[0] > window_x - 10) and (snake2_position[1] < 0 or snake2_position[1] > window_y - 10):
                game_over(highscore_improve, "draw")
            #case: snake1 y-coords, snake2 x-coords
            if (snake_position[1] < 0 or snake_position[1] > window_y - 10) and (snake2_position[0] < 0 or snake2_position[0] > window_x - 10):
                game_over(highscore_improve, "draw")

            #check for rock collision
            for rock in rocks_list:
                #case: snake1 eats rock while snake1 eats wall on y-coord
                if (snake_position[0] == rock[0] and snake_position[1] == rock[1]) and (snake2_position[0] < 0 or snake2_position[0] > window_x - 10):
                    game_over(highscore_improve, "draw")
                #case: snake1 eats rock while snake1 eats wall on y-coord
                if (snake_position[0] == rock[0] and snake_position[1] == rock[1]) and (snake2_position[1] < 0 or snake2_position[1] > window_y - 10):
                    game_over(highscore_improve, "draw")
                #case: snake2 eats rock while snake1 eats wall on x-coord
                if (snake2_position[0] == rock[0] and snake2_position[1] == rock[1]) and (snake_position[0] < 0 or snake_position[0] > window_x - 10):
                    game_over(highscore_improve, "draw")
                #case: snake2 eats rock while snake1 eats wall on y-coord
                if (snake2_position[0] == rock[0] and snake2_position[1] == rock[1]) and (snake_position[1] < 0 or snake_position[1] > window_y - 10):
                    game_over(highscore_improve, "draw")

            #check for a head-on collision
            if snake_position[0] == snake2_position[0] and snake_position[1] == snake2_position[1]:
                game_over(highscore_improve, "draw")

            #check if snake2 is hitting the walls
            if snake2_position[0] < 0 or snake2_position[0] > window_x - 10:
                game_over(highscore_improve, "Player 1")
            if snake2_position[1] < 0 or snake2_position[1] > window_y - 10:
                game_over(highscore_improve, "Player 1")

            #check for self-touch of snake2 during coop
            for block in snake2_body[1:]:
                if snake2_position[0] == block[0] and snake2_position[1] == block[1]:
                    game_over(highscore_improve, "Player 1")

            #if snake2's head is found to match any point in snake1's body
            #it means snake2 lost the game            
            for entry in snake_body:
                if snake2_position[0] == entry[0] and snake2_position[1] == entry[1]:
                    game_over(highscore_improve, "Player 1")

            #in these cases snake1 touched snake2
            #so player2 is declared a winner
            for entry in snake2_body:
                if snake_position[0] == entry[0] and snake_position[1] == entry[1]:
                    game_over(highscore_improve, "Player 2")
        
            #snake dies to rocks also
            for rock in rocks_list:
                if snake2_position[0] == rock[0] and snake2_position[1] == rock[1]:
                    game_over(highscore_improve, "Player 1")

        #game ends if bounds of map are exceeded
        #x-coordinates
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            if coop == False:
                #snake is teleported to out of bounds. this is jank, but it works
                #the alternative is that the snake keeps moving while the game waits for input
                #which is even weirder (and obvious)
                snake_position[0] = window_x + 10
                snake_position[1] = window_y + 10
            game_over(highscore_improve, "Player 2")
        #y-coordinates
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            if coop == False:
                snake_position[0] = window_x + 10
                snake_position[1] = window_y + 10
            game_over(highscore_improve, "Player 2")

        #game ends if self is touched
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                if coop == False:
                    snake_position[0] = window_x + 10
                    snake_position[1] = window_y + 10
                game_over(highscore_improve, "Player 2")

        #snake dies to rocks also
        for rock in rocks_list:
            if snake_position[0] == rock[0] and snake_position[1] == rock[1]:
                if coop == False:
                    snake_position[0] = window_x + 10
                    snake_position[1] = window_y + 10
                game_over(highscore_improve, "Player 2")
                   
        #score display during game (also does highscore)
        #no score in co-op
        if coop == False:
            if lightmode == False:
                show_score(white, chosen_font, 20)
                show_highscore(white, chosen_font, 20)
            else:
                show_score(black, chosen_font, 20)
                show_highscore(black, chosen_font, 20)
    
        pygame.display.update()
        #difficulty changes snake speed
        if difficulty == "Easy":
            snake_speed = 10
        elif difficulty == "Normal":
            snake_speed = 17
        elif difficulty == "Hard":
            snake_speed = 25
        elif difficulty == "Extreme":
            snake_speed = 33
        fps.tick(snake_speed)

#main menu
#text formatting is 'hard coded' according to the font
#this is because each font is interpreted differently
#i am aware this sucks
def start_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio):
    while True:
        #decide color of window
        game_window.fill(menucolor)

        #track mouse movements
        mouse = pygame.mouse.get_pos()

        #prep menu sound
        menu_blip = pygame.mixer.Sound("pokeconfirm.mp3")           

        #draw images on menu screen
        logo1 = pygame.image.load("logo1.png")
        game_window.blit(logo1, (window_x / 2 - 145, 35))
        logo2 = pygame.image.load("logo2.png")
        game_window.blit(logo2, (0, 20))
        logo3 = pygame.image.load("logo3.png")
        game_window.blit(logo3, (700, 50))

        #define buttons
        #this is done programatically, the screen is divided into 2n+1 parts
        #where n is the amount of buttons
        play_button_outline = pygame.Rect(window_x / 3 - 10, 3 * window_y / 9 - 10, window_x / 3 + 20, window_y / 9 + 20)
        play_button = pygame.Rect(window_x / 3, 3 * window_y / 9, window_x / 3, window_y / 9)
        options_button_outline = pygame.Rect(window_x / 3 - 10, 5 * window_y / 9 - 10, window_x / 3 + 20, window_y / 9 + 20)
        options_button = pygame.Rect(window_x / 3, 5 * window_y / 9, window_x / 3, window_y / 9)
        quit_button_outline = pygame.Rect(window_x / 3 - 10, 7 * window_y / 9 - 10, window_x / 3 + 20, window_y / 9 + 20)
        quit_button = pygame.Rect(window_x / 3, 7 * window_y / 9, window_x / 3, window_y / 9)

        #sound stuff
        sound_button = pygame.Rect(1000, 640, 1064, 704)
        audiologo_on = pygame.image.load("volumeon.png")
        audiologo_off = pygame.image.load("volumeoff.png")
        if audio == False:
            game_window.blit(audiologo_off, (1000, 640))
        if audio == True:
            game_window.blit(audiologo_on, (1000, 640))

        #start drawing buttons
        #first draw a static outline
        #then, draw the dynamic button over this
        #dynamic in the sense it changes color when hovered over
        pygame.draw.rect(game_window, black, play_button_outline)
        pygame.draw.rect(game_window, light if play_button.collidepoint(mouse) else dark, play_button)
        pygame.draw.rect(game_window, black, options_button_outline)
        pygame.draw.rect(game_window, light if options_button.collidepoint(mouse) else dark, options_button)
        pygame.draw.rect(game_window, black, quit_button_outline)
        pygame.draw.rect(game_window, light if quit_button.collidepoint(mouse) else dark, quit_button)
        
        #put text on buttons
        font = pygame.font.SysFont(chosen_font, 50)

        #text should be colored differently depending on wether we have dark or light mode
        if lightmode == False:
            play_text = font.render("Play", True, white)
            options_text = font.render("Options", True, white)
            quit_text = font.render("Quit", True, white)
        else:
            play_text = font.render("Play", True, black)
            options_text = font.render("Options", True, black)
            quit_text = font.render("Quit", True, black)

        #we handle each font seperatly bc the renderer has strange quirks for each one
        #ie they get drawn slightly differently and as such need to be spaced differently
        if chosen_font == "Comic Sans MS":
            game_window.blit(play_text, (window_x / 3 + 20, 3 * window_y / 9))
            game_window.blit(options_text, (window_x / 3 + 20, 5 * window_y / 9))
            game_window.blit(quit_text, (window_x / 3 + 20, 7 * window_y / 9))
        elif chosen_font == "Bahnschrift":
            game_window.blit(play_text, (window_x / 3 + 20, 3 * window_y / 9 + 15))
            game_window.blit(options_text, (window_x / 3 + 20, 5 * window_y / 9 + 15))
            game_window.blit(quit_text, (window_x / 3 + 20, 7 * window_y / 9 + 15))
        elif chosen_font == "Calibri":
            game_window.blit(play_text, (window_x / 3 + 20, 3 * window_y / 9 + 15))
            game_window.blit(options_text, (window_x / 3 + 20, 5 * window_y / 9 + 15))
            game_window.blit(quit_text, (window_x / 3 + 20, 7 * window_y / 9 + 15))
        elif chosen_font == "Impact":
            game_window.blit(play_text, (window_x / 3 + 20, 3 * window_y / 9 + 10))
            game_window.blit(options_text, (window_x / 3 + 20, 5 * window_y / 9 + 10))
            game_window.blit(quit_text, (window_x / 3 + 20, 7 * window_y / 9 + 10))

        #handle pressing of buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    game(chosen_font, difficulty, color, lightmode, highscore, coop, audio)
                if options_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    options_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio)
                if sound_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    if audio == False:
                        audio = True
                        pygame.mixer.music.unpause()
                    else:
                        audio = False
                        pygame.mixer.music.pause()
                if quit_button.collidepoint(mouse):
                    pygame.quit()
                    quit()
        pygame.display.update()

def options_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio):
    while(1):
        #create window and track mouse
        game_window.fill(menucolor)
        mouse = pygame.mouse.get_pos()

        #prep menu sound
        menu_blip = pygame.mixer.Sound("pokeconfirm.mp3")

        #prep image for vulume button
        audiologo_on = pygame.image.load("volumeon.png")
        audiologo_off = pygame.image.load("volumeoff.png")

        #create buttons
        difficulty_button_outline = pygame.Rect(window_x / 4 - 10, window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        difficulty_button = pygame.Rect(window_x / 4, window_y / 13, window_x / 2, window_y / 13)
        font_button_outline = pygame.Rect(window_x / 4 - 10, 3 * window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        font_button = pygame.Rect(window_x / 4, 3 * window_y / 13, window_x / 2, window_y / 13)
        color_button_outline = pygame.Rect(window_x / 4 - 10, 5 * window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        color_button = pygame.Rect(window_x / 4 , 5 * window_y / 13, window_x / 2, window_y / 13)
        mode_button_outline = pygame.Rect(window_x / 4 - 10, 7 * window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        mode_button = pygame.Rect(window_x / 4, 7 * window_y / 13, window_x / 2, window_y / 13)
        coop_button_outline = pygame.Rect(window_x / 4 - 10, 9 * window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        coop_button = pygame.Rect(window_x / 4, 9 * window_y / 13, window_x / 2, window_y / 13)
        back_button_outline = pygame.Rect(window_x / 4 - 10, 11 * window_y / 13 - 10, window_x / 2 + 20, window_y / 13 + 20)
        back_button = pygame.Rect(window_x / 4, 11 * window_y / 13, window_x / 2, window_y / 13)

        #draw button for volume
        sound_button = pygame.Rect(1000, 640, 1064, 704)
        if audio == False:
            game_window.blit(audiologo_off, (1000, 640))
        if audio == True:
            game_window.blit(audiologo_on, (1000, 640))

        #buttons first draw an outline which is statically colored.
        #after that, draw the button itself
        #buttons change color when hovered over
        pygame.draw.rect(game_window, black, difficulty_button_outline)
        pygame.draw.rect(game_window, light if difficulty_button.collidepoint(mouse) else dark, difficulty_button)
        pygame.draw.rect(game_window, black, font_button_outline)
        pygame.draw.rect(game_window, light if font_button.collidepoint(mouse) else dark, font_button)
        pygame.draw.rect(game_window, black, color_button_outline)
        pygame.draw.rect(game_window, light if color_button.collidepoint(mouse) else dark, color_button)
        pygame.draw.rect(game_window, black, mode_button_outline)
        pygame.draw.rect(game_window, light if mode_button.collidepoint(mouse) else dark, mode_button)
        pygame.draw.rect(game_window, black, coop_button_outline)
        pygame.draw.rect(game_window, light if coop_button.collidepoint(mouse) else dark, coop_button)
        pygame.draw.rect(game_window, black, back_button_outline)
        pygame.draw.rect(game_window, light if back_button.collidepoint(mouse) else dark, back_button)

        #prep text for buttons
        font = pygame.font.SysFont(chosen_font, 50)
        if lightmode == False:
            difficulty_text = font.render("Difficulty: " + difficulty, True, white)
            font_text = font.render("Font: " + chosen_font, True, white)
            if color == green:
                color_text = font.render("Snake color: Green", True, white)
            elif color == yellow:
                color_text = font.render("Snake color: Yellow", True, white)
            elif color == pink:
                color_text = font.render("Snake color: Pink", True, white)
            elif color == orange:
                color_text = font.render("Snake color: Orange", True, white)         
            mode_text = font.render("Dark mode", True, white)
            if coop == True:
                coop_text = font.render("Versus Mode", True, white)
            else:
                coop_text = font.render("High Score Mode", True, white)
            back_text = font.render("Back", True, white)
        else:
            difficulty_text = font.render("Difficulty: " + difficulty, True, black)
            font_text = font.render("Font: " + chosen_font, True, black)
            if color == green:
                color_text = font.render("Snake color: Green", True, black)
            elif color == yellow:
                color_text = font.render("Snake color: Yellow", True, black)
            elif color == pink:
                color_text = font.render("Snake color: Pink", True, black)
            elif color == orange:
                color_text = font.render("Snake color: Orange", True, black)
            if coop == True:
                coop_text = font.render("Versus Mode", True, black)
            else:
                coop_text = font.render("High Score Mode", True, black)
            mode_text = font.render("Light mode", True, black)
            back_text = font.render("Back", True, black)

        #draw text for buttons
        #offset/padding is different for each font
        if chosen_font == "Comic Sans MS":
            game_window.blit(difficulty_text, (window_x / 4 + 20, window_y / 13 - 10))
            game_window.blit(font_text, (window_x / 4 + 20, 3 * window_y / 13 - 10))
            game_window.blit(color_text, (window_x / 4 + 20, 5 * window_y / 13 - 10))
            game_window.blit(mode_text, (window_x / 4 + 20, 7 * window_y / 13 - 10))
            game_window.blit(coop_text, (window_x / 4 + 20, 9 * window_y / 13 - 10))
            game_window.blit(back_text, (window_x / 4 + 20, 11 * window_y / 13 - 10))

        elif chosen_font == "Bahnschrift":
            game_window.blit(difficulty_text, (window_x / 4 + 20, window_y / 13 + 5))
            game_window.blit(font_text, (window_x / 4 + 20, 3 * window_y / 13 + 5))
            game_window.blit(color_text, (window_x / 4 + 20, 5 * window_y / 13 + 5))
            game_window.blit(mode_text, (window_x / 4 + 20, 7 * window_y / 13 + 5))
            game_window.blit(coop_text, (window_x / 4 + 20, 9 * window_y / 13 + 5))
            game_window.blit(back_text, (window_x / 4 + 20, 11 * window_y / 13 + 5))
        elif chosen_font == "Calibri":
            game_window.blit(difficulty_text, (window_x / 4 + 20, window_y / 13 + 5))
            game_window.blit(font_text, (window_x / 4 + 20, 3 * window_y / 13 + 5))
            game_window.blit(color_text, (window_x / 4 + 20, 5 * window_y / 13 + 5))
            game_window.blit(mode_text, (window_x / 4 + 20, 7 * window_y / 13 + 5))
            game_window.blit(coop_text, (window_x / 4 + 20, 9 * window_y / 13 + 5))
            game_window.blit(back_text, (window_x / 4 + 20, 11 * window_y / 13 + 5))
        elif chosen_font == "Impact":
            game_window.blit(difficulty_text, (window_x / 4 + 20, window_y / 13 - 5))
            game_window.blit(font_text, (window_x / 4 + 20, 3 * window_y / 13 - 5))
            game_window.blit(color_text, (window_x / 4 + 20, 5 * window_y / 13 - 5))
            game_window.blit(mode_text, (window_x / 4 + 20, 7 * window_y / 13 - 5))
            game_window.blit(coop_text, (window_x / 4 + 20, 9 * window_y / 13 - 5))
            game_window.blit(back_text, (window_x / 4 + 20, 11 * window_y / 13 - 5))

        #handle on click events for options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #this handles clicking on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    difficulty = increment_difficulty(difficulty, chosen_font, color, lightmode, highscore, coop, audio)
                if font_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    chosen_font = increment_font(chosen_font, difficulty, color, lightmode, highscore, coop, audio)
                if color_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    color = increment_color(color, chosen_font, difficulty, lightmode, highscore, coop, audio)
                if sound_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    if audio == False:
                        audio = True
                        pygame.mixer.music.unpause()
                    else:
                        audio = False
                        pygame.mixer.music.pause()
                if mode_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    if lightmode == False:
                        lightmode = True
                    else:
                        lightmode = False
                if coop_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    if coop == False:
                        coop = True
                    else:
                        coop = False
                if back_button.collidepoint(mouse):
                    pygame.mixer.Sound.play(menu_blip)
                    start_menu(chosen_font, difficulty, color, lightmode, highscore, coop, audio)
        pygame.display.update()

#basic font selection funciton that loops thru a list indefinitly.
def increment_font(font, difficulty, color, lightmode, highscore, coop, audio):
    i = 0
    #create list of fonts
    #python picks these from your system fonts so if you do not have them they will show as blank
    #if running this locally, then change these to be some kinda font you do have on your machine
    #do note that a lot of padding and spacing of text on buttons was hard-coded to fit these fonts
    #and so, by changing fonts, stuff will likely look bad
    font_list = ["Comic Sans MS", "Bahnschrift", "Calibri", "Impact"]
    #loop thru fonts
    for entry in font_list:
        if entry == font:
            #if font isnt last one in list, select next
            if i != len(font_list) - 1:
                font = font_list[i + 1]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
            #if font is last one, select entry 0
            else:
                font = font_list[0]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
        i += 1

#reused font function, using difficulties
def increment_difficulty(difficulty, font, color, lightmode, highscore, coop, audio):
    i = 0
    #create list of difficulties
    difficulty_list = ["Easy", "Normal", "Hard", "Extreme"]
    for entry in difficulty_list:
        if entry == difficulty:
            #if difficulty isnt last one in list, select next
            if i != len(difficulty_list) - 1:
                difficulty = difficulty_list[i + 1]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
            #if difficulty is last one, select entry 0
            else:
                difficulty = difficulty_list[0]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
        i += 1

#this is essentially the same function as used for fonts
#just with color this time
def increment_color(color, font, difficulty, lightmode, highscore, coop, audio):
    i = 0
    #create list of colors
    color_list = [green, pink, orange, yellow]
    #loop thru colors
    for entry in color_list:
        if entry == color:
            #if color isnt last one in list, select next
            if i != len(color_list) - 1:
                color = color_list[i + 1]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
            #if color is last one, select entry 0
            else:
                color = color_list[0]
                options_menu(font, difficulty, color, lightmode, highscore, coop, audio)
        i += 1

#this function loops through our rainbow to find the next
def iterate_rainbow (color):
    rainbow_list = [red, orange, yellow, green, blue, menucolor, pink]
    i = 0
    #loop through rainbow
    for entry in rainbow_list:
        #find the color we currently have
        if entry == color:
            #return next entry
            if i != len(rainbow_list) - 1:
                return rainbow_list[i + 1]
            #or return start of list
            else:
                return rainbow_list[0]
        i += 1


#function that generates a new fruit spawn
def gen_fruit(snake_body, rocks_list):
    #generate a random position for the fruit within the range of the screen
    fruit_position = [random.randrange(0, (window_x // 10)) * 10, random.randrange(0, (window_y // 10)) * 10]

    #check if newly spanwed fruit spawned inside a rock
    for rock in rocks_list:
        if fruit_position[0] == rock[0] and fruit_position[1] == rock[1]:
            fruit_position = gen_fruit(snake_body, rocks_list)

    #loop thru the snake_body, making sure the fruit spawns on both a different x and y coordinate
    #this ensures the fruit doesn't spawn inside the snake and that user inputs are required to pick up the fruit
    for entry in snake_body:
        if fruit_position[0] == entry[0]:
            fruit_position = gen_fruit(snake_body, rocks_list)
        elif fruit_position[1] == entry[1]:
            fruit_position = gen_fruit(snake_body, rocks_list)

    #for quality of life we avoid spawning fruit in the outer ring (is this too nice?)
    if fruit_position[0] < 21:
        fruit_position = gen_fruit(snake_body, rocks_list)
    elif fruit_position[1] < 21:
        fruit_position = gen_fruit(snake_body, rocks_list)
    elif fruit_position[0] > window_x - 21:
        fruit_position = gen_fruit(snake_body, rocks_list)
    elif fruit_position[1] > window_y - 21:
        fruit_position = gen_fruit(snake_body, rocks_list)
    return fruit_position

#function that generates a new fruit spawn
def gen_fruit_coop(snake_body, snake2_body, rocks_list):
    #generate a random position for the fruit within the range of the screen
    fruit_position = [random.randrange(0, (window_x // 10)) * 10, random.randrange(0, (window_y // 10)) * 10]

    #check if newly spanwed fruit spawned inside a rock
    for rock in rocks_list:
        if fruit_position[0] == rock[0] and fruit_position[1] == rock[1]:
            fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
    
    #loop thru snake1 (prevent fruit spawning inside body or on same row/column)
    for entry in snake_body:
        if fruit_position[0] == entry[0]:
            fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
        elif fruit_position[1] == entry[1]:
            fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)

    #loop thru snake2 (prevent fruit spawning inside body or on same row/column)
    for entry in snake2_body:
        if fruit_position[0] == entry[0]:
            fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
        elif fruit_position[1] == entry[1]:
            fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)

    #for quality of life we avoid spawning fruit in the outer ring (is this too nice?)
    if fruit_position[0] < 21:
        fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
    elif fruit_position[1] < 21:
        fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
    elif fruit_position[0] > window_x - 21:
        fruit_position = gen_fruit_coop(snake_body, snake_body, rocks_list)
    elif fruit_position[1] > window_y - 21:
        fruit_position = gen_fruit_coop(snake_body, snake2_body, rocks_list)
    return fruit_position

#this function spawns some obstacles at the start of the round
#it is functionally identical to the fruit spawning thing
def gen_rocks(rocks_list, snake_body, fruit_position):
    #generate a spot
    rock_position = [random.randrange(0, (window_x // 10)) * 10, random.randrange(0, (window_y // 10)) * 10]

    #check if the rock spawned inside a fruit and reroll if so
    if rock_position [0] == fruit_position[0] and rock_position[1] == fruit_position [1]:
        rock_position = gen_rocks(rocks_list, snake_body, fruit_position)

    #loop thru snake (prevent rocks spawning inside body or on same row/column)
    for entry in snake_body:
        if rock_position[0] == entry[0]:
            rock_position = gen_rocks(rocks_list, snake_body, fruit_position)
        elif rock_position[1] == entry[1]:
            rock_position = gen_rocks(rocks_list, snake_body, fruit_position)

    #prevent rocks spawning on the same spot
    for entry in rocks_list:
        if rock_position[0] == entry[0] and rock_position[1] == entry[1]:
            rock_position = gen_rocks(rocks_list, snake_body, fruit_position)
    return rock_position

#this function spawns some obstacles at the start of the round
#it is functionally identical to the fruit spawning thing
def gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position):
    #generate a spot
    rock_position = [random.randrange(0, (window_x // 10)) * 10, random.randrange(0, (window_y // 10)) * 10]

    #check if the rock spawned inside a fruit and reroll if so
    if rock_position [0] == fruit_position[0] and rock_position[1] == fruit_position [1]:
        rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)

    #loop thru snake (prevent rocks spawning inside body or on same row/column)
    for entry in snake_body:
        if rock_position[0] == entry[0]:
            rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)
        elif rock_position[1] == entry[1]:
            rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)

    #loop thru snake2 (and mandate having to do inputs to get to next fruit)
    for entry in snake2_body:
        if rock_position[0] == entry[0]:
            rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)
        elif rock_position[1] == entry[1]:
            rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)

    #prevent rocks spawning on the same spot
    for entry in rocks_list:
        if rock_position[0] == entry[0] and rock_position[1] == entry[1]:
            rock_position = gen_rocks_coop(rocks_list, snake_body, snake2_body, fruit_position)
    return rock_position

#this initiates the main menu to start the game out of
#and parses standard values into the menu which can be changed in options
#also initiates the high score at 0
start_menu("Comic Sans MS", "Easy", green, False, 0, False, True)