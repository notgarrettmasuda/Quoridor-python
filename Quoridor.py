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
rows, columns = (17, 17)
boardArray = [[None]*rows for _ in range(columns)]
boardArray[8][0] = 'p1'
boardArray[8][16] = 'p2'
#boardArray[12][10] = 'w'
#boardArray[13][10] = 'w'
#boardArray[14][10] = 'w'
#boardArray[7][7] = 'w'
#boardArray[7][8] = 'w'
#boardArray[7][9] = 'w'

#class GameLogic:
#    def playerMove(board):



#wallLogic
class WallLogic:
    def wallCountRow(board):
        res = []
        for i in range(rows):
            count = 0
            temp = []
            for j in range(columns):
                if board[i][j] == 'w':
                    count += 1
                    temp.append((j, i))
                    if count == 3:
                        res.append(temp)
                else:
                    count = 0
                    temp = list()
        return res

    def wallCountColumn(board):
        res = []
        for i in range(rows):
            count = 0
            temp = []
            for j in range(columns):
                if board[j][i] == 'w':
                    count += 1
                    temp.append((i, j))
                    if count == 3:
                        res.append(temp)
                else:
                    count = 0
                    temp = list()
        return res
    
walls = pygame.sprite.Group()
wallbuttons = pygame.sprite.Group()

wallArray = [[None]*rows for _ in range(columns)]
for i in range(1, 9):
    for j in range(1, 9):
        tempButton = pygame.draw.rect(screen, BLACK, pygame.Rect(defaultPosX + wallSize/2 + (blockSize + wallSize) * i + ((i - 1) * wallSize), 
                                                                defaultPosY - wallSize/2 + ((blockSize + (2 * wallSize)) * j),
                                                                wallSize, wallSize))
        wallArray[i - 1][j - 1] = tempButton

rotateButton = pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 50, 50))

def createAVerticalWall(x, y):
    a = x  * 2
    y = y - 1
    y = y * 2
    for i in range(3):
        b = i
        boardArray[y + b][a - 1] = 'w'
    
def createAHorizontalWall(x, y):
    a = y  * 2
    x = x - 1
    x = x * 2
    for i in range(3):
        b = i
        boardArray[a - 1][b + x] = 'w'

def drawAHorizontalWall(board):
    rowCoords = WallLogic.wallCountRow(board)
    for i in range(len(rowCoords)):
        temp = rowCoords[i]
        if len(rowCoords) > 0:
            wallCoordX, wallCoordY = temp[0]
        if len(rowCoords) > 0:
            #print(str(wallCoordX) + ", " + str(wallCoordY))
            if wallCoordY != 1:
                wallCoordY = ((2 * wallCoordY) - 1)/2
            #print(wallCoordY)
            wall = Rect(defaultPosX + wallSize/2 + ((blockSize + (2 * wallSize)) * wallCoordX), 
                        defaultPosY + wallSize/2 + ((blockSize + wallSize) * wallCoordY) + ((wallCoordY - 1) * wallSize),
                        (blockSize + (1.5 * wallSize)) * 2, wallSize, YELLOW)
            walls.add(wall)

def drawAVerticalWall(board):
    columnCoords = WallLogic.wallCountColumn(board)
    for i in range(len(columnCoords)):
        temp = columnCoords[i]
        if len(columnCoords) > 0:
            wallCoordX, wallCoordY = temp[0]
        if len(columnCoords) > 0:
            wallCoordX = wallCoordX + 1
            wall = Rect((defaultPosX + wallSize/2 + (blockSize + wallSize) * (wallCoordX/2)) + ((wallCoordX/2) - 1) * wallSize, 
                        defaultPosY + wallSize/2 + ((blockSize + (2 * wallSize)) * (wallCoordY / 2)),
                        wallSize, (blockSize + (1.5 * wallSize)) * 2, YELLOW)
        walls.add(wall)


def displayBoard(board):
    for i in range(rows):
        for j in range(columns):
            if board[j][i] == 'p1':
                player1.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * (i / 2), defaultPosY + wallSize + (blockSize + (2 * wallSize)) * (j / 2))
                player1.draw()
            if board[j][i] == 'p2':
                player2.move(defaultPosX + wallSize + (blockSize + (2 * wallSize)) * (i / 2), defaultPosY + wallSize + (blockSize + (2 * wallSize)) * (j / 2))
                player2.draw()

def findPlayerPos(board, player):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == player:
                return [i, j]
            

