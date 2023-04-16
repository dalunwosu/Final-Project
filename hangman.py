import requests
import pygame
import os
import sys
import json
import random
from leaderboard import get_top_players, update_leaderboard





pygame.init()
pygame.display.set_caption('Hangman')
winHeight = 800
winWidth = 1000
win = pygame.display.set_mode((winWidth, winHeight))
# ---------------------------------------#
# initialize global variables/constants #
# ---------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
GRAY = (128,128,128)


btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load(
    'hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

limbs = 0

font = pygame.font.SysFont("pressstart2pregular", 30)

def redraw_game_win():
    global score
    global guessed
    global hangmanPics
    global limbs
    global username
    win.fill(WHITE)
    # Buttons
    if username == "":
        username = 'guest' 

    username_text = font.render(f"Username: {username}", True, BLACK)
    username_rect = username_text.get_rect(center=(500,550))
    win.blit(username_text, username_rect)
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(
                win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2),
                     buttons[i][2] - (label.get_height() / 2)))

    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(500,650))        
    win.blit(score_text,score_rect)
    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]

    win.blit(label1, (winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()





def randomWord():
    word_response = requests.get(
        'https://random-word-api.vercel.app/api?words=1')
    word = word_response.json()
    word = "".join(word)
    print(word)
    return word


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

score = 0
counter = 0
lose = True
def end(winner=False):
    global font
    global limbs
    global score
    global username
    global lose
    lostTxt = 'You Lost'
    winTxt = 'WINNER! press any key to play again...'
    redraw_game_win()
    pygame.time.delay(1000)
    win.fill(WHITE)

    if winner == True:
        font = pygame.font.SysFont("pressstart2pregular", 25)
        label = font.render(winTxt, 1, BLACK)
        score +=1 
    else:
        lose = True
        label = font.render(lostTxt, 1, BLACK)
        win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
        pygame.display.update()
        pygame.time.delay(4000) # wait for 2 seconds
        if lose is True:
            pygame.quit()
            print(username)
            with open('leaderboard.json', 'r') as f:
                leaderboard_data = json.load(f)

            score_dict = {'name': username, 'score': score}
            leaderboard_data.append(score_dict)
            with open('leaderboard.json', 'w') as f:
                json.dump(leaderboard_data, f)

    wordTxt = font.render(word.upper(), 1, BLACK)
    wordWas = font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    leaderboard_data = []
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(username)
                with open('leaderboard.json', 'r') as f:
                    leaderboard_data = json.load(f)

                score_dict = {'name': username, 'score': score}
                leaderboard_data.append(score_dict)
                with open('leaderboard.json', 'w') as f:
                    json.dump(leaderboard_data, f)

            if event.type == pygame.KEYDOWN:
                again = False
    reset()

def draw_leaderboard():
    global inMenu
    while inMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inMenu = False
                inPlay = False
        win.fill(WHITE)
        font = pygame.font.SysFont("pressstart2pregular", 30)
        leaderboard_text = font.render("LEADERBOARD", True, BLACK)
        win.blit(leaderboard_text, (250, 50))

        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)

        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

        for i, entry in enumerate(leaderboard):
            name = entry["name"]
            score = entry["score"]
            entry_text = f"{i+1}. {name}: {score}"
            entry_render = font.render(entry_text, True, BLACK)
            win.blit(entry_render, (250, 100 + i*60))

        pygame.display.update()




def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

# MAINLINE


# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([WHITE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])



word = randomWord()
inPlay = True



def game():
    global inMenu
    global limbs
    while inMenu:
        redraw_game_win()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inMenu = False
                pygame.quit()
                print(username)
                with open('leaderboard.json', 'r') as f:
                    leaderboard_data = json.load(f)

                score_dict = {'name': username, 'score': score}
                leaderboard_data.append(score_dict)
                with open('leaderboard.json', 'w') as f:
                    json.dump(leaderboard_data, f)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inMenu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(chr(letter)):
                        if limbs != 5:
                            limbs += 1
                        else:
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)
                            

# def display_riddle():
#     # Initialize Pygame
#     pygame.init()

#     # Set up the window
#     window_size = (800, 600)
#     window = pygame.display.set_mode(window_size)
#     pygame.display.set_caption("Riddle Game")

#     # Set up the fonts
#     question_font = pygame.font.Font(None, 40)
#     option_font = pygame.font.Font(None, 30)

#     # Get a random riddle from the API
#     riddle_response = requests.get('https://riddles-api.vercel.app/random')
#     riddle = riddle_response.json()

#     question = riddle['riddle']
#     answer = riddle['answer']

#     # Set up the four options
#     options = [answer]
#     while len(options) < 4:
#         # Send a GET request to the API endpoint to get a random riddle
#         response = requests.get("https://riddles-api.vercel.app/random")

#         # Get the JSON response
#         riddle = response.json()

#         # Extract the wrong answer from the JSON response
#         wrong_answer = riddle['answer']

#         # Check if the wrong answer is the same as the correct answer
#         if wrong_answer != answer:
#             options.append(wrong_answer)

