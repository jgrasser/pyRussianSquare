
#Import Modules
import os, pygame, random
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#------------------------------------------------------------------------------------------#
# Loading scripts                                                       Joseph Grasser     # 
#------------------------------------------------------------------------------------------#
# This section is where all the all the functions for loading the alphabet file and        #
# Hollow Square images is defined                                                          # 
# -----------------------------------------------------------------------------------------#
def load_alphabet(alphabet_file, charwidth, charheight):
    letterImage = pygame.image.load( alphabet_file )
    letters = []
    
    height = letterImage.get_height()
    width = letterImage.get_width()
    x = 0 
    y = 0
    while y+charheight < height and x < width:
        letters.append( letterImage.subsurface(pygame.Rect(x, y, charwidth, charheight) ) )   
        y = y + charheight 

    return letters

def big_Alpha():
    char_width = 32
    char_height = 40
    alpha = load_alphabet(os.path.join('data', 'abcdefghijkl_big.tga' ), char_width, char_height) 
    alpha.extend( load_alphabet(os.path.join('data', 'mnopqrstuvwx_big.tga' ), char_width, char_height) )
    alpha.extend( load_alphabet(os.path.join('data', 'yzplus_big.tga' ), char_width, char_height) )
    alpha.extend( load_alphabet(os.path.join('data', 'numeralsBig.tga' ), char_width, char_height) )
    return alpha

def small_Alpha():
    char_width = 16
    char_height = 20
    alpha = load_alphabet(os.path.join('data', 'abcdefghijkl.tga' ), char_width, char_height) 
    alpha.extend( load_alphabet(os.path.join('data', 'mnopqrstuvwx.tga' ), char_width, char_height) )
    alpha.extend( load_alphabet(os.path.join('data', 'yzplus.tga' ), char_width, char_height) )
    alpha.extend( load_alphabet(os.path.join('data', 'numerals.tga' ), char_width, char_height) )
    return alpha

def colorfy(image, color):
    for x in range(0, image.get_width()):
        for y in range(0, image.get_height()):
            pixel = image.get_at((x,y))
            image.set_at((x,y) , (color[0], color[1], color[2], pixel[3]))
    return image

def hollow_square(color, scale_x=-1, scale_y=-1):
    image = pygame.image.load( os.path.join('data', 'pieceHalo.tga' ) )
    for x in range(0, image.get_width()):
        for y in range(0, image.get_height()):
            pixel = image.get_at((x,y))
            image.set_at((x,y) , (color[0], color[1], color[2], pixel[3]))
    if scale_x == -1:
        return image
    else:
        return pygame.transform.scale(image, (scale_x, scale_y))
    
