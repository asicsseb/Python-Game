import pygame, sys
from pygame.locals import *
from character import Character

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600

#       R   G  B
BLACK = (0, 0, 0)
LRED = (255, 50, 50)
LGREEN = (50, 255, 50)
LBLUE = (50, 50, 255)
DRED = (255, 0, 0)





def main():
    global DISPLAYSURF, FPSCLOCK, mouseClicked, mX, mY, gameState, mainCharList, stafferList, weeks, candidate, stafferA, stafferB, team, support, batArea, batAction, enemyTeam, combatComplete, playerScore, enemyScore
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Demagogues & Democracy')
    FPSCLOCK = pygame.time.Clock()

    #stores mouse event coord
    mX = 0
    mY = 0
    mouseClicked = False

    #Character Values
    mainCharList = [['Matt', 6, 4, 2, 1], ['Arnie', 8, 2, 1, 3], ['Jed', 7, 3, 2, 2]]
    stafferList = [['Toby', 7, 2, 2, 2], ['Josh', 5, 4, 1, 1], ['Sam', 5, 2, 1, 3], ['C.J.', 5, 1, 1, 4], ['Donna', 6, 3, 1, 2], ['Kate', 9, 1, 1, 1]] + mainCharList

    #scene switching variable
    gameState = 'title'

    #Players Team
    candidate = 'none'
    stafferA = 'none'
    stafferB = 'none'

    team = []

    #temporary name while I work out object functionality
    tempTeam = []
    playerTeam = []
    teamBuilt = False

    #Enemy Team
    enemyStats = [('b1', 10, 2, 2, 1), ('b2', 6, 2, 1, 2), ('b3', 5, 1, 1, 3)]
    enemyTeam = []
    populateTeam(enemyStats, enemyTeam)

    #Location of Campaign
    campLoc = 'Harrisburg'

    #State of the race
    support = 5

    #Weeks left in campaign
    weeks = 10

    #Combat Prep Info
    batArea = 'none'
    batAction = 'none'
    combatComplete = False
    playerScore = 0
    enemyScore = 0


    #Primary Game Loop
    while True:

        DISPLAYSURF.fill(BLACK)
        if gameState == 'title':
            gameState = titleScene()
        elif gameState == 'continue':
            gameState = continueScene()
        elif gameState == 'character select':
            changes = charScene()
            gameState = changes[0]
            candidate = changes[1]
        elif gameState == 'draft':
            changes = draftScene()
            gameState = changes[0]
            stafferA = changes[1]
            stafferB = changes[2]
            team = [candidate, stafferA, stafferB]



        elif gameState == 'team':
            if teamBuilt == False:
                itr = 0
                for c in team:
                    if c != 'none':
                        pH = searchFunction(stafferList, c)
                        if tempTeam == []:
                            tempTeam.append(pH)
                        else:
                            if pH in tempTeam:
                                    pass
                            else:
                                tempTeam.append(pH)

                populateTeam(tempTeam, playerTeam)

            teamBuilt = True
            #Resets Values for Combat
            combatComplete = False
            playerScore = 0
            enemyScore = 0
            changes = teamScene(campLoc, support, weeks, playerTeam)
            gameState = changes[0]
            tempTeam = changes[1]
        elif gameState == 'area':
            changes = areaScene()
            gameState = changes[0]
            batArea = changes[1]
            batAction = changes[2]
        elif gameState == 'combat':
            changes = combatScene(batArea, batAction, playerTeam, enemyTeam, playerScore, enemyScore)
            playerScore = changes[1]
            enemyScore = changes[2]
            support = changes[3]
            weeks = changes[4]
            combatComplete = True
            gameState = changes[0]
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

def populateTeam(listStats, emptyList):
    for a in listStats:
        createCharacter = Character(a[0], a[1], a[2], a[3], a[4])
        emptyList.append(createCharacter)

#traverses list of characters, and returns stats of character as tuple
def searchFunction(list, str):
    for a in list:
        if a[0] == str:
            return a


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

#Returns a string within a button if the button is clicked
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

#Returns True or False for if a button in a list is clicked
def clickCheckB(button, mX, mY):
    tL = topLeft(button)
    leftBound = tL[0]
    rightBound = leftBound+button[1][0]
    upBound = tL[1]
    botBound = upBound+button[1][1]

    if mX >= leftBound and mX <= rightBound:
        if mY >= upBound and mY <= botBound:
            return True
        else:
            return False
    else:
        return False