#     # Shuffle the options
#     random.shuffle(options)

#     # Set up the option rectangles and positions
#     option_rects = {}
#     option_positions = [
#         (200, 300),
#         (500, 300),
#         (200, 400),
#         (500, 400)
#     ]
#     for i, option in enumerate(options):
#         option_text = f"{chr(65+i)}. {option}"
#         option_surf = option_font.render(option_text, True, (0, 0, 0))
#         option_rect = option_surf.get_rect(center=option_positions[i])
#         option_rects[chr(65+i)] = option_rect

#     # Set up the question text and rectangle
#     question_surf = question_font.render(question, True, (0, 0, 0))
#     question_rect = question_surf.get_rect(center=(400, 200))

#     # Set up the result text and rectangle
#     result_font = pygame.font.Font(None, 30)
#     result_surf = None
#     result_rect = None

#     # Start the game loop
#     running = True
#     while running:
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 # Check if an option was clicked
#                 pos = pygame.mouse.get_pos()
#                 for key, rect in option_rects.items():
#                     if rect.collidepoint(pos):
#                         # Check if the clicked option is the correct answer
#                         if key == answer:
#                             result_text = "Correct!"
#                             result_color = (0, 255, 0)

#                         else:
#                             result_text = f"Incorrect. The correct answer is {answer}."
#                             result_color = (255, 0, 0)
#                             running = False

#                         # Render the result as a text surface
#                         result_surf = result_font.render(result_text, True, result_color)
#                         result_rect = result_surf.get_rect(center=(400, 500))

#         # Clear the screen
#         window.fill((255, 255, 255))

#         # Draw the question and options
#         window.blit(question_surf, question_rect)
#         for option_rect in option_rects.values():
#             pygame.draw.rect(window, (255, 255, 255), option_rect)
#             pygame.draw.rect(window, (0, 0, 0), option_rect, 2)

#         # Draw the options text
#         for key, option_text in option_text.items():
#             window.blit(option_text, option_rects[key].move(10, 10))

#         # Draw the result text if any
#         if result_surf:
#             window.blit(result_surf, result_rect)

#         # Update the screen
#         pygame.display.update()






# Initialize global variable
username = ""

inMenu = True

def start_menu():
    global username
    global active
    global inPlay
    global font
    global inMenu
    active = True
    title = font.render("Hangman", True, (255, 255, 255))
    start_text = font.render("Start Game", True, (255, 255, 255))
    leaderboard_text = font.render("Leaderboard", True, (255, 255, 255))

    win.blit(title, (winWidth/2, 100))
    start_rect = start_text.get_rect(center=(winWidth/2, winHeight/2))
    leaderboard_rect = leaderboard_text.get_rect(
        center=(winWidth/2, winHeight/2 + 100))
        
    # Display username input
    font = pygame.font.SysFont("pressstart2pregular", 30)
    username_input = pygame.Rect(winWidth/2 - 100, winHeight/2 - 120, 200, 50)
    username = ""
    # Clear the screen
    win.fill((0, 0, 0))

    # Draw the start menu options
    win.blit(start_text, start_rect)
    win.blit(leaderboard_text, leaderboard_rect)

    # Update the display
    pygame.display.update()

    while inMenu:
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inMenu = False
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inMenu = False
                    inPlay = False
                elif event.key == pygame.K_RETURN and username != "":
                    # Start game with the entered username
                    inMenu = False
                    inPlay = True
                # Handle username input
                elif active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():  # Only add letters to username
                    username_input.width = max(200, font.size(username)[0] + 20)

    # Draw username input box and text
        pygame.draw.rect(win, (255, 255, 255), username_input, 2)
        win.fill((0, 0, 0), (username_input.x + 3, username_input.y + 3, username_input.width - 6, username_input.height - 6))
        username_text = font.render(username, True, (255, 255, 255))
        win.blit(username_text, (username_input.x + 5, username_input.y + 5))

        pygame.display.update()

        # Check if start game or leaderboard is clicked
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            start_text = font.render("Start Game", True, (0, 0, 0))
            pygame.draw.rect(win, (255, 255, 255), start_rect)
            win.blit(start_text, start_rect)
            if pygame.mouse.get_pressed()[0] == 1:
                game()
        else:
            pygame.draw.rect(win, (BLACK), start_rect)
            start_text = font.render("Start Game", True, (255, 255, 255))
            win.blit(start_text, start_rect)

        if leaderboard_rect.collidepoint(pygame.mouse.get_pos()):
            leaderboard_text = font.render("Leaderboard", True, (0, 0, 0))
            pygame.draw.rect(win, (255, 255, 255), leaderboard_rect)
            win.blit(leaderboard_text, leaderboard_rect)
            if pygame.mouse.get_pressed()[0] == 1:
                draw_leaderboard()
        else:
            pygame.draw.rect(win, (BLACK), leaderboard_rect)
            leaderboard_text = font.render("Leaderboard", True, (255, 255, 255))
            win.blit(leaderboard_text, leaderboard_rect)

    # Update the display
        pygame.display.update()




start_menu()
# Check if mouse is over start button



    
pygame.quit()