#------------------------------------------------------------------------------------------#
# Global Variables                                                      Joseph Grasser     # 
#------------------------------------------------------------------------------------------#
# This section is where all the global variables are defined and initilizd.                # 
# -----------------------------------------------------------------------------------------#
windowDimension = (620, 500)
screen = pygame.display.set_mode(windowDimension)
scene = 0
letterKey = ['a','b','c','d','e','f','g','h', 'i', 'j', 'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '+', ' ', '0','1','2','3','4','5','6','7','8','9','.']

#colors
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
purple = 200, 0, 255
colors = [red, green, blue, yellow, purple]

hollow_squares = []
for color in colors:
    hollow_squares.append( hollow_square( color, 35, 35 ) )

big_alphabet = big_Alpha()
small_alphabet = small_Alpha()

#------------------------------------------------------------------------------------------#
# GUI Utilities                                                      Joseph Grasser        # 
#------------------------------------------------------------------------------------------#
# Functions for drawing text, and borders on the screen.                                   # 
# -----------------------------------------------------------------------------------------#  
def init():
    pygame.init()
    pygame.display.set_caption('Russian Squares v1.0')
    pygame.mouse.set_visible(1)

def darkenScreen(screen):
    color = (0, 0, 0, 0)
    darkScreen = pygame.Surface(windowDimension, SRCALPHA)
    alpha = 0
    while alpha < 255 :
        darkScreen.fill(color)
        screen.blit(darkScreen, (0,0))
        alpha = alpha + 1
        color = color[0],color[1],color[2],alpha
        for x in range(0, 10):
            print "Waiting"

def addText(screen, alpha, text, location):
    x = location[0]
    y = location[1]
    text = text.lower()
    for i in range(0, len(text)):
        letter = text[i]
        key = letterKey.index(letter)
        screen.blit(alpha[key], (x+i*alpha[key].get_width()/2,y))

def addParagraph(screen, title, text, position):
	addText(screen, big_alphabet, title, position)
	text = text.split('\n')
	y = 1
	for line in text:
		y = y + 1
		addText(screen, small_alphabet, line, (position[0], position[1] + 16*y))

def drawBorder(Surface):
    paneWidth = Surface.get_width()
    paneHeight = Surface.get_height()
    borderTop = pygame.image.load(os.path.join('data','gridLineTop.tga'))  
    borderBottom = pygame.image.load(os.path.join('data','gridLineBottom.tga'))   
    borderLeft = pygame.image.load(os.path.join('data','gridLineLeft.tga'))   
    borderRight = pygame.image.load(os.path.join('data','gridLineRight.tga'))  
    for x in range( 0, paneWidth/40):
        for y in range( 0, paneHeight/40):
            if x == 0 and y >= 0:
                Surface.blit(borderLeft, (0, y*40))
            if x >= 0 and y == 0:
                Surface.blit(borderTop, (x*40,0))
            if x+1 == paneWidth/40 and y >= 0:
                Surface.blit(borderRight, ((x)*40, y*40))
            if x >= 0 and y+1 == paneHeight/40:
                Surface.blit(borderBottom, (x*40, (y)*40))      

#------------------------------------------------------------------------------------------#
# GUI Components                                                     Joseph Grasser        # 
#------------------------------------------------------------------------------------------#
# Section contains the following gui components: Menus, Enterboxes, and Scoreboards        # 
# -----------------------------------------------------------------------------------------# 
class GUI_Menu(pygame.Surface):
    def load_selection_square(self):
        image =  pygame.image.load(os.path.join('data', 'Hammer_and_sickle.png'))
        image = pygame.transform.scale(image, (40, 40))
        return image
		
    def __init__(self, commands, width, alphabet):
        pygame.Surface.__init__(self, (width+40, 20+len(commands)*alphabet[0].get_height())) 
        self.commands = commands
        self.alphabet = alphabet
        self.printOptions()
        self.selectionSquare = self.load_selection_square()
        self.angle = 0
        self.index = 0
		
    def up(self):
        if self.index > 0:
            self.index -= 1

    def down(self):
        if self.index+1 < len(self.commands):
            self.index += 1

    def printOptions(self):
        y = 10
        for x in range(0, len(self.commands)):
            addText(self, self.alphabet, self.commands[x], (40, y + self.alphabet[0].get_height()*x) )

    def update(self):
        self.fill((0,0,0))
        self.printOptions()
        drawBorder(self)
        self.blit(self.selectionSquare, (10, 10+self.index*self.alphabet[0].get_height()))

class GUI_EnterBox(pygame.Surface):
    def __init__(self, alpha):
        pygame.Surface.__init__(self, (500, 60))
        self.box = hollow_square( (0,0,255), 500, 60)
        self.alphabet = alpha
        
    def update(self, data):
        self.fill((0,0,0))
        self.blit(self.box, (0,0))
        addText(self, self.alphabet, data, (100,10))

class GUI_Scoreboard(pygame.Surface):
    def __init__(self, alphabet):
        pygame.Surface.__init__(self, (225, 420))
        self.alphabet = alphabet
        self.xoffset = 10
        self.yoffset = 10
        self.score = 0
        self.time = 0
        self.color = "Blue"        

    def update(self, time, score):
        self.fill((0,0,0))
        addText(self, self.alphabet, str(time), (self.xoffset, self.yoffset) ) 
        addText(self, self.alphabet, "00000000" +  str(score), (self.xoffset, 25) )
        addText(self, self.alphabet, "Red x3", (self.xoffset+3, self.yoffset+self.alphabet[0].get_height()*7) )

#------------------------------------------------------------------------------------------#
# Scene Section                                                      Joseph Grasser        # 
#------------------------------------------------------------------------------------------#
# Contains all the scenes in the game.                                                     # 
# -----------------------------------------------------------------------------------------# 
class Scene_Title(pygame.Surface):
    def __init__(self):	
        pygame.Surface.__init__(self, windowDimension)
        self.menu = GUI_Menu(["New Game", "High Scores", "Instructions", "Quit Game"], 225, big_alphabet)
        self.menu.update()	
    
    def start(self):
        #<>Title loop start
        while 1:    
            self.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return 0
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    self.menu.down()
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.menu.up()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    if( self.menu.index == 0 ):
                        #New game selected
                        return Scene_Difficulty()
                    elif( self.menu.index == 1 ):
                        #High scores selected
                        print "High Score wanted"
                    elif( self.menu.index == 2 ):
                        #Instructions selected
                        return Scene_Instructions()
                    else : 
                        #Exit selected
                        return 0

    def update(self):
        self.fill(black)
        drawBorder(self)
        addText(self, big_alphabet, "Russian Squares version1.0", (34,50) )	
        self.menu.update()        
        self.blit( self.menu, (275, 250) )
        screen.blit(self, (0,0))
        pygame.display.flip()

class Scene_Difficulty(pygame.Surface):
    def __init__(self):	
        pygame.Surface.__init__(self, windowDimension)
        self.menu = GUI_Menu(["Easy", "Moderate", "Difficult"], 225, big_alphabet)	
 
    def start(self):      
        while 1:  
            self.update()   
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return Scene_Title()
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    self.menu.down()
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.menu.up()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    if (self.menu.index == 0):
                        return Scene_Board("EASY")
                    elif(self.menu.index == 1):
                        return Scene_Board("MEDIUM")
                    elif(self.menu.index == 2):
                        return Scene_Board("HARD")

    def update(self):
        self.fill(black)
        self.menu.update()
        drawBorder(self)
        addText(self, big_alphabet, "Choose Difficulty", (160, 75) )
        self.blit( self.menu, (175, 150) )
        screen.blit(self, (0,0))
        pygame.display.flip()

class Scene_Instructions(pygame.Surface):
    def __init__(self):	
        pygame.Surface.__init__(self, windowDimension)
	
    def start(self):
        #<>Title loop start
        while 1:    
            self.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return Scene_Title()
        #<>Game Loop End

    def update(self):
        self.fill(black)
        drawBorder(self)
        addParagraph(self,"Description", "Russian squares is a very challenging and fun logic game.  Each\n"+
                "game begins with a 4 by 4 block. Each time the clock runs down\n" + 
                "to zero another row or column is added to the block. Player gains\n" + 
                "points by elimating rows or columns. Scores enough points he will\n" +
                "advance another level. Doing so will make game more difficult.", (50, 50))
        addParagraph(self,"Objective", "Try to make the big block disappear. Fill a column or\n" +
                "row with one color and that column or row will dissapear. Player\n" +
                "will gain points for each column or row they eliminate. If column\n" +
                "or row is glowing player gains 4 times the points. Try to advance\n" +
                "as far as you can. Climb the highscore list.", (50, 170) )
        addParagraph(self, "License", "This is an opensource implementation of a Microsoft Game of the same\n" +
                "name. This application was developed by Joseph Graser\n" +
                "jgrasser DOT dev AT gmail.com in a stunning 24 hours. \n" +
                "Russian Squares v1.0 is licensed under the GPL3.0. All artwork is\n" +
                "licensed under the Creative Commons License. No artists name\n"
                "could be found on artwork.", (50, 290) )	
        addText(self, small_alphabet, "Press Escape to go back to Title Screen", (260, 450) )
        screen.blit(self, (0,0))	
        pygame.display.flip()	

def enterNameScene(screen, big_a, small_a):
    drawBorder(screen)
    addText(screen, big_a, "highscore", (340, 50) )	
    
    box = GUI_EnterBox( big_a )
    boxStart = (170, 150)
    screen.blit(box, boxStart)
    
    #<>Title loop start
    data = "name"
    box.update(data)
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                if( len(data) > 0 ):
                    data = data.__getslice__(0, len(data)-1)
            elif (event.type == KEYDOWN and (event.key == K_SPACE or (event.key >= K_a and event.key <= K_z) or (event.key >= K_0 and event.key <= K_9)) and len(data) < 18 ):
                data = data + chr(event.key)
        box.update(data)
        screen.blit(box, boxStart)
        pygame.display.flip()
    #<>Game Loop End	

class Square(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.blinking = 0
        self.spinning = 0
        self.angle = 0
        self.image = random.choice( hollow_squares )
        self.original = self.image
        self.rect = self.image.get_rect()
        
    def goTo(self, x, y):
        self.loc = [x,y]
        self.rect.center = x+50, y + 16    
   
    def update(self):            
        if self.blinking:
            self.blink()
        elif self.spinning:
            self.spin()
   
    def spin(self):
        center = self.rect.center
        self.angle = self.angle + 12
        if self.angle >= 360:
            self.angle = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)


    def blink(self):
        if( self.image == self.image1 ):
            self.image = self.image2
        else:
            self.image = self.image1

class Scene_Board(pygame.Surface):
    def __init__(self, difficulty):
        pygame.Surface.__init__(self, windowDimension)
        self.board = [  [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0]
                     ]
        self.active = 0,0
        sprite = Square((0,0,0))
        self.set(self.active, sprite)
        self.sprites = [sprite]
        for x in range( 1, len( self.board )-1 ):
            for y in range( 1, len( self.board[2] )-1):
                sprite = Square((0,0,0))
                self.sprites.append(sprite)
                self.set((x,y),sprite)
        self.seenSprites = pygame.sprite.RenderPlain(self.sprites)

    def collapseSquare(self):
        midpoint = windowDimension[0]/2 , windowDimension[1]/2
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                piece = self.board[x][y]
                if piece == 0:                    
                    continue
                x_l = x*35 + 35
                y_l = y*35 + 35
                if len(self.board)%2 >= 0 :
                    x_l = x_l + 35/2
                if len(self.board[1])%2 !=0:
                    y_l = x_l + 35/2
                piece.goTo(x_l,y_l)

    def get( self, location ):
        return self.board[location[0]][location[1]]
    
    def set(self, location, piece):
        if piece != 0 :  
            self.board[location[0]][location[1]] = piece
        else :
            self.board[location[0]][location[1]] = 0

    def move(self, piece, current, new):
        if self.get(new) == 0:
            self.set(new, piece)
            return new
        else:
            x_diff = (new[0] - current[0])
            y_diff = (new[1] - current[1])
            newLocation = new[0] +x_diff, new[1] + y_diff
            nextCurrent = new
            nextPiece = self.get(new)
            self.set(new, piece)
            return self.move(nextPiece, nextCurrent, newLocation)

    def removeCol(self, col):
        pieceCol = self.active[0]
        piece = self.get(self.active) 
        if pieceCol >= col :
            old = self.active
            piece = self.get(old)
            self.active = self.active[0]-1, self.active[1]
        self.board.pop(col)
        self.set(self.active, piece)
   
    def removeRow(self, row): 
        pieceRow = self.active[1] 
        piece = self.get(self.active)       
        if pieceRow >= row:
            old = self.active
            piece = self.get(old)
            self.active = self.active[0], self.active[1]-1
        for x in range(0, len(self.board)):
            self.board[x].pop(row)
        self.set(self.active, piece)

    def findCompleteRowsColomns(self):
        for x in range(1, len(self.board)-1):
            piece = self.get((x,1))
            col = [piece]
            for y in range(2, len(self.board[0])-1):
                piece2 = self.get((x, y))
                if piece.image == piece2.image:
                    col.append(piece2)  
                else :
                    col = []
                    break
            if col != [] :
                self.removeCol(x)
                return col

        for y in range(1, len(self.board[0])-1):
            piece = self.get((1,y))
            row = [piece]
            for x in range(2, len(self.board)-1):
                piece2 = self.get((x, y))
                if piece.image == piece2.image:
                    row.append(piece2)  
                else :
                    row = []
                    break
            if row != [] :
                self.removeRow(y)
                return row
            
        return []
                       
    def start(self):
        #<>Title loop start
        while 1:  
            #Search and remove completed rows and columns 
            squares = self.findCompleteRowsColomns()	
            while( squares != [] ):
            	for square in squares:
                	square.spinning = 1 
                	square.kill()
                squares = self.findCompleteRowsColomns()  
            
            #Look for player input
            activeSprite = 0
            newLocation = self.active 
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return 0
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    if self.active[1] + 1 < len(self.board[0]):
                        activeSprite = self.get(self.active)
                        newLocation = self.active[0], self.active[1] + 1
                elif event.type == KEYDOWN and event.key == K_UP:
                    if self.active[1] > 0:
                        activeSprite = self.get(self.active)
                        newLocation = self.active[0], self.active[1] - 1
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    if self.active[0]+1 < len(self.board):
                        activeSprite = self.get(self.active)
                        newLocation = self.active[0]+1, self.active[1]
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    if self.active[0] > 0:
                        activeSprite = self.get(self.active)
                        newLocation = self.active[0]-1, self.active[1]    
                elif event.type == KEYDOWN and event.key == K_p:
                    self.printBoard("Printing") 
            
            #Respond to input 
            if activeSprite != 0:
                self.old = self.active
                self.active = self.move(activeSprite, self.active, newLocation)
                self.set(self.old, 0)
            self.update()
        #<>Game Loop End
            
    def printBoard(self, st):
        s = st + "Board --------------------------------\n"
        for y in range(0, len(self.board[0])):        
            for x in range(0, len(self.board)):
                piece = self.get((x,y))
                if piece != 0 :
                    piece = "|" + str(x) +"," + str(y) + "|"
                s = s + str(piece)     
            s = s + '\n'
        print s + "$----------------------------------"
        for y in range(0, len(self.board[0])):        
            for x in range(0, len(self.board)):
                piece = self.get((x,y))
                if piece != 0 :
                    print str(piece.loc)
            
    def update(self):
        self.fill(black)
        #drawBorder(self)
        self.collapseSquare()
        self.seenSprites.update()
        self.seenSprites.draw(self) 
        screen.blit(self, (0,0))	
        pygame.display.flip()		
    
def main():
    init()
	
    pygame.mixer.init()
    pygame.mixer.music.load( os.path.join('data', 'ussr.union77.ogg') )
    pygame.mixer.music.play(-1)
	
    scene = Scene_Title()
    #<>Game loop start
    while scene != 0:
        #fade into scene   
        scene = scene.start()   
    #<>Game Loop End
    return 0

#Game Over



if __name__ == '__main__': 
    main()