#Switches positions of elements in list
def orderSwap(teamList, a, b):
    holdA = teamList[a]
    holdB = teamList[b]
    teamList[a] = holdB
    teamList[b] = holdA

    return teamList

def combatLoop(playerObj, enemyObj, eScore, pScore, i):
    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)

    #Player Team Icon
    playerX = 110
    playerY = 300
    playerDirection = 'right'
    playerHealth = playerObj.health
    playerInt = playerObj.int

    #Enemy Team Icon
    enemyX = 670
    enemyY = 300
    enemyHealth = enemyObj.health
    enemyInt = enemyObj.int

    #internal player score
    pScoreText = f"Player Score: {pScore}"
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    playerTextObj = infoFont.render(pScoreText, True, LRED)
    playerRectObj = playerTextObj.get_rect()
    playerRectObj.topleft = (100,100)

    #internal enemy score
    eScoreText = f"Enemy Score: {eScore}"
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    enemyTextObj = infoFont.render(eScoreText, True, LRED)
    enemyRectObj = enemyTextObj.get_rect()
    enemyRectObj.topleft = (500,100)

    #Round info
    round = i+1
    roundText = f"Round {round}"
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    roundTextObj = infoFont.render(roundText, True, LRED)
    roundRectObj = roundTextObj.get_rect()
    roundRectObj.topleft = (350, 200)

    #matchup info
    matchupText = f"{playerObj.name} vs. {enemyObj.name}"
    matchupTextObj = infoFont.render(matchupText, True, LRED)
    matchupRectObj = matchupTextObj.get_rect()
    matchupRectObj.center = (400, 250)


    while True: 
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(playerTextObj, playerRectObj)
        DISPLAYSURF.blit(enemyTextObj, enemyRectObj)
        DISPLAYSURF.blit(roundTextObj, roundRectObj)
        DISPLAYSURF.blit(matchupTextObj, matchupRectObj)
        PLAYER = [(playerX, playerY), (100, 100), '']
        ENEMY = [(enemyX, enemyY), (100, 100), '']

        healthStr = str(playerHealth)
        enemyStr = str(enemyHealth)


        if playerDirection == 'right':
            if playerHealth > 0 and enemyHealth > 0:
                playerX += 5
                enemyX -= 5
                if playerX == 340:
                    playerHealth -= enemyInt
                    enemyHealth -= playerInt
                    if playerHealth > 0 and enemyHealth > 0:
                        playerDirection = 'left'
        elif playerDirection == 'left':
            playerX -= 5
            enemyX += 5
            if playerX == 110:
                playerDirection = 'right'
    

        if playerHealth > 0:
            createButton(BUTTONFONT, healthStr, BLACK, LRED, PLAYER[0], PLAYER[1])
        else:
            break

        if enemyHealth > 0:
            createButton(BUTTONFONT, enemyStr, BLACK, LGREEN, ENEMY[0], ENEMY[1])
        else:
            break


        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
    if playerHealth > 0 and enemyHealth < 1:
        return 'player'
    elif playerHealth < 1 and enemyHealth > 0:
        return 'enemy'
    elif playerHealth < 1 and enemyHealth < 1:
        return 'tie'

