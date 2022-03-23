import pygame
from pygame import mixer


# The root class that defines the most basic attributes for all other menus of the game
class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100
        self.selectSound = mixer.Sound("ui_select.mp3")
    # creates a star like cursor that blinks next to selected item

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display,(0, 0))
        pygame.display.update()
        self.game.reset_keys()
# The first menu that gets initialized on start of game
class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        # menu attributes and inner sections
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h+30
        self.optionsx,self.optionsy = self.mid_w,self.mid_h+50
        self.creditsx,self.creditsy = self.mid_w,self.mid_h+70
        self.cursor_rect.midtop = (self.startx + self.offset ,self.starty)

    # function responsible for keeping the display visible on screen
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_inputs()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 20 , self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2-20)
            self.game.draw_text("Start Game",20 , self.startx,self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
    #to move the star like cursor next to selected items
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx+self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx+self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
    # to check for any input given by user ,essentially keyboard inputs
    def check_inputs(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.game.soundsOn:
                self.selectSound.play()
            if self.state == "Start":
                self.game.playing = False
                self.game.curr_menu = self.game.start
            elif self.state == "Options":
                self.game.curr_menu = self.game.optionsMenu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.creditsMenu
            self.run_display = False

# The menu that holds the actual game and board
class StartMenu(Menu):
    # defining board attributes and numbers positions and message
    def __init__(self, game):
        Menu.__init__(self, game)
        self.playerOneTurn = True
        self.playerTwoTurn = False
        self.image0x,self.image0y,self.image0Fixed = 0,700,False
        self.image1x,self.image1y,self.image1Fixed = 60,700,False
        self.image2x,self.image2y,self.image2Fixed = 120,700,False
        self.image3x,self.image3y,self.image3Fixed = 180,700,False
        self.image4x,self.image4y,self.image4Fixed = 240,700,False
        self.image5x,self.image5y,self.image5Fixed = 300,700,False
        self.image6x,self.image6y,self.image6Fixed = 360,700,False
        self.image7x,self.image7y,self.image7Fixed = 420,700,False
        self.image8x,self.image8y,self.image8Fixed = 480,700,False
        self.image9x,self.image9y,self.image9Fixed = 540,700,False
        self.box1,self.box2,self.box3,self.box4,self.box5,self.box6,self.box7,self.box8,self.box9 = False,False,False,False,False,False,False,False,False
        self.gameWin , self.gameDraw , self.gameEnd= False,False,False
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.actualNumbersBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.message = ""
        self.allowedToPlay = True

    # fynction responsible for keeping the board on the screen
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_winner()
            self.game.check_events()
            self.check_inputs()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_lines(self.game.display, self.game.WHITE, (200, 0), (200, 600), 10)
            self.game.draw_lines(self.game.display, self.game.WHITE, (400, 0), (400, 600), 10)
            self.game.draw_lines(self.game.display, self.game.WHITE, (0, 200), (600, 200), 10)
            self.game.draw_lines(self.game.display, self.game.WHITE, (0, 400), (600, 400), 10)

            if self.gameEnd:
                self.allowedToPlay = False
                if self.gameWin:
                    if not self.playerOneTurn:
                        self.message = "player one wins"
                    else:
                        self.message = "player two wins"
                else:
                    self.message = "it's a draw"

            else:
                if self.playerOneTurn:
                    self.message = "it is player one's turn"
                else:
                    self.message = "it is player two's turn"
            self.game.draw_text(self.message, 30, 180, 650)
            self.game.add_Images("zero", self.image0x, self.image0y)
            self.game.add_Images("two", self.image2x, self.image2y)
            self.game.add_Images("four", self.image4x,self.image4y)
            self.game.add_Images("six", self.image6x, self.image6y)
            self.game.add_Images("eight", self.image8x, self.image8y)
            self.game.add_Images("one", self.image1x, self.image1y)
            self.game.add_Images("three", self.image3x, self.image3y)
            self.game.add_Images("five", self.image5x, self.image5y)
            self.game.add_Images("seven", self.image7x, self.image7y)
            self.game.add_Images("nine", self.image9x, self.image9y)

            self.blit_screen()
    # function that detects position of mouse on board to select specific cells
    def checkMousePosition(self):
        if self.game.mx < 200 and self.game.my < 200:
            self.box1 = True
            return 80,80,0,0
        elif self.game.mx > 200 and self.game.mx < 400 and self.game.my <200:
            self.box2 = True
            return 300,100,0,1
        elif self.game.mx>400 and self.game.my < 200:
            self.box3 = True
            return 500,100,0,2
        elif self.game.mx < 200 and self.game.my < 400 and self.game.my > 200:
            self.box4 = True
            return 100,300,1,0
        elif self.game.mx>200 and self.game.mx<400 and self.game.my < 400 and self.game.my > 200:
            self.box5 = True
            return 300,300,1,1
        elif self.game.mx>400 and self.game.my < 400 and self.game.my > 200:
            self.box6 = True
            return 500,300,1,2
        elif self.game.mx < 200 and self.game.my>400:
            self.box7 = True
            return 100,500,2,0
        elif self.game.mx >200 and self.game.mx < 400 and self.game.my>400:
            self.box8 = True
            return 300,500,2,1
        elif self.game.mx>400 and self.game.my>400:
            self.box9 = True
            return 500,500,2,2

    # checking every possible input by user to interact with the game such as mouse movements and clicking
    def check_inputs(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.allowedToPlay:
            if self.game.left_Click:
                self.game.left_Click = False
                if 0<=self.game.mx <60 and self.game.my >=700 and self.playerTwoTurn and not self.image0Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image0x = mx
                            self.image0y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 0
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image0Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 60 <= self.game.mx < 120 and self.game.my >= 700 and self.playerOneTurn and not self.image1Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image1x = mx
                            self.image1y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 1
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image1Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 120 <= self.game.mx < 180 and self.game.my >= 700 and self.playerTwoTurn and not self.image2Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image2x = mx
                            self.image2y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 2
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image2Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 180 <= self.game.mx < 240 and self.game.my >= 700 and self.playerOneTurn and not self.image3Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image3x = mx
                            self.image3y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 3
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image3Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 240 <= self.game.mx < 300 and self.game.my >= 700 and self.playerTwoTurn and not self.image4Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image4x = mx
                            self.image4y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 4
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image4Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 300 <= self.game.mx < 360 and self.game.my >= 700 and self.playerOneTurn and not self.image5Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image5x = mx
                            self.image5y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 5
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image5Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 360 <= self.game.mx < 420 and self.game.my >= 700 and self.playerTwoTurn and not self.image6Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image6x = mx
                            self.image6y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 6
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image6Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 420 <= self.game.mx < 480 and self.game.my >= 700 and self.playerOneTurn and not self.image7Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image7x = mx
                            self.image7y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 7
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image7Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 480 <= self.game.mx < 540 and self.game.my >= 700 and self.playerTwoTurn and not self.image8Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image8x = mx
                            self.image8y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 8
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image8Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
                elif 540 <= self.game.mx <= 600 and self.game.my >= 700 and self.playerOneTurn and not self.image9Fixed:
                    while not self.game.left_Click:
                        self.game.check_events()
                        mx, my, i, j = self.checkMousePosition()
                        if self.game.left_Click and self.board[i][j] != "X":
                            self.image9x = mx
                            self.image9y = my
                            self.board[i][j] = "X"
                            self.actualNumbersBoard[i][j] = 9
                            print(self.board)
                            self.playerOneTurn = not self.playerOneTurn
                            self.playerTwoTurn = not self.playerTwoTurn
                            self.image9Fixed = True
                        else:
                            self.game.left_Click = False
                    self.game.left_Click = False
    # function that checks if the board contains a sum of 15 or is full and declare game state
    # either winning of a player or a draw
    def check_winner(self):
        sum = 0
        xsCount = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=="X":
                    xsCount+=1
        if xsCount == 9:
            self.gameEnd = True
        else:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "X":
                        sum += self.actualNumbersBoard[i][j]
                    else:
                        sum = 0
                        break

                if sum==15:
                    self.gameWin = True
                    self.gameEnd = True
                    break
                else:
                    sum = 0
            if not self.gameEnd:
                #check cols:
                sum = 0
                for i in range(3):
                    for j in range(3):
                        if self.board[j][i] == "X":
                            sum += self.actualNumbersBoard[j][i]
                        else:
                            sum = 0
                            break
                    if sum ==15:
                        self.gameWin = True
                        self.gameEnd = True
                        break
                    else:
                        sum = 0
            if not self.gameEnd:
                #check diagonals
                sum = 0
                #d1
                for i in range(3):
                    if self.board[i][i] == "X":
                        sum+= self.actualNumbersBoard[i][i]
                    else:
                        sum = 0
                        break
                if sum == 15:
                    self.gameWin = True
                    self.gameEnd = True
                else:
                    sum = 0
                if not self.gameEnd:
                    #d2
                    sum = self.actualNumbersBoard[2][2] + self.actualNumbersBoard[1][1] + self.actualNumbersBoard[2][0]
                    if sum == 15 and(self.board[2][2]==self.board[1][1]==self.board[2][0]=="X"):
                        self.gameWin = True
                        self.gameEnd = True
                    else:
                        sum = 0
# options menu that holds one option which is sound control
class Options(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_inputs()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Sound:",20,self.game.DISPLAY_WIDTH/2-10, self.game.DISPLAY_HEIGHT/2)
            self.game.draw_text("On" if self.game.soundsOn else "Off",20,self.game.DISPLAY_WIDTH/2+50,self.game.DISPLAY_HEIGHT/2)
            self.blit_screen()
    def check_inputs(self):
        if self.game.START_KEY:
            self.game.soundsOn = not self.game.soundsOn
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

# credits menu that holds the author of the code and the game
class Credits(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_inputs()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Created By",20,self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2)
            self.game.draw_text("Hossam Ahmed Fouad", 20, self.game.DISPLAY_WIDTH / 2, self.game.DISPLAY_HEIGHT /2+20)
            self.blit_screen()

    def check_inputs(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False