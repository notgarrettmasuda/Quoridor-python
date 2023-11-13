import pygame
import os

pygame.init()
os.chdir('C:/users/garre/OneDrive/Documents/Python/My Projects/Quoridor/Quoridor-python')

clock = pygame.time.Clock()
FPS = 60

#screen dimensions
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650

#show screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen title
pygame.display.set_caption('Quoridor')

arrow_img = pygame.image.load(os.path.join("img", "arrow.png")).convert_alpha()
arrow_width = arrow_img.get_width()
arrow_height = arrow_img.get_height()
arrow_img = pygame.transform.scale(arrow_img, (int(arrow_width * 0.05), int(arrow_height * 0.05)))
up_arrow_img = pygame.transform.rotate(arrow_img, 90)
right_arrow_img = arrow_img
down_arrow_img = pygame.transform.rotate(arrow_img, -90)
left_arrow_img = pygame.transform.rotate(arrow_img, 180)
upRight_arrow_img = pygame.transform.rotate(arrow_img, 45)
downRight_arrow_img = pygame.transform.rotate(arrow_img,-45)
upLeft_arrow_img = pygame.transform.rotate(arrow_img, 135)
downLeft_arrow_img = pygame.transform.rotate(arrow_img, -135)

#colors
WOODBROWN= (164, 116, 73)
EDGYRED = (151, 11, 45)
DARKRED = (139, 0, 0)
BLACK = (0, 0, 0)
WHITEPEACH = (100, 89.8, 70.6)
WHITE = (255, 255, 255)
YELLOW = (100, 68, 26)

rects = pygame.sprite.Group()

boardBorder = SCREEN_WIDTH * 12/13 #600
defaultPosX = SCREEN_WIDTH * 1/26 #25
defaultPosY = SCREEN_HEIGHT * 1/26 #25
blockSize = (boardBorder/9) * 5/7 
wallSize = (boardBorder/9) * 1/7

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        radius = size // 2
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)

class moveButton(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def move(self, x, y):
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

class Rect(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def draw(self):
        screen.blit(self.image, self.rect)

player1 = Player(defaultPosX + wallSize, defaultPosY + wallSize, blockSize, WHITEPEACH)
player2 = Player(defaultPosX + wallSize, defaultPosY + wallSize, blockSize, BLACK)

#game set up
rows, columns = (10, 10)
playersPosition = [[None]*rows for _ in range(columns)]
playersPosition[4][0] = 'p1'
playersPosition[4][8] = 'p2'
verticalWallPositions = [[None]*rows for _ in range(columns)]
horizontalWallPositions = [[None]*rows for _ in range(columns)]
    
walls = pygame.sprite.Group()

rotateButtonFont = pygame.font.SysFont('Arial', 30)
horizontalRotateButtonText = rotateButtonFont.render('H', True, BLACK)
verticalRotateButtonText = rotateButtonFont.render('V', True, BLACK)
horizontalRotateTextRect = horizontalRotateButtonText.get_rect(center = (SCREEN_WIDTH * 1/26 - wallSize, SCREEN_HEIGHT * 1/26 - wallSize))
verticalRotateButtonTextRect = verticalRotateButtonText.get_rect(center = (SCREEN_WIDTH * 1/26 - wallSize, SCREEN_HEIGHT * 1/26 - wallSize))
rotateButton = pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, SCREEN_WIDTH * 1/26 + wallSize, SCREEN_HEIGHT * 1/26 + wallSize))
winnerFont = pygame.font.Font(None, 50)
player1WinsText = winnerFont.render("Player 1 Wins!!", True, BLACK)
player1WinsTextRect = player1WinsText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
player2WinsText = winnerFont.render("Player 2 Wins!!", True, BLACK)
player2WinsTextRect = player2WinsText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

#find the position of object on board
def findObjectPos(board, player):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == player:
                return [i, j]

#get the coords of all horizontal walls
def getHorizontalWallCount():
    res = []
    for i in range(rows):
        for j in range(columns):
            if horizontalWallPositions[i][j] == 'w':
                res.append((j, i))
    return res

#get the coords of all vertical walls
def getVerticalWallCount():
    res = []
    for i in range(rows):
        for j in range(columns):
            if verticalWallPositions[i][j] == 'w':
                res.append((j, i))
    return res