def resultsCalc(area, action, pScore, eScore):
    supportChange = 0
    if area == 'areaA' and action == 'actionA':
        if pScore > eScore:
            supportChange += 1
        elif eScore > pScore:
            supportChange -= 1
    elif area == 'areaA' and action == 'actionB':
        if pScore > eScore:
            supportChange += 2
        elif eScore > pScore:
            supportChange -= 2
    elif area == 'areaA' and action == 'actionC':
        if pScore > eScore:
            supportChange += 3
        elif eScore > pScore:
            supportChange -= 3
    elif area == 'areaB' and action == 'actionA':
        if pScore > eScore:
            supportChange += .5
        elif eScore > pScore:
            supportChange -= .5
    elif area == 'areaB' and action == 'actionB':
        if pScore > eScore:
            supportChange += 1.5
        elif eScore > pScore:
            supportChange -= 1.5
    elif area == 'areaB' and action == 'actionC':
        if pScore > eScore:
            supportChange += 2.5
        elif eScore > pScore:
            supportChange -= 2.5
    elif area == 'areaC' and action == 'actionA':
        if pScore > eScore:
            supportChange += 2
        elif eScore > pScore:
            supportChange -= 2
    elif area == 'areaC' and action == 'actionB':
        if pScore > eScore:
            supportChange += 3
        elif eScore > pScore:
            supportChange -= 3
    elif area == 'areaC' and action == 'actionC':
        if pScore > eScore:
            supportChange += 4
        elif eScore > pScore:
            supportChange -= 4
    
    return supportChange

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
    CONTINUEBUTTON = [(400,380), (240, 80), 'continue']
    createButton(BUTTONFONT, "Continue", BLACK, LRED, CONTINUEBUTTON[0], CONTINUEBUTTON[1])
    buttonList.append(CONTINUEBUTTON)

    if mouseClicked == True:
        for button in buttonList:
            newState = clickCheck(button, mX, mY)
            if newState != 'oops':
                break
            else:
                newState = 'title'
    return newState

def continueScene():
    newState = 'continue'
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    textSurfaceObj = fontObj.render('This has not yet been implemented.', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 150)

    textSurfaceObj2 = fontObj.render('Click anywhere to return to title screen.', True, LRED)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (400, 250)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

    if mouseClicked == True:
        newState = 'title'
    
    return newState

