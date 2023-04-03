import requests
import pygame
import os
import sys
import json
from leaderboard import get_top_players, update_leaderboard


riddle_response = requests.get('https://riddles-api.vercel.app/random')
riddle = riddle_response.json()

question = riddle['riddle']
answer = riddle['answer']


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
def end(winner=False):
    global limbs
    global score
    global username
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER! press any key to play again...'
    redraw_game_win()
    pygame.time.delay(1000)
    win.fill(WHITE)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
        score +=1 
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

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
    win.fill(WHITE)
    font = pygame.font.Font(None, 30)
    leaderboard_text = font.render("LEADERBOARD", True, BLACK)
    win.blit(leaderboard_text, (250, 50))

    with open("leaderboard.json", "r") as f:
        leaderboard = json.load(f)

    for i, entry in enumerate(leaderboard):
        name = entry["name"]
        score = entry["score"]
        entry_text = f"{i+1}. {name}: {score}"
        entry_render = font.render(entry_text, True, BLACK)
        win.blit(entry_render, (250, 100+i))

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

font = pygame.font.Font(None, 50)
title = font.render("Hangman", True, (255, 255, 255))
start_text = font.render("Start Game", True, (255, 255, 255))
leaderboard_text = font.render("Leaderboard", True, (255, 255, 255))
username_text = font.render("Username:", True, (255, 255, 255))

win.blit(title, (winWidth/2 - title.get_width()/2, 100))
start_rect = start_text.get_rect(center=(winWidth/2, winHeight/2))
leaderboard_rect = leaderboard_text.get_rect(
    center=(winWidth/2, winHeight/2 + 100))
username_rect = username_text.get_rect(
    center=(winWidth/2 - 100, winHeight/2 - 100))


username = ""
# Display username input
font = pygame.font.Font(None, 50)
username_input = pygame.Rect(winWidth/2 - 50, winHeight/2 - 120, 100, 50)
username = ""

pygame.display.update()

word = randomWord()
inPlay = True


def game():
    global inPlay
    global limbs
    while inPlay:
        redraw_game_win()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
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


# Initialize global variable
username = ""


def start_menu():
    global username
    global inPlay
    while inMenu:

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

        # Draw username input box and text
        # ...

        # Get user input and update username variable
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                username = username[:-1]
            else:
                username += event.unicode

    return username


# Check if mouse is over start button



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if start game or leaderboard is clicked
            if start_rect.collidepoint(event.pos):
                game()
            elif leaderboard_rect.collidepoint(event.pos):
                draw_leaderboard()
                pygame.display.update()
                
        elif event.type == pygame.KEYDOWN:
            # Check if a key is pressed while the username input box is selected
            if event.key == pygame.K_RETURN and username != "":
                # Start game with the entered username
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if username_input.collidepoint(pygame.mouse.get_pos()):
                    active = True
                else:
                    active = False

            else:
                username += event.unicode

    # Clear the screen
    win.fill((0, 0, 0))

    # Draw the start menu options
    win.blit(start_text, start_rect)
    win.blit(leaderboard_text, leaderboard_rect)

    # Draw the username input box
    pygame.draw.rect(win, (255, 255, 255), username_input, 2)
    username_text = font.render(username, True, (255, 255, 255))
    win.blit(username_text, (username_input.x + 5, username_input.y + 5))

    # Update the display
    pygame.display.update()
pygame.quit()
