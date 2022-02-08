import pygame, sys
from pygame.locals import *
from character import Character

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600

#       R   G  B
BLACK = (0, 0, 0)
LRED = (255, 50, 50)
DRED = (255, 0, 0)





def main():
    global DISPLAYSURF, FPSCLOCK, mouseClicked, mX, mY, gameState, mainCharList
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Demagogues & Democracy')
    FPSCLOCK = pygame.time.Clock()

    #stores mouse event coord
    mX = 0
    mY = 0
    mouseClicked = False

    #Main Character Values
    mainCharList = [(5,3,7), (5,5,5), (2, 3, 10)]

    #scene switching variable
    gameState = 'title'
    #Primary Game Loop
    while True:
        if gameState == 'title':
            gameState = titleScene()
        elif gameState == 'character select':
            charScene()
        elif gameState == 'draft':
            draftScene()
        elif gameState == 'team':
            teamScene()
        elif gameState == 'area':
            areaScene()
        elif gameState == 'combat':
            combatScene()
        elif gameState == 'end of week':
            weekScene()
        elif gameState == 'end':
            endScene()
        else:
            errorScene()
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mX, mY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mX, mY = event.pos
                mouseClicked = True

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def createButton(font, text, textColor, buttonColor, center, whRect):
    buttonText = font.render(text, True, textColor)
    buttonRectObj = buttonText.get_rect()
    buttonRectObj.center = center
    cX = center[0]
    cY = center[1]
    tlX = cX - (whRect[0]/2)
    tlY = cY - (whRect[1]/2)
    pygame.draw.rect(DISPLAYSURF, buttonColor,(tlX, tlY, whRect[0], whRect[1]))
    DISPLAYSURF.blit(buttonText, buttonRectObj)

def topLeft(button):
    cX = button[0][0]
    cY = button[0][1]
    width = button[1][0]
    height = button[1][1]
    tlX = cX - (width/2)
    tlY = cY - (height/2)
    return (tlX, tlY)

def clickCheck(button, mX, mY):
    tL = topLeft(button)
    leftBound = tL[0]
    rightBound = leftBound+button[1][0]
    upBound = tL[1]
    botBound = upBound+button[1][1]

    if mX >= leftBound and mX <= rightBound:
        if mY >= upBound and mY <= botBound:
            str = button[2]
            return str
        else:
            return 'oops'
    else:
        return 'oops'



def titleScene():
    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    buttonList = []
    newState = 'title'
    #Title
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Demagogues & Democracy', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 150)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    #Start Game Button
    STARTBUTTON = [(400,290), (240,80), 'character select']
    createButton(BUTTONFONT, 'Start New Game', BLACK, LRED, STARTBUTTON[0], STARTBUTTON[1])
    buttonList.append(STARTBUTTON)

    #Continue Button, NOT YET FUNCTIONAL
    CONTINUEBUTTON = [(400,380), (240, 80), 'title']
    createButton(BUTTONFONT, "Continue", BLACK, LRED, CONTINUEBUTTON[0], CONTINUEBUTTON[1])
    buttonList.append(CONTINUEBUTTON)

    if mouseClicked == True:
        for button in buttonList:
            newState = clickCheck(button, mX, mY)
            if newState != 'oops':
                break
            else:
                newState = 'title'
            print(newState)
    return newState
        
    


def charScene():
    global mainCharacter

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    cbuttonList = []
    newState = 'character select'
    #Character Selection
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Character Select', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 150)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    mainCharacter = []
    itr = 0
    x = WINWIDTH/3
    y = 240

    CHARABUTTON = [(x,y), (100, 100), 'charA']
    CHARBBUTTON = [(x+120, y), (100, 100), 'charB']
    CHARCBUTTON = [(x+240, y), (100, 100), 'charC']


    selection = 'none'
    selectionFrame = [(400, 350), (100,100), ' ']

    createButton(BUTTONFONT, 'Char A', BLACK, LRED, CHARABUTTON[0], CHARABUTTON[1])
    cbuttonList.append(CHARABUTTON)

    createButton(BUTTONFONT, 'Char B', BLACK, LRED, CHARBBUTTON[0], CHARBBUTTON[1])
    cbuttonList.append(CHARABUTTON)

    createButton(BUTTONFONT, 'Char C', BLACK, LRED, CHARCBUTTON[0], CHARCBUTTON[1])
    cbuttonList.append(CHARABUTTON)


    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'draft']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])

    if mouseClicked == True:
        for button in cbuttonList:
            selection = clickCheck(button, mX, mY)
            if selection != 'oops':
                break
            else:
                selection = 'none'
        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops':
            pass
        else: newState = 'character select'

    if selection == 'charA':
        selectionFrame[2]= 'Char A'
    elif selection == 'charB':
        selectionFrame[2]= 'Char B'
    elif selection == 'charC':
        selectionFrame[2]= 'Char C'

    createButton(BUTTONFONT, selectionFrame[2], BLACK, LRED, selectionFrame[0], selectionFrame[1])

    main.mouseClicked = False
    return newState


def draftScene():
    a = 0

def teamScene():
    a = 0

def areaScene():
    a = 0

def combatScene():
    a = 0

def weekScene():
    a = 0

def endScene():
    a = 0

def errorScene():
    a = 0

if __name__ == '__main__':
    main()