#returns True if wall in front of player
def wallRight(player):
    playerPosition = findObjectPos(playersPosition, player)
    playerX, playerY = playerPosition[1], playerPosition[0]
    if verticalWallPositions[playerX + 1][playerY] == 'w' or verticalWallPositions[playerX + 1][playerY + 1] == 'w':
        return True
    else:
        return False

#returns True if wall is behind of player
def wallLeft(player):
    playerPosition = findObjectPos(playersPosition, player)
    playerX, playerY = playerPosition[1], playerPosition[0]
    if verticalWallPositions[playerX][playerY] == 'w' and playerY == 8:
        return True
    if verticalWallPositions[playerX][playerY] == 'w' or verticalWallPositions[playerX][playerY + 1] == 'w':
        return True
    else:
        return False
    
#returns True if wall is under player
def wallUnder(player):
    playerPosition = findObjectPos(playersPosition, player)
    playerX, playerY = playerPosition[1], playerPosition[0]
    if playerX < 8:
        if horizontalWallPositions[playerX][playerY + 1] == 'w' or horizontalWallPositions[playerX + 1][playerY + 1] == 'w':
            return True
        else:
            return False
    
#returns True if wall is over player
def wallOver(player):
    playerPosition = findObjectPos(playersPosition, player)
    playerX, playerY = playerPosition[1], playerPosition[0]
    if playerX < 8:
        if horizontalWallPositions[playerX][playerY] == 'w' or horizontalWallPositions[playerX + 1][playerY] == 'w':
            return True
        else:
            return False

#return True if vertical wall isn't there and there's a wall in front or behind coords
def horizontalWallCheck(x, y):
    if verticalWallPositions[x][y] != 'w':
        if x == 8:
            if horizontalWallPositions[x - 1][y] == None:
                return True
        if horizontalWallPositions[x - 1][y] == None and horizontalWallPositions[x + 1][y] == None:
            return True
    return False

#return True if horizontal wall isn't there and there's a wall under or over coords
def verticalWallCheck(x, y):
    if horizontalWallPositions[x][y] != 'w':
        if y == 8:
            if verticalWallPositions[x][y - 1] == None:
                return True
        if verticalWallPositions[x][y - 1] == None and verticalWallPositions[x][y + 1] == None:
            return True
    return False

#makes a wall group with all the horizontal walls
def drawAHorizontalWall():
    rowCoords = getHorizontalWallCount()
    for i in range(len(rowCoords)):
        temp = rowCoords[i]
        if len(rowCoords) > 0:
            wallCoordY, wallCoordX = temp
        if len(rowCoords) > 0:
            wallCoordX -= 1
            wall = Rect(defaultPosX + wallSize/2 + ((blockSize + (2 * wallSize)) * wallCoordX), 
                        defaultPosY + wallSize/2 + ((blockSize + wallSize) * wallCoordY) + ((wallCoordY - 1) * wallSize),
                        (blockSize + (1.5 * wallSize)) * 2, wallSize, YELLOW)
            walls.add(wall)

#makes a wall group with all the vertical walls
def drawAVerticalWall():
    columnCoords = getVerticalWallCount()
    for i in range(len(columnCoords)):
        temp = columnCoords[i]
        if len(columnCoords) > 0:
            wallCoordY, wallCoordX = temp
        if len(columnCoords) > 0:
            wallCoordY -= 1
            wall = Rect((defaultPosX + wallSize/2 + (blockSize + wallSize) * wallCoordX) + (wallCoordX - 1) * wallSize, 
                        defaultPosY + wallSize/2 + ((blockSize + (2 * wallSize)) * wallCoordY),
                        wallSize, (blockSize + (1.5 * wallSize)) * 2, YELLOW)
        walls.add(wall)

#shows the players on board
def displayBoard(board):
    for i in range(rows):
        for j in range(columns):
            if board[j][i] == 'p1':
                player1.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * i, defaultPosY + wallSize + (blockSize + (2 * wallSize)) * j)
                player1.draw()
            if board[j][i] == 'p2':
                player2.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * i, defaultPosY + wallSize + (blockSize + (2 * wallSize)) * j)
                player2.draw()

