
#Import Modules
import os, pygame, random
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

letterKey = ['a','b','c','d','e','f','g','h', 'i', 'j', 'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '+', ' ', '0','1','2','3','4','5','6','7','8','9','.']

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
purple = 200, 0, 255

colors = [red, green, blue, yellow, purple]

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

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

hollow_squares = []
for color in colors:
    hollow_squares.append( hollow_square( color, 35, 35 ) )
    
def init():
    pygame.init()
    screen = pygame.display.set_mode((825, 460))
    pygame.display.set_caption('Russian Squares v1.0')
    pygame.mouse.set_visible(1)
    return screen

def addText(screen, alpha, text, location):
    x = location[0]
    y = location[1]
    text = text.lower()
    for i in range(0, len(text)):
        letter = text[i]
        key = letterKey.index(letter)
        screen.blit(alpha[key], (x+i*alpha[key].get_width()/2,y))

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

class Menu(pygame.Surface):
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

class Scoreboard(pygame.Surface):
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
        drawBorder(self)
        addText(self, self.alphabet, "Time +" + str(time), (self.xoffset, self.yoffset) ) 
        addText(self, self.alphabet, "SCORE +" +  str(score), (self.xoffset, self.yoffset+self.alphabet[0].get_height()*2) )
        addText(self, self.alphabet, "Bonus Color", (self.xoffset+3, self.yoffset+self.alphabet[0].get_height()*7) )

def titleScene(screen, big_a, small_a):
    drawBorder(screen)
	
    menu = Menu(["New Game", "High Scores", "Instructions", "Quit Game"], 225, big_a)
    menu.update()	
	
    russianFlag = pygame.image.load( os.path.join('data', 'Soviet_Flag.jpg' ) )
    screen.blit( russianFlag, (100, 150) )
	
    addText(screen, big_a, "Russian Squares version1.0", (34,50) )
    addText(screen, small_a, "Licensed under the GPL3.0 + Author is Joseph Grasser + Email jgrasser DOT dev AT gmail.com", (34,400) )	

    #<>Title loop start
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                menu.down()
                menu.update()
            elif event.type == KEYDOWN and event.key == K_UP:
                menu.up()
                menu.update()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return menu.index
        screen.blit( menu, (500, 150) )
        pygame.display.flip()
    #<>Game Loop End

def difficultlyScene(screen, big_a, small_a):
    drawBorder(screen)
	
    menu = Menu(["Easy", "Moderate", "Difficult"], 225, big_a)
    menu.update()	
	
    addText(screen, big_a, "Choose Difficulty", (260, 75) )
    
    #<>Title loop start
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                menu.down()
                menu.update()
            elif event.type == KEYDOWN and event.key == K_UP:
                menu.up()
                menu.update()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return menu.index
        screen.blit( menu, (272, 150) )
        pygame.display.flip()
    #<>Game Loop End

def addParagraph(screen, big_a, small_a, title, text, position):
	addText(screen, big_a, title, position)
	text = text.split('\n')
	y = 0
	for line in text:
		y = y + 1
		addText(screen, small_a, line, (position[0]+200, position[1] + 16*y))
	
def instructionScene(screen, big_a, small_a):
    drawBorder(screen)
    addParagraph(screen, big_a, small_a, "Description", "Russian squares is a very challenging and fun logic game.  Each\n"+
            "game begins with a 4 by 4 block. Each time the clock runs down\n" + 
            "to zero another row or column is added to the block. Player gains\n" + 
            "points by elimating rows or columns. Scores enough points he will\n" +
            "advance another level. Doing so will make game more difficult.", (50, 50))
    addParagraph(screen, big_a, small_a, "Objective", "Try to make the big block disappear. Fill a column or\n" +
            "row with one color and that column or row will dissapear. Player\n" +
            "will gain points for each column or row they eliminate. If column\n" +
            "or row is glowing player gains 4 times the points. Try to advance\n" +
            "as far as you can. Climb the highscore list.", (50, 160) )
    addParagraph(screen, big_a, small_a, "License", "This is an opensource implementation of a Microsoft Game of the same\n" +
            "name. This application was developed by Joseph Graser\n" +
            "jgrasser DOT dev AT gmail.com in a stunning 24 hours. \n" +
            "Russian Squares v1.0 is licensed under the GPL3.0. All artwork is\n" +
            "licensed under the Creative Commons License. No artists name\n"
            "could be found on artwork.", (50, 270) )	
    addText(screen, small_a, "Press Escape to go back to Title Screen", (260, 420) )	
    
    #<>Title loop start
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == KEYDOWN and event.key == K_SPACE:
                screen.fill((0,0,0))
                return menu.index
        pygame.display.flip()
    #<>Game Loop End	

class EnterBox(pygame.Surface):
    def __init__(self, alpha):
        pygame.Surface.__init__(self, (500, 60))
        self.box = hollow_square( (0,0,255), 500, 60)
        self.alphabet = alpha
        
    def update(self, data):
        self.fill((0,0,0))
        self.blit(self.box, (0,0))
        addText(self, self.alphabet, data, (100,10))

def enterNameScene(screen, big_a, small_a):
    drawBorder(screen)
    addText(screen, big_a, "highscore", (340, 50) )	
    
    box = EnterBox( big_a )
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

class GameBoard(pygame.Surface):
    def __init__(self):
        # 550 w    420 h
        # center  225, 210
        pygame.Surface.__init__(self, (550, 420))
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
        locations = []
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                piece = self.board[x][y]
                if piece == 0:                    
                    continue
                x_l = x*35
                y_l = y*35
                locations.append( [x, y] ) 
                #if len(self.board)%2 != 0 :
                #    x_l = (x-1) * 35 + 35/2
                #if len(self.board[1])%2 !=0:
                #    y_l = (y-1) * 35 + 35/2
                piece.goTo(x_l,y_l)
        for i in range(0, len(locations)):
            if locations.count(locations[i]) > 1 :
                print "Double trouble: " + str(locations[i])

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
                       
    def signal(self, direction):
        activeSprite = 0
        newLocation = self.active
        if direction == "LEFT" and self.active[0] > 0:
            activeSprite = self.get(self.active)
            newLocation = self.active[0]-1, self.active[1]
        elif direction == "RIGHT" and self.active[0]+1 < len(self.board):
            activeSprite = self.get(self.active)
            newLocation = self.active[0]+1, self.active[1]
        elif direction == "UP" and self.active[1] > 0:
            activeSprite = self.get(self.active)
            newLocation = self.active[0], self.active[1] - 1
        elif direction == "DOWN" and self.active[1] + 1 < len(self.board[0]):
            activeSprite = self.get(self.active)
            newLocation = self.active[0], self.active[1] + 1
        else:
            return
        
        if activeSprite != 0:
            self.old = self.active
            self.active = self.move(activeSprite, self.active, newLocation)
            self.set(self.old, 0)

            squares = self.findCompleteRowsColomns()
            for square in squares:
                square.spinning = 1 
                square.kill()
    
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
        
def gameScene(screen, big_a, small_a):
    drawBorder(screen)
    scoreboard = Scoreboard(big_a)
    gameboard = GameBoard()
    
    #<>Title loop start
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return -1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                gameboard.signal("DOWN")
            elif event.type == KEYDOWN and event.key == K_UP:
                gameboard.signal("UP")
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                gameboard.signal("RIGHT")
            elif event.type == KEYDOWN and event.key == K_LEFT:
                gameboard.signal("LEFT")    
            elif event.type == KEYDOWN and event.key == K_p:
                gameboard.printBoard("Printing")    

        scoreboard.update( "20.59", 100)
        gameboard.update()
        screen.blit(scoreboard, (580, 20))
        screen.blit(gameboard, (20 ,20))
        pygame.display.flip()
    #<>Game Loop End	
    
def main():
    screen = init()
    big_alphabet = big_Alpha()
    small_alphabet = small_Alpha()
	
    pygame.mixer.init()
    pygame.mixer.music.load( os.path.join('data', 'ussr.union77.ogg') )
    pygame.mixer.music.play(-1)
	
    #x = titleScene(screen, big_alphabet, small_alphabet)
    #x = difficultlyScene(screen, big_alphabet, small_alphabet)
    #instructionScene(screen, big_alphabet, small_alphabet)
    #name = enterNameScene(screen, big_alphabet, small_alphabet)
     
    gameScene(screen, big_alphabet, small_alphabet)
    
    #create allsprites rendergroup
    #allsprites = pygame.sprite.RenderPlain((gameSquare))
   
    #<>Game loop start
    while 1:    
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
     #   update sprites and background
     #   allsprites.update()
     #   allsprites.draw(screen)
        pygame.display.flip()        
    #<>Game Loop End


#Game Over



if __name__ == '__main__': 
    main()