def main():
    run = True
    horizontal = True
    while run:
        clock.tick(FPS)
        
        #Background
        screen.fill(WOODBROWN)
        
        #Board
        pygame.draw.rect(screen, EDGYRED, pygame.Rect(SCREEN_WIDTH * 1/26, SCREEN_HEIGHT * 1/26, boardBorder, boardBorder))
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, WHITE, pygame.Rect(defaultPosX + wallSize + (i * blockSize) + (2 * i * wallSize), defaultPosY + wallSize + (j * blockSize) + (2 * j * wallSize), blockSize, blockSize))

        displayBoard(boardArray)
        
        drawAHorizontalWall(boardArray)
        drawAVerticalWall(boardArray)
        walls.draw(screen)
        moveUpButton = moveButton(up_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y - player1.rect.height/5)
        moveRightButton = moveButton(right_arrow_img, player1.rect.x + player1.rect.width * 6/5, player1.rect.y + player1.rect.height/2)
        moveDownButton = moveButton(down_arrow_img, player1.rect.x + player1.rect.width/2, player1.rect.y + player1.rect.height * 6/5)
        moveLeftButton = moveButton(left_arrow_img, player1.rect.x - player1.rect.width/5, player1.rect.y + player1.rect.height/2)
        moveUpButton2 = moveButton(up_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y - player2.rect.height/5)
        moveRightButton2 = moveButton(right_arrow_img, player2.rect.x + player2.rect.width * 6/5, player2.rect.y + player2.rect.height/2)
        moveDownButton2 = moveButton(down_arrow_img, player2.rect.x + player2.rect.width/2, player2.rect.y + player2.rect.height * 6/5)
        moveLeftButton2 = moveButton(left_arrow_img, player2.rect.x - player2.rect.width/5, player2.rect.y + player2.rect.height/2)
        temp = findPlayerPos(boardArray, 'p1')
        if temp[0] != 16:
            moveRightButton.draw()
        if temp[1] != 0:
            moveUpButton.draw()
        if temp[0] != 0:
            moveLeftButton.draw()
        if temp[1] != 16:
            moveDownButton.draw()
        temp = findPlayerPos(boardArray, 'p2')
        if temp[0] != 16:
            moveRightButton2.draw()
        if temp[1] != 0:
            moveUpButton2.draw()
        if temp[0] != 0:
            moveLeftButton2.draw()
        if temp[1] != 16:
            moveDownButton2.draw()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #player1 controls
                temp = findPlayerPos(boardArray, 'p1')
                if moveRightButton.rect.collidepoint(event.pos) and temp[0] != 16:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x + 2][y] = 'p1'
                if moveUpButton.rect.collidepoint(event.pos) and temp[1] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x][y - 2] = 'p1'
                if moveLeftButton.rect.collidepoint(event.pos) and temp[0] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x - 2][y] = 'p1'
                if moveDownButton.rect.collidepoint(event.pos) and temp[1] != 16:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x][y + 2] = 'p1'

                #player2 controls
                temp = findPlayerPos(boardArray, 'p2')
                if moveRightButton2.rect.collidepoint(event.pos) and temp[0] != 16:     
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x + 2][y] = 'p2'
                if moveUpButton2.rect.collidepoint(event.pos) and temp[1] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x][y - 2] = 'p2'
                if moveLeftButton2.rect.collidepoint(event.pos) and temp[0] != 0:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x - 2][y] = 'p2'
                if moveDownButton2.rect.collidepoint(event.pos) and temp[1] != 16:
                    x, y = int(temp[0]), int(temp[1])
                    boardArray[x][y] = None
                    boardArray[x][y + 2] = 'p2'

                #wall interactions
                for i in range(1, 9):
                    for j in range(1, 9):
                        tempButton = wallArray[i - 1][j - 1]
                        if tempButton.collidepoint(event.pos):
                            if horizontal == False:
                                createAVerticalWall(i, j)
                                wallArray[i - 1][j - 1] = pygame.draw.rect(screen, BLACK, pygame.Rect(-100, - 100, 1, 1))
                                if j != 9:
                                    wallArray[i - 1][j] = pygame.draw.rect(screen, BLACK, pygame.Rect(-100, - 100, 1, 1))
                                elif j != 1:
                                    wallArray[i - 1][j - 2] = pygame.draw.rect(screen, BLACK, pygame.Rect(-100, - 100, 1, 1))
                            if horizontal == True:
                                createAHorizontalWall(i, j)
                                print(str(i) + ", " + str(j))

                if rotateButton.collidepoint(event.pos) and horizontal == False:
                    horizontal = True
                if rotateButton.collidepoint(event.pos) and horizontal == True:
                    horizontal = True
        for i in range(8):
            for j in range(8):
                tempButton = wallArray[i][j]
                a, b = pygame.mouse.get_pos()        
                if tempButton.x <= a <= tempButton.x + wallSize and tempButton.y <= b <= tempButton.y + wallSize:
                    pygame.draw.rect(screen, (YELLOW), tempButton)
                else:
                    pygame.draw.rect(screen, (WOODBROWN), tempButton)
        a, b = pygame.mouse.get_pos()   
        if tempButton.x <= a <= tempButton.x + wallSize and tempButton.y <= b <= tempButton.y + wallSize:
            pygame.draw.rect(screen, (192, 192, 192), rotateButton)
        else:
            pygame.draw.rect(screen, (128, 128, 128), rotateButton)

            #keys_pressed = pygame.key.get_pressed()
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main() 