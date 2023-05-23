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

#gameLogic
rows, columns = (9, 9)
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

def findObjectPos(board, player):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == player:
                return [i, j]

def getHorizontalWallCount():
    res = []
    for i in range(rows):
        for j in range(columns):
            if horizontalWallPositions[i][j] == 'w':
                res.append((j, i))
    return res

def getVerticalWallCount():
    res = []
    for i in range(rows):
        for j in range(columns):
            if verticalWallPositions[i][j] == 'w':
                res.append((j, i))
    return res

def horizontalWallCheck(x, y):
    if verticalWallPositions[x][y] != 'w':
        if x == 8:
            if horizontalWallPositions[x - 1][y] == None:
                return True
        if horizontalWallPositions[x - 1][y] == None and horizontalWallPositions[x + 1][y] == None:
            return True
    return False

def verticalWallCheck(x, y):
    if horizontalWallPositions[x][y] != 'w':
        if y == 8:
            if verticalWallPositions[x][y - 1] == None:
                return True
        if verticalWallPositions[x][y - 1] == None and verticalWallPositions[x][y + 1] == None:
            return True
    return False

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


def displayBoard(board):
    for i in range(rows):
        for j in range(columns):
            if board[j][i] == 'p1':
                player1.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * i, defaultPosY + wallSize + (blockSize + (2 * wallSize)) * j)
                player1.draw()
            if board[j][i] == 'p2':
                player2.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * i, defaultPosY + wallSize + (blockSize + (2 * wallSize)) * j)
                player2.draw()
            

def main():
    run = True
    horizontal = False
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
        
        moveUpButton = moveButton(up_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y - player1.rect.height/5)
        moveRightButton = moveButton(right_arrow_img, player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
        moveDownButton = moveButton(down_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y + player1.rect.height * 6/5)
        moveLeftButton = moveButton(left_arrow_img, player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
        moveUpButton2 = moveButton(up_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y - player2.rect.height/5)
        moveRightButton2 = moveButton(right_arrow_img, player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
        moveDownButton2 = moveButton(down_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y + player2.rect.height * 6/5)
        moveLeftButton2 = moveButton(left_arrow_img, player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
        temp = findObjectPos(playersPosition, 'p1')
        if temp[1] != 8:
            moveRightButton.draw()
        if temp[0] != 0:
            moveUpButton.draw()
        if temp[1] != 0:
            moveLeftButton.draw()
        if temp[0] != 8:
            moveDownButton.draw()
        temp = findObjectPos(playersPosition, 'p2')
        if temp[1] != 8:
            moveRightButton2.draw()
        if temp[0] != 0:
            moveUpButton2.draw()
        if temp[1] != 0:
            moveLeftButton2.draw()
        if temp[0] != 8:
            moveDownButton2.draw()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #player1 controls
                temp = findObjectPos(playersPosition, 'p1')
                if moveRightButton.rect.collidepoint(event.pos) and temp[1] != 8:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x][y + 1] = 'p1'
                if moveUpButton.rect.collidepoint(event.pos) and temp[0] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x - 1][y] = 'p1'
                if moveLeftButton.rect.collidepoint(event.pos) and temp[1] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x][y - 1] = 'p1'
                if moveDownButton.rect.collidepoint(event.pos) and temp[0] != 8:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x + 1][y] = 'p1'

                #player2 controls
                temp = findObjectPos(playersPosition, 'p2')
                if moveRightButton2.rect.collidepoint(event.pos) and temp[1] != 8:     
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x][y + 1] = 'p2'
                if moveUpButton2.rect.collidepoint(event.pos) and temp[0] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x - 1][y] = 'p2'
                if moveLeftButton2.rect.collidepoint(event.pos) and temp[1] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x][y - 1] = 'p2'
                if moveDownButton2.rect.collidepoint(event.pos) and temp[0] != 8:
                    x, y = int(temp[0]), int(temp[1])
                    playersPosition[x][y] = None
                    playersPosition[x + 1][y] = 'p2'

                #wall interactions
                for i in range(1, rows):
                    for j in range(1, columns):
                        tempButton = pygame.draw.rect(screen, BLACK, pygame.Rect(defaultPosX + wallSize/2 + (blockSize + wallSize) * i + ((i - 1) * wallSize), 
                                                                                 defaultPosY - wallSize/2 + ((blockSize + (2 * wallSize)) * j),
                                                                                 wallSize, wallSize))
                        if tempButton.collidepoint(event.pos):
                            if horizontal == False and verticalWallCheck(i, j):
                                verticalWallPositions[i][j] = 'w'
                                drawAVerticalWall()
                                print("vertical wall coords:" + str(i) + ", " + str(j))
                            if horizontal == True and horizontalWallCheck(i, j):
                                horizontalWallPositions[i][j] = 'w'
                                print("horizontal wall coords:" + str(i) + ", " + str(j))
                                drawAHorizontalWall()
                                

                if rotateButton.collidepoint(event.pos) and horizontal == False:
                    horizontal = True
                elif rotateButton.collidepoint(event.pos) and horizontal == True:
                    horizontal = False
        for i in range(1, rows):
            for j in range(1, columns):
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

        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main() 