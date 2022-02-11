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
    global DISPLAYSURF, FPSCLOCK, mouseClicked, mX, mY, gameState, mainCharList, candidate, stafferA, stafferB
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

    #Players Team
    candidate = 'none'
    stafferA = 'none'
    stafferB = 'none'

    #Primary Game Loop
    while True:
        if gameState == 'title':
            gameState = titleScene()
        elif gameState == 'character select':
            changes = charScene()
            gameState = changes[0]
            candidate = changes[1]
        elif gameState == 'draft':
            changes = draftScene()
            gameState = changes[0]
            stafferA = changes[1]
            stafferB = changes[2]
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

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    cbuttonList = []
    newState = 'character select'
    #Character Selection
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Character Select', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 50)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    itr = 0
    x = 400
    y = 140

    CHARABUTTON = [(x-120,y), (100, 100), 'charA']
    CHARBBUTTON = [(x, y), (100, 100), 'charB']
    CHARCBUTTON = [(x+120, y), (100, 100), 'charC']


    selection = candidate
    selectionFrame = [(400, 350), (100,100), ' ']

    createButton(BUTTONFONT, 'Char A', BLACK, LRED, CHARABUTTON[0], CHARABUTTON[1])
    cbuttonList.append(CHARABUTTON)

    createButton(BUTTONFONT, 'Char B', BLACK, LRED, CHARBBUTTON[0], CHARBBUTTON[1])
    cbuttonList.append(CHARBBUTTON)

    createButton(BUTTONFONT, 'Char C', BLACK, LRED, CHARCBUTTON[0], CHARCBUTTON[1])
    cbuttonList.append(CHARCBUTTON)


    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'draft']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])

    #Place holder variable to prevent selection frame from changing with clicks not relevant
    holder = 'none'


    if mouseClicked == True:
        for button in cbuttonList:
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                selection = holder
                

        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops' and candidate != 'none':
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
    return newState, selection


def draftScene():

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    cbuttonList1 = []
    cbuttonList2 = []
    newState = 'draft'
    #Staff Selection
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Staffer Selection', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 50)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    itr = 0
    x = 400
    y1 = 140
    y2 = 260

    STAFFABUTTON = [(x-120,y1), (100, 100), 'staffA']
    STAFFBBUTTON = [(x, y1), (100, 100), 'staffB']
    STAFFCBUTTON = [(x+120, y1), (100, 100), 'staffC']

    STAFFDBUTTON = [(x-120,y2), (100, 100), 'staffD']
    STAFFEBUTTON = [(x,y2), (100, 100), 'staffE']
    STAFFFBUTTON = [(x+120,y2), (100, 100), 'staffF']


    selection = candidate
    staff1 = stafferA
    staff2 = stafferB
    selectionFrame = [(x-120, 380), (100,100), ' ']
    staffFrame1 = [(x, 380), (100,100), ' ']
    staffFrame2 = [(x+120, 380), (100, 100),' ']

    createButton(BUTTONFONT, 'Staff A', BLACK, LRED, STAFFABUTTON[0], STAFFABUTTON[1])
    cbuttonList1.append(STAFFABUTTON)

    createButton(BUTTONFONT, 'Staff B', BLACK, LRED, STAFFBBUTTON[0], STAFFBBUTTON[1])
    cbuttonList1.append(STAFFBBUTTON)

    createButton(BUTTONFONT, 'Staff C', BLACK, LRED, STAFFCBUTTON[0], STAFFCBUTTON[1])
    cbuttonList1.append(STAFFCBUTTON)

    createButton(BUTTONFONT, 'Staff D', BLACK, LRED, STAFFDBUTTON[0], STAFFDBUTTON[1])
    cbuttonList2.append(STAFFDBUTTON)

    createButton(BUTTONFONT, 'Staff E', BLACK, LRED, STAFFEBUTTON[0], STAFFEBUTTON[1])
    cbuttonList2.append(STAFFEBUTTON)

    createButton(BUTTONFONT, 'Staff F', BLACK, LRED, STAFFFBUTTON[0], STAFFFBUTTON[1])
    cbuttonList2.append(STAFFFBUTTON)


    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'team']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])

    #Place holder variable to prevent selection frame from changing with clicks not relevant
    holder = 'none'

    if mouseClicked == True:
        for button in cbuttonList1:
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                staff1 = holder
                break
        
        for button in cbuttonList2:
            print("This is running")
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                staff2 = holder
                break

        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops':
            pass
        else: newState = 'draft'

    if selection == 'charA':
        selectionFrame[2]= 'Char A'
    elif selection == 'charB':
        selectionFrame[2]= 'Char B'
    elif selection == 'charC':
        selectionFrame[2]= 'Char C'

    if staff1 == 'staffA':
        staffFrame1[2]= 'Staff A'
    elif staff1 == 'staffB':
        staffFrame1[2]= 'Staff B'
    elif staff1 == 'staffC':
        staffFrame1[2]= 'Staff C'
    
    if staff2 == 'staffD':
        staffFrame2[2]= 'Staff D'
    elif staff2 == 'staffE':
        staffFrame2[2]= 'Staff E'
    elif staff2 == 'staffF':
        staffFrame2[2]= 'Staff F'

    createButton(BUTTONFONT, selectionFrame[2], BLACK, LRED, selectionFrame[0], selectionFrame[1])
    createButton(BUTTONFONT, staffFrame1[2], BLACK, LRED, staffFrame1[0], staffFrame1[1])
    createButton(BUTTONFONT, staffFrame2[2], BLACK, LRED, staffFrame2[0], staffFrame2[1])

    main.mouseClicked = False
    return newState, staff1, staff2

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