def charScene():

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    cbuttonList = []
    newState = 'character select'
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    #Character Selection
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Character Select', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 50)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    x = 400
    y = 140

    CHARABUTTON = [(x-120,y), (100, 100), 'Matt']
    CHARBBUTTON = [(x, y), (100, 100), 'Arnie']
    CHARCBUTTON = [(x+120, y), (100, 100), 'Jed']


    selection = candidate
    selectionFrame = [(400, 350), (100,100), ' ']

    createButton(BUTTONFONT, mainCharList[0][0], BLACK, LRED, CHARABUTTON[0], CHARABUTTON[1])
    cbuttonList.append(CHARABUTTON)

    createButton(BUTTONFONT, mainCharList[1][0], BLACK, LRED, CHARBBUTTON[0], CHARBBUTTON[1])
    cbuttonList.append(CHARBBUTTON)

    createButton(BUTTONFONT, mainCharList[2][0], BLACK, LRED, CHARCBUTTON[0], CHARCBUTTON[1])
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

    if selection == 'Matt':
        selectionFrame[2]= mainCharList[0][0]
        #Health
        healthTextObj = infoFont.render(f'Health: {mainCharList[0][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (200, 220)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {mainCharList[0][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (200, 270)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {mainCharList[0][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (200, 320)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {mainCharList[0][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (200, 370)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)

    elif selection == 'Arnie':
        selectionFrame[2]= mainCharList[1][0]
        #Health
        healthTextObj = infoFont.render(f'Health: {mainCharList[1][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (200, 220)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {mainCharList[1][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (200, 270)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {mainCharList[1][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (200, 320)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {mainCharList[1][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (200, 370)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)        

    elif selection == 'Jed':
        selectionFrame[2]= mainCharList[2][0]
        #Health
        healthTextObj = infoFont.render(f'Health: {mainCharList[2][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (200, 220)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {mainCharList[2][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (200, 270)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {mainCharList[2][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (200, 320)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {mainCharList[2][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (200, 370)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)        

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

    x = 400
    y1 = 140
    y2 = 260

    STAFFABUTTON = [(x-120,y1), (100, 100), 'Toby']
    STAFFBBUTTON = [(x, y1), (100, 100), 'Josh']
    STAFFCBUTTON = [(x+120, y1), (100, 100), 'Sam']

    STAFFDBUTTON = [(x-120,y2), (100, 100), 'C.J.']
    STAFFEBUTTON = [(x,y2), (100, 100), 'Donna']
    STAFFFBUTTON = [(x+120,y2), (100, 100), 'Kate']



    staff1 = stafferA
    staff2 = stafferB

    staffFrame1 = [(x-80, 380), (100,100), ' ']
    staffFrame2 = [(x+80, 380), (100, 100),' ']

    createButton(BUTTONFONT, 'Toby', BLACK, LRED, STAFFABUTTON[0], STAFFABUTTON[1])
    cbuttonList1.append(STAFFABUTTON)

    createButton(BUTTONFONT, 'Josh', BLACK, LRED, STAFFBBUTTON[0], STAFFBBUTTON[1])
    cbuttonList1.append(STAFFBBUTTON)

    createButton(BUTTONFONT, 'Sam', BLACK, LRED, STAFFCBUTTON[0], STAFFCBUTTON[1])
    cbuttonList1.append(STAFFCBUTTON)

    createButton(BUTTONFONT, 'C.J.', BLACK, LRED, STAFFDBUTTON[0], STAFFDBUTTON[1])
    cbuttonList2.append(STAFFDBUTTON)

    createButton(BUTTONFONT, 'Donna', BLACK, LRED, STAFFEBUTTON[0], STAFFEBUTTON[1])
    cbuttonList2.append(STAFFEBUTTON)

    createButton(BUTTONFONT, 'Kate', BLACK, LRED, STAFFFBUTTON[0], STAFFFBUTTON[1])
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
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                staff2 = holder
                break

        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops' and staff1 != 'none' and staff2 != 'none':
            pass
        else: newState = 'draft'


    infoFont = pygame.font.Font('freesansbold.ttf', 18)
    s1TextObj = infoFont.render('Pick 1 From Each Row', True, LBLUE)
    s1RectObj = s1TextObj.get_rect()
    s1RectObj.topleft = (25, 150)
    DISPLAYSURF.blit(s1TextObj, s1RectObj)

    if staff1 == 'Toby':
        staffFrame1[2]= 'Toby'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[0][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (150, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[0][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (150, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[0][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (150, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[0][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (150, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)
    elif staff1 == 'Josh':
        staffFrame1[2]= 'Josh'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[1][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (150, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[1][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (150, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[1][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (150, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[1][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (150, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)

    elif staff1 == 'Sam':
        staffFrame1[2]= 'Sam'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[2][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (150, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[2][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (150, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[2][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (150, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[2][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (150, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)
    
    if staff2 == 'C.J.':
        staffFrame2[2]= 'C.J.'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[3][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (650, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[3][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (650, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[3][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (650, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[3][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (650, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)

    elif staff2 == 'Donna':
        staffFrame2[2]= 'Donna'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[4][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (650, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[4][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (650, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[4][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (650, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[4][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (650, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)

    elif staff2 == 'Kate':
        staffFrame2[2]= 'Kate'
        #Health
        healthTextObj = infoFont.render(f'Health: {stafferList[5][1]}', True, LBLUE)
        healthRectObj = healthTextObj.get_rect()
        healthRectObj.center = (650, 400)
        DISPLAYSURF.blit(healthTextObj, healthRectObj)
        #INT
        strTextObj = infoFont.render(f'INT: {stafferList[5][2]}', True, LBLUE)
        strRectObj = strTextObj.get_rect()
        strRectObj.center = (650, 440)
        DISPLAYSURF.blit(strTextObj, strRectObj)
        #CHA
        chaTextObj = infoFont.render(f'CHA: {stafferList[5][3]}', True, LBLUE)
        chaRectObj = chaTextObj.get_rect()
        chaRectObj.center = (650, 480)
        DISPLAYSURF.blit(chaTextObj, chaRectObj)    
        #FORT
        fortTextObj = infoFont.render(f'INT: {stafferList[5][4]}', True, LBLUE)
        fortRectObj = fortTextObj.get_rect()
        fortRectObj.center = (650, 520)
        DISPLAYSURF.blit(fortTextObj, fortRectObj)


    createButton(BUTTONFONT, staffFrame1[2], BLACK, LRED, staffFrame1[0], staffFrame1[1])
    createButton(BUTTONFONT, staffFrame2[2], BLACK, LRED, staffFrame2[0], staffFrame2[1])

    main.mouseClicked = False
    return newState, staff1, staff2

def teamScene(loc, raceDiff, weeks, teamList):
    newState = 'team'
    smallFont = pygame.font.Font('freesansbold.ttf', 12)
    #Staff Selection Title
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Campaign HQ', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 50)
    
    #Location Text
    location = "Location: "+ loc
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    locationTextObj = infoFont.render(location, True, LRED)
    locationRectObj = locationTextObj.get_rect()
    locationRectObj.topleft = (100,100)

    # Percent Support Text
    raceStatus = f"Status of Race: {raceDiff}%"
    supTextObj = infoFont.render(raceStatus, True, LRED)
    supRectObj = supTextObj.get_rect()
    supRectObj.topleft = (100,140)

    # Weeks Left Text
    weeksLeft = f"Weeks Left: {weeks}"
    weeksTextObj = infoFont.render(weeksLeft, True, LRED)
    weeksRectObj = weeksTextObj.get_rect()
    weeksRectObj.topleft = (100,180)

    #Team Slot Frames
    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    x = 400
    y = 300

    teamSpot1 = [(x-200,y), (100, 100), teamList[0].name]
    teamSpot2 = [(x, y), (100, 100), teamList[1].name]
    teamSpot3 = [(x+200, y), (100, 100), teamList[2].name]
    teambuttonList = []

    #spot 1 Info
    s1HealthTextObj = smallFont.render(f'Health: {teamList[0].health}', True, LBLUE)
    s1HealthRectObj = s1HealthTextObj.get_rect()
    s1HealthRectObj.center = (x-200, 370)    

    s1IntTextObj = smallFont.render(f'INT: {teamList[0].int}', True, LBLUE)
    s1IntRectObj = s1IntTextObj.get_rect()
    s1IntRectObj.center = (x-200, 390)

    s1ChaTextObj = smallFont.render(f'CHA: {teamList[0].cha}', True, LBLUE)
    s1ChaRectObj = s1ChaTextObj.get_rect()
    s1ChaRectObj.center = (x-200, 410)

    s1FortTextObj = smallFont.render(f'FORT: {teamList[0].fort}', True, LBLUE)
    s1FortRectObj = s1FortTextObj.get_rect()
    s1FortRectObj.center = (x-200, 430)

    #spot 2 info
    s2HealthTextObj = smallFont.render(f'Health: {teamList[1].health}', True, LBLUE)
    s2HealthRectObj = s2HealthTextObj.get_rect()
    s2HealthRectObj.center = (x, 370)    

    s2IntTextObj = smallFont.render(f'INT: {teamList[1].int}', True, LBLUE)
    s2IntRectObj = s2IntTextObj.get_rect()
    s2IntRectObj.center = (x, 390)

    s2ChaTextObj = smallFont.render(f'CHA: {teamList[1].cha}', True, LBLUE)
    s2ChaRectObj = s2ChaTextObj.get_rect()
    s2ChaRectObj.center = (x, 410)

    s2FortTextObj = smallFont.render(f'FORT: {teamList[1].fort}', True, LBLUE)
    s2FortRectObj = s2FortTextObj.get_rect()
    s2FortRectObj.center = (x, 430)

    #spot 3 info 
    s3HealthTextObj = smallFont.render(f'Health: {teamList[2].health}', True, LBLUE)
    s3HealthRectObj = s3HealthTextObj.get_rect()
    s3HealthRectObj.center = (x+200, 370)    

    s3IntTextObj = smallFont.render(f'INT: {teamList[2].int}', True, LBLUE)
    s3IntRectObj = s3IntTextObj.get_rect()
    s3IntRectObj.center = (x+200, 390)

    s3ChaTextObj = smallFont.render(f'CHA: {teamList[2].cha}', True, LBLUE)
    s3ChaRectObj = s3ChaTextObj.get_rect()
    s3ChaRectObj.center = (x+200, 410)

    s3FortTextObj = smallFont.render(f'FORT: {teamList[2].fort}', True, LBLUE)
    s3FortRectObj = s3FortTextObj.get_rect()
    s3FortRectObj.center = (x+200, 430)    


    leftRightFirst = [(305, y-25), (50,40), 'Swap']
    leftRightSecond = [(505, y-25), (50, 40), 'Swap']

    orderbuttonList = []

    createButton(BUTTONFONT, leftRightFirst[2], BLACK, LRED, leftRightFirst[0], leftRightFirst[1])
    orderbuttonList.append(leftRightFirst)
    
    createButton(BUTTONFONT, leftRightSecond[2], BLACK, LRED, leftRightSecond[0], leftRightSecond[1])
    orderbuttonList.append(leftRightSecond)




    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(locationTextObj, locationRectObj)
    DISPLAYSURF.blit(supTextObj, supRectObj)
    DISPLAYSURF.blit(weeksTextObj, weeksRectObj)

    DISPLAYSURF.blit(s1HealthTextObj, s1HealthRectObj)
    DISPLAYSURF.blit(s1IntTextObj, s1IntRectObj)
    DISPLAYSURF.blit(s1ChaTextObj, s1ChaRectObj)
    DISPLAYSURF.blit(s1FortTextObj, s1FortRectObj)

    DISPLAYSURF.blit(s2HealthTextObj, s2HealthRectObj)
    DISPLAYSURF.blit(s2IntTextObj, s2IntRectObj)
    DISPLAYSURF.blit(s2ChaTextObj, s2ChaRectObj)
    DISPLAYSURF.blit(s2FortTextObj, s2FortRectObj)

    DISPLAYSURF.blit(s3HealthTextObj, s3HealthRectObj)
    DISPLAYSURF.blit(s3IntTextObj, s3IntRectObj)
    DISPLAYSURF.blit(s3ChaTextObj, s3ChaRectObj)
    DISPLAYSURF.blit(s3FortTextObj, s3FortRectObj)

    createButton(BUTTONFONT, teamSpot1[2], BLACK, LRED, teamSpot1[0], teamSpot1[1])
    teambuttonList.append(teamSpot1)

    createButton(BUTTONFONT, teamSpot2[2], BLACK, LRED, teamSpot2[0], teamSpot2[1])
    teambuttonList.append(teamSpot2)

    createButton(BUTTONFONT, teamSpot3[2], BLACK, LRED, teamSpot3[0], teamSpot3[1])
    teambuttonList.append(teamSpot3)

    createButton(BUTTONFONT, leftRightFirst[2], BLACK, LRED, leftRightFirst[0], leftRightFirst[1])
    orderbuttonList.append(leftRightFirst)
    
    createButton(BUTTONFONT, leftRightSecond[2], BLACK, LRED, leftRightSecond[0], leftRightSecond[1])
    orderbuttonList.append(leftRightSecond)

    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'area']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])


    #event handler
    if mouseClicked == True:
        for button in orderbuttonList:
            clickedButton = clickCheckB(button, mX, mY)
            if clickedButton == True:
                if button == leftRightFirst:
                    #logic to move #1 member to #2
                    teamList = orderSwap(teamList, 0, 1)
                    break
                elif button == leftRightSecond:
                    #logic to move #2 member to #3
                    teamList = orderSwap(teamList, 1, 2)
                    break
        
        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops':
            pass
        else: newState = 'team'
    return [newState, teamList]

def areaScene():
    newState = 'area'

    #Staff Selection Title
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Location/Action', True, LRED)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 50)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    areabuttonList = []
    actionbuttonList = []

    x = 400
    y1 = 140
    y2 = 260

    AREAABUTTON = [(x-120,y1), (100, 100), 'areaA']
    AREABBUTTON = [(x, y1), (100, 100), 'areaB']
    AREACBUTTON = [(x+120, y1), (100, 100), 'areaC']

    ACTIONABUTTON = [(x-120,y2), (100, 100), 'actionA']
    ACTIONBBUTTON = [(x,y2), (100, 100), 'actionB']
    ACTIONCBUTTON = [(x+120,y2), (100, 100), 'actionC']

    areaFrame = [(x-80, 380), (100,100), ' ']
    actionFrame = [(x+80, 380), (100, 100),' ']

    area = batArea
    action = batAction

    createButton(BUTTONFONT, 'Area A', BLACK, LRED, AREAABUTTON[0], AREAABUTTON[1])
    areabuttonList.append(AREAABUTTON)

    createButton(BUTTONFONT, 'Area B', BLACK, LRED, AREABBUTTON[0], AREABBUTTON[1])
    areabuttonList.append(AREABBUTTON)

    createButton(BUTTONFONT, 'Area C', BLACK, LRED, AREACBUTTON[0], AREACBUTTON[1])
    areabuttonList.append(AREACBUTTON)

    createButton(BUTTONFONT, 'Action A', BLACK, LRED, ACTIONABUTTON[0], ACTIONABUTTON[1])
    actionbuttonList.append(ACTIONABUTTON)

    createButton(BUTTONFONT, 'Action B', BLACK, LRED, ACTIONBBUTTON[0], ACTIONBBUTTON[1])
    actionbuttonList.append(ACTIONBBUTTON)

    createButton(BUTTONFONT, 'Action C', BLACK, LRED, ACTIONCBUTTON[0], ACTIONCBUTTON[1])
    actionbuttonList.append(ACTIONCBUTTON)

    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'combat']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])

    #event handler
    if mouseClicked == True:
        for button in areabuttonList:
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                area = holder
                break
        
        for button in actionbuttonList:
            holder = clickCheck(button, mX, mY)
            if holder != 'oops':
                action = holder
                break

        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops' and area != 'none' and action != 'none':
            pass
        else: newState = 'area'

    if area == 'areaA':
        areaFrame[2]= 'Area A'
    elif area == 'areaB':
        areaFrame[2]= 'Area B'
    elif area == 'areaC':
        areaFrame[2]= 'Area C'
    
    if action == 'actionA':
        actionFrame[2]= 'Action A'
    elif action == 'actionB':
        actionFrame[2]= 'Action B'
    elif action == 'actionC':
        actionFrame[2]= 'Action C'

    createButton(BUTTONFONT, areaFrame[2], BLACK, LRED, areaFrame[0], areaFrame[1])
    createButton(BUTTONFONT, actionFrame[2], BLACK, LRED, actionFrame[0], actionFrame[1])

    main.mouseClicked = False
    return newState, area, action


def combatScene(area, action, playerTeam, eTeam, playerScore, enemyScore):

    BUTTONFONT = pygame.font.Font('freesansbold.ttf', 26)
    newState = 'combat'
    itr = 0
    result = ''
    eScore = enemyScore
    pScore = playerScore
    newWeeks = weeks
    newSupport = support

    if combatComplete == False:
        newWeeks = weeks - 1
        for a in playerTeam:
            result = combatLoop(a, eTeam[itr], eScore, pScore, itr)
            if result == 'player':
                pScore += 1
            elif result == 'enemy':
                eScore += 1
            elif result == 'tie':
                pass
            itr += 1

    #score Text
    pScoreText = f"Player Score: {playerScore}"
    infoFont = pygame.font.Font('freesansbold.ttf', 24)
    playerTextObj = infoFont.render(pScoreText, True, LRED)
    playerRectObj = playerTextObj.get_rect()
    playerRectObj.topleft = (100,100)

    eScoreText = f"Enemy Score: {enemyScore}"
    enemyTextObj = infoFont.render(eScoreText, True, LRED)
    enemyRectObj = enemyTextObj.get_rect()
    enemyRectObj.topleft = (500,100)

    #Results Text
    resultsText = "Results"
    resultsTextObj = infoFont.render(resultsText, True, LRED)
    resultsRectObj = resultsTextObj.get_rect()
    resultsRectObj.topleft = (350, 200)

    supScore = resultsCalc(area, action, pScore, eScore)
    scoreText = str(supScore)
    supScoreText = "Support: " + scoreText
    supTextObj = infoFont.render(supScoreText, True, LRED)
    supRectObj = supTextObj.get_rect()
    supRectObj.topleft = (350, 250)

    weeksText = f"Weeks Left: {newWeeks}"
    weeksTextObj = infoFont.render(weeksText, True, LRED)
    weeksRectObj = weeksTextObj.get_rect()
    weeksRectObj.topleft = (350, 300)

    #Next Button
    NEXTBUTTON = [(400, 500), (240, 80), 'place holder']
    createButton(BUTTONFONT, 'Next', BLACK, LRED, NEXTBUTTON[0], NEXTBUTTON[1])


    DISPLAYSURF.blit(playerTextObj, playerRectObj)
    DISPLAYSURF.blit(enemyTextObj, enemyRectObj)
    DISPLAYSURF.blit(resultsTextObj, resultsRectObj)
    DISPLAYSURF.blit(supTextObj, supRectObj)
    DISPLAYSURF.blit(weeksTextObj, weeksRectObj)

    #event handler
    if mouseClicked == True:
        newState = clickCheck(NEXTBUTTON, mX, mY)
        if newState != 'oops':
            newSupport = supScore + support
            if newWeeks > 0:
                newState = 'team'
            elif newWeeks == 0:
                newState = 'end'
        else: newState = 'combat'

    

    return newState, pScore, eScore, newSupport, newWeeks


def endScene():
    a = 0

def errorScene():
    a = 0

if __name__ == '__main__':
    main()