def winCondition(player):
    playerPosition = findObjectPos(playersPosition, player)
    playerX = playerPosition[1]
    if player == 'p1':
        if playerX == 8:
            return True
    elif player == 'p2':
        if playerX == 0:
            return True
    return False

def main():
    run = True
    horizontal = False
    turn = True 
    winner1 = False
    winner2 = False

    moveUpButton = moveButton(up_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y - player1.rect.height/5)
    moveRightButton = moveButton(right_arrow_img, player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
    moveDownButton = moveButton(down_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y + player1.rect.height * 6/5)
    moveLeftButton = moveButton(left_arrow_img, player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
    
    moveUpButton2 = moveButton(up_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y - player2.rect.height/5)
    moveRightButton2 = moveButton(right_arrow_img, player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
    moveDownButton2 = moveButton(down_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y + player2.rect.height * 6/5)
    moveLeftButton2 = moveButton(left_arrow_img, player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)

    moveUpRightButton = moveButton(upRight_arrow_img, player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
    moveDownRightButton = moveButton(downRight_arrow_img, player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
    moveUpLeftButton = moveButton(upLeft_arrow_img, player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
    moveDownLeftButton = moveButton(downLeft_arrow_img, player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
    
    moveUpRightButton2 = moveButton(upRight_arrow_img, player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
    moveDownRightButton2 = moveButton(downRight_arrow_img, player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
    moveUpLeftButton2 = moveButton(upLeft_arrow_img, player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
    moveDownLeftButton2 = moveButton(downLeft_arrow_img, player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)

    #swaps Turns between players
    def swapTurns(turn):
        if turn == True:
            turn = False
        elif turn == False:
            turn = True
        return turn

    while run:
        clock.tick(FPS)
        
        #Background
        screen.fill(WOODBROWN)
        
        #Board
        pygame.draw.rect(screen, EDGYRED, pygame.Rect(SCREEN_WIDTH * 1/26, SCREEN_HEIGHT * 1/26, boardBorder, boardBorder))
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, WHITE, pygame.Rect(defaultPosX + wallSize + (i * blockSize) + (2 * i * wallSize), defaultPosY + wallSize + (j * blockSize) + (2 * j * wallSize), blockSize, blockSize))

        displayBoard(playersPosition)

        #Makes buttons and places them in correct position
        moveUpButton.move(player1.rect.x + player1.rect.width/2, player1.rect.y - player1.rect.height/5)
        moveRightButton.move(player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
        moveDownButton.move(player1.rect.x + player1.rect.width/2, player1.rect.y + player1.rect.height * 6/5)
        moveLeftButton.move(player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
        
        moveUpButton2.move(player2.rect.x + player2.rect.width/2, player2.rect.y - player2.rect.height/5)
        moveRightButton2.move(player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
        moveDownButton2.move(player2.rect.x + player2.rect.width/2, player2.rect.y + player2.rect.height * 6/5)
        moveLeftButton2.move(player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
    
        moveUpRightButton.move(player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
        moveDownRightButton.move(player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
        moveUpLeftButton.move(player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
        moveDownLeftButton.move(player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
        
        moveUpRightButton2.move(player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
        moveDownRightButton2.move(player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
        moveUpLeftButton2.move(player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
        moveDownLeftButton2.move(player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
        
        #draws the movement options based on player position
        #player 1's turn
        if turn == True:
            temp = findObjectPos(playersPosition, 'p1')
            y, x = int(temp[0]), int(temp[1])
            if playersPosition[y][x + 1] == 'p2' and wallRight('p2'):
                if not wallOver('p2'):
                    moveUpRightButton.move(player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2 - arrow_img.get_height())
                    moveUpRightButton.draw()
                if not wallUnder('p2'):
                    moveDownRightButton.move(player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2 + arrow_img.get_height())
                    moveDownRightButton.draw()
            elif x != 8 and not wallRight('p1'):
                moveRightButton.draw()

            if playersPosition[y - 1][x] == 'p2' and (wallOver('p2') or y - 1 == 0):
                if not wallRight('p2'):
                    moveUpRightButton.move(player1.rect.x + player1.rect.width/2 + arrow_img.get_width(), player1.rect.y - player1.rect.height/5)
                    moveUpRightButton.draw()
                if not wallLeft('p2'):
                    moveUpLeftButton.move(player1.rect.x + player1.rect.width/2 - arrow_img.get_width(), player1.rect.y - player1.rect.height/5)
                    moveUpLeftButton.draw()
            elif y != 0 and not wallOver('p1'):
                moveUpButton.draw()

            if playersPosition[y][x - 1] == 'p2' and wallLeft('p2'):
                if not wallOver('p2'):
                    moveUpLeftButton.move(player1.rect.x + player1.rect.width/5 - arrow_img.get_width(), player1.rect.y + player1.rect.height/2 - arrow_img.get_height())
                    moveUpLeftButton.draw()
                if not wallUnder('p2'):
                    moveDownLeftButton.move(player1.rect.x + player1.rect.width/5 - arrow_img.get_width(), player1.rect.y + player1.rect.height/2 + arrow_img.get_height())
                    moveDownLeftButton.draw()
            elif x != 0 and not wallLeft('p1'):
                moveLeftButton.draw()
            if y != 8 and playersPosition[y + 1][x] == 'p2' and (wallUnder('p2') or y + 1 == 8):
                if not wallRight('p2'):
                    moveDownRightButton.move(player1.rect.x + player1.rect.width/2 + arrow_img.get_width(), player1.rect.y + player1.rect.height * 6/5)
                    moveDownRightButton.draw()
                if not wallLeft('p2'):
                    moveDownLeftButton.move(player1.rect.x + player1.rect.width/2 - arrow_img.get_width(), player1.rect.y + player1.rect.height * 6/5)
                    moveDownLeftButton.draw()
            elif y != 8 and not wallUnder('p1'):
                moveDownButton.draw()
            
        #player 2's turn
        if turn == False:
            temp = findObjectPos(playersPosition, 'p2')
            y, x = int(temp[0]), int(temp[1])
            if x != 8 and playersPosition[y][x + 1] == 'p1' and wallRight('p1'):
                if not wallOver('p1'):
                    moveUpRightButton2.move(player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2 - arrow_img.get_height())
                    moveUpRightButton2.draw()
                if not wallUnder('p1'):
                    moveDownRightButton2.move(player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2 + arrow_img.get_height())
                    moveDownRightButton2.draw()
            elif x != 8 and not wallRight('p2'):
                moveRightButton2.draw()

            if playersPosition[y - 1][x] == 'p1' and (wallOver('p1') or y - 1 == 0):
                if not wallRight('p1'):
                    moveUpRightButton2.move(player2.rect.x + player2.rect.width/2 + arrow_img.get_width(), player2.rect.y - player2.rect.height/5)
                    moveUpRightButton2.draw()
                if not wallLeft('p1'):
                    moveUpLeftButton2.move(player2.rect.x + player2.rect.width/2 - arrow_img.get_width(), player2.rect.y - player2.rect.height/5)
                    moveUpLeftButton2.draw()
            elif y != 0 and not wallOver('p2'):
                moveUpButton2.draw()

            if playersPosition[y][x - 1] == 'p1' and wallLeft('p1'):
                if not wallOver('p1'):
                    moveUpLeftButton2.move(player2.rect.x + player2.rect.width/5 - arrow_img.get_width(), player2.rect.y + player2.rect.height/2 - arrow_img.get_height())
                    moveUpLeftButton2.draw()
                if not wallUnder('p1'):
                    moveDownLeftButton2.move(player2.rect.x + player2.rect.width/5 - arrow_img.get_width(), player2.rect.y + player2.rect.height/2 + arrow_img.get_height())
                    moveDownLeftButton2.draw()
            elif x != 0 and not wallLeft('p2'):
                moveLeftButton2.draw()
            if y != 8 and playersPosition[y + 1][x] == 'p1' and (wallUnder('p1') or y + 1 == 8):
                if not wallRight('p1'):
                    moveDownRightButton2.move(player2.rect.x + player2.rect.width/2 + arrow_img.get_width(), player2.rect.y + player2.rect.height * 6/5)
                    moveDownRightButton2.draw()
                if not wallLeft('p1'):
                    moveDownLeftButton2.move(player2.rect.x + player2.rect.width/2 - arrow_img.get_width(), player2.rect.y + player2.rect.height * 6/5)
                    moveDownLeftButton2.draw()
            elif y != 8 and not wallUnder('p2'):
                moveDownButton2.draw()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #player1 controls
                if turn == True:
                    temp = findObjectPos(playersPosition, 'p1')
                    x, y = int(temp[0]), int(temp[1])
                    if moveRightButton.rect.collidepoint(event.pos) and temp[1] != 8 and not wallRight('p1'):
                        playersPosition[x][y] = None
                        if playersPosition[x][y + 1] == 'p2' and not wallRight('p2'):
                            playersPosition[x][y + 2] = 'p1'
                        else:
                            playersPosition[x][y + 1] = 'p1'
                        turn = swapTurns(turn)
                    elif moveUpButton.rect.collidepoint(event.pos) and temp[0] != 0 and not wallOver('p1'):
                        playersPosition[x][y] = None
                        if playersPosition[x - 1][y] == 'p2' and not wallOver('p2'):
                            playersPosition[x - 2][y] = 'p1'
                        else:
                            playersPosition[x - 1][y] = 'p1'
                        turn = swapTurns(turn)
                    elif moveLeftButton.rect.collidepoint(event.pos) and temp[1] != 0 and not wallLeft('p1'):
                        playersPosition[x][y] = None
                        if playersPosition[x][y - 1] == 'p2' and not wallLeft('p2'):
                            playersPosition[x][y - 2] = 'p1'
                        else:
                            playersPosition[x][y - 1] = 'p1'
                        turn = swapTurns(turn)
                    elif moveDownButton.rect.collidepoint(event.pos) and temp[0] != 8 and not wallUnder('p1'):
                        playersPosition[x][y] = None
                        if playersPosition[x + 1][y] == 'p2' and not wallUnder('p2'):
                            playersPosition[x + 2][y] = 'p1'
                        else:
                            playersPosition[x + 1][y] = 'p1'
                        turn = swapTurns(turn)

                    #diagonal controls
                    elif moveUpRightButton.rect.collidepoint(event.pos) and temp[1] != 8:
                        playersPosition[x][y] = None
                        playersPosition[x - 1][y + 1] = 'p1'
                        turn = swapTurns(turn)
                    elif moveDownRightButton.rect.collidepoint(event.pos) and temp[0] != 0:
                        playersPosition[x][y] = None
                        playersPosition[x + 1][y + 1] = 'p1'
                        turn = swapTurns(turn)
                    elif moveUpLeftButton.rect.collidepoint(event.pos) and temp[1] != 0:
                        playersPosition[x][y] = None
                        playersPosition[x - 1][y - 1] = 'p1'
                        turn = swapTurns(turn)
                    elif moveDownLeftButton.rect.collidepoint(event.pos) and temp[0] != 8:
                        playersPosition[x][y] = None
                        playersPosition[x + 1][y - 1] = 'p1'
                        turn = swapTurns(turn)
                    #print("p1 coords:" + str(x) + ", " + str(y))
                #player2 controls
                else:
                    temp = findObjectPos(playersPosition, 'p2')
                    x, y = int(temp[0]), int(temp[1])
                    if moveRightButton2.rect.collidepoint(event.pos) and temp[1] != 8 and not wallRight('p2'):     
                        playersPosition[x][y] = None
                        if playersPosition[x][y + 1] == 'p1' and not wallRight('p1'):
                            playersPosition[x][y + 2] = 'p2'
                        else:
                            playersPosition[x][y + 1] = 'p2'
                        turn = swapTurns(turn)
                    elif moveUpButton2.rect.collidepoint(event.pos) and temp[0] != 0 and not wallOver('p2'):
                        playersPosition[x][y] = None
                        if playersPosition[x - 1][y] == 'p1' and not wallOver('p1'):
                            playersPosition[x - 2][y] = 'p2'
                        else:
                            playersPosition[x - 1][y] = 'p2'
                        turn = swapTurns(turn)
                    elif moveLeftButton2.rect.collidepoint(event.pos) and temp[1] != 0 and not wallLeft('p2'):
                        playersPosition[x][y] = None
                        if playersPosition[x][y - 1] == 'p1' and not wallLeft('p1'):
                            playersPosition[x][y - 2] = 'p2'
                        else:
                            playersPosition[x][y - 1] = 'p2'
                        turn = swapTurns(turn)
                    elif moveDownButton2.rect.collidepoint(event.pos) and temp[0] != 8 and not wallUnder('p2'):
                        playersPosition[x][y] = None
                        if playersPosition[x + 1][y] == 'p1' and not wallUnder('p1'):
                            playersPosition[x + 2][y] = 'p2'
                        else:
                            playersPosition[x + 1][y] = 'p2'
                        turn = swapTurns(turn)

                    elif moveUpRightButton2.rect.collidepoint(event.pos) and temp[1] != 8:
                        playersPosition[x][y] = None
                        playersPosition[x - 1][y + 1] = 'p2'
                        turn = swapTurns(turn)
                    elif moveDownRightButton2.rect.collidepoint(event.pos) and temp[0] != 0:
                        playersPosition[x][y] = None
                        playersPosition[x + 1][y + 1] = 'p2'
                        turn = swapTurns(turn)
                    elif moveUpLeftButton2.rect.collidepoint(event.pos) and temp[1] != 0:
                        playersPosition[x][y] = None
                        playersPosition[x - 1][y - 1] = 'p2'
                        turn = swapTurns(turn)
                    elif moveDownLeftButton2.rect.collidepoint(event.pos) and temp[0] != 8:
                        playersPosition[x][y] = None
                        playersPosition[x + 1][y - 1] = 'p2'
                        turn = swapTurns(turn)

                #wall interactions
                for i in range(1, rows - 1):
                    for j in range(1, columns - 1):
                        tempButton = pygame.draw.rect(screen, BLACK, pygame.Rect(defaultPosX + wallSize/2 + (blockSize + wallSize) * i + ((i - 1) * wallSize), 
                                                                                defaultPosY - wallSize/2 + ((blockSize + (2 * wallSize)) * j),
                                                                                wallSize, wallSize))
                        if tempButton.collidepoint(event.pos):
                            if horizontal == False and verticalWallCheck(i, j):
                                verticalWallPositions[i][j] = 'w'
                                drawAVerticalWall()
                            elif horizontal == True and horizontalWallCheck(i, j):
                                horizontalWallPositions[i][j] = 'w'
                                drawAHorizontalWall()
                            turn = swapTurns(turn)

                #Button that allows player to choose whether or not player places a horizontal or vertical wall
                if rotateButton.collidepoint(event.pos) and horizontal == False:
                    horizontal = True
                elif rotateButton.collidepoint(event.pos) and horizontal == True:
                    horizontal = False
        
        for i in range(1, rows - 1):
            for j in range(1, columns - 1):
                tempButton = pygame.draw.rect(screen, BLACK, pygame.Rect(defaultPosX + wallSize/2 + (blockSize + wallSize) * i + ((i - 1) * wallSize), 
                                                                        defaultPosY - wallSize/2 + ((blockSize + (2 * wallSize)) * j),
                                                                        wallSize, wallSize))
                a, b = pygame.mouse.get_pos()        
                if tempButton.x <= a <= tempButton.x + wallSize and tempButton.y <= b <= tempButton.y + wallSize:
                    pygame.draw.rect(screen, (YELLOW), tempButton)
                else:
                    pygame.draw.rect(screen, (WOODBROWN), tempButton)

        walls.draw(screen)

        a, b = pygame.mouse.get_pos()   
        if rotateButton.x <= a <= rotateButton.x + (SCREEN_WIDTH * 1/26 + wallSize) and rotateButton.y <= b <= rotateButton.y + (SCREEN_HEIGHT * 1/26+ wallSize):
            pygame.draw.rect(screen, (192, 192, 192), rotateButton)
        else:
            pygame.draw.rect(screen, (128, 128, 128), rotateButton)

        if horizontal == True:
            screen.blit(horizontalRotateButtonText, horizontalRotateTextRect)
        elif horizontal == False:
            screen.blit(verticalRotateButtonText, verticalRotateButtonTextRect)

        if winCondition('p1'):
            winner1 = True
        elif winCondition('p2'):
            winner2 = True
            
        if winner1 == True:
            screen.blit(player1WinsText, player1WinsTextRect)
        elif winner2 == True:
            screen.blit(player1WinsText, player1WinsTextRect)
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main() 