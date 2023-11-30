
import tkinter,createMap,math,random


mapName = 'Map1.txt'
Map = createMap.create(mapName)

#function to move the tank on the board
def move(Object,others,user_input):
    if Object.speed >= 2:
        x = Object.x1
        y = Object.y1
        for i in range(0,4):
            if user_input == Object.movements[i]:
                user_input = i
                continue
        if user_input == 0:
            Object.y1 -= 1
        if user_input == 1:
            Object.x1 -= 1
        if user_input == 2:
            Object.y1 += 1
        if user_input == 3:
            Object.x1 += 1
        if Map[Object.y1][Object.x1] == '|':
            Object.x1 = x
        if Map[Object.y1][Object.x1] == '-':
            Object.y1 = y
        for i in range(len(others)):
            if ((Map[Object.y1][Object.x1] == '#') or (Map[Object.y1][Object.x1] == others[i].look)) and (user_input == 1 or user_input == 3):
                Object.x1 = x
            if ((Map[Object.y1][Object.x1] == '#') or (Map[Object.y1][Object.x1] == others[i].look)) and (user_input == 0 or user_input == 2):
                Object.y1 = y
        Map[y][x] = ' '
        Map[Object.y1][Object.x1] = Object.look 
        Object.speed = 0

#function to determine if the tanks have a clear line of sight to each other              
def sight(Object,angle,other):
    end = len(Map[0])-1
    yEnd = len(Map)-1
    objAngle = angle % (2*math.pi)
    row = 0
    column = 0
    if (math.pi/2 < objAngle < 3*math.pi/2):
        end = 0
    if (math.pi < objAngle < 2*math.pi):
            yEnd = 0
    if (math.pi/4 < objAngle < 3*math.pi/4) or (5*math.pi/4 < objAngle < 7*math.pi/4):
        dis = abs(abs(Object.y1-yEnd)*pHeight/math.sin(objAngle))
    else:
        dis = abs(abs(Object.x1-end)*pWidth/math.cos(objAngle))
    pos = 0
    while  pos < dis:
        pos += 1
        x = Object.x1Px + pos*math.cos(objAngle)
        y = Object.y1Px + pos*math.sin(objAngle)
        for i in range(len(Map)):
            if i*pHeight <= y < (i+1)*pHeight:
                column = i
                break
        for num in range(len(Map[0])):
            if (center + pWidth*(num - len(Map[0])/2)) <= x < (center + pWidth*(num+ 1 - len(Map[0])/2)):
                row = num
                break
        if (Map[column][row] == '|') or (Map[column][row] == '-') or (Map[column][row] == '#') or (Map[column][row] == other.look):
           return [row,column,Map[column][row]]
           break

#creates the game board
class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.board = []
        self.stop = 'no'
        self.keys = dict.fromkeys(('a','w','s','d','Up','Left','Down','Right','space','5','j'))
        canvas.bind("<KeyPress>", self.keypress)
        canvas.bind("<KeyRelease>", self.keypress)
        self.canvas.focus_set()
        for i in range(len(Map)): 
            self.board.append(canvas.create_text((150+pWidth*len(Map[0]))/2,2.75+(pHeight*i), anchor='center', text=''.join(Map[i]), font=('Consolas',11)))
           
    def keypress(self,event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = event.type == '2'
            
    def updateBoard(self):
        if len(players) == 1:
            self.stop = 'yes'
            self.canvas.delete('all')
            window.create_text(center, canvasHeight-canvasHeight/2-25, anchor='center', text=players[0].name + str(" won!"), font=('Consolas',40))
        if self.stop !='yes':
            for num in range(len(players)):
                others = []
                for count in range(len(players)):
                    if players[num] != players[count]:
                        others.append(players[count])
                players[num].update()
                players[num].actions(others)
                players[num].update()
                if players[num].hitpoints <= 0:
                    self.canvas.itemconfig(players[num].hitBox,fill='grey')
                    self.canvas.itemconfig(players[num].barrel,fill='black')
                    players[num].update()
                    players.pop(num)
                    break
            for i in range(len(self.board)):
                self.canvas.itemconfigure(self.board[i], text=''.join(Map[i]))
            if self.stop != 'yes':
                self.canvas.after(25,self.updateBoard)
        
#constructs the tanks and variables associated with it        
class Player:
    def __init__(self, look, name, colour, bColour, side, movements, fire):
        self.movements = movements
        self.speed = 1
        self.fire = fire
        self.side = side
        self.angle = self.side*math.pi +2*math.pi
        self.angle2 = self.side*math.pi +2*math.pi
        self.hitpoints = 9
        self.colour=colour
        self.cooldown = 75
        self.charge = self.cooldown
        self.look = look
        self.name = name
        self.turnSpeed = 1
        self.pos = createMap.locate(self.look,mapName)
        self.x1 = self.pos[1]
        self.y1 = self.pos[0]
        self.x1Px = (center + pWidth*(self.x1 - len(Map[0])/2)) + pWidth/2
        self.y1Px = pHeight*self.y1 + pHeight/2
        self.xA = 7*math.cos(math.pi)
        self.yA = 7*math.sin(math.pi)       
        self.hitBox = window.create_rectangle(self.x1Px-pWidth/2, self.y1Px-pHeight/2, self.x1Px+pWidth/2, self.y1Px+pHeight/2, fill=self.colour)
        self.barrel = window.create_line(self.x1Px, self.y1Px, self.x1Px + self.xA, self.y1Px + self.yA, width = 3, fill=bColour)
        self.health = window.create_rectangle(self.side*center+center/2-40,canvasHeight -80, (self.side*center+center/2)+40, (canvasHeight -80)+15, fill='green')
        self.bar = window.create_rectangle(self.side*center+center/2-40,canvasHeight -80, (self.side*center+center/2)+40, (canvasHeight -80)+15)
        self.nameText = window.create_text(self.side*center+center/2, canvasHeight - 90, anchor='center', text=self.name+str("'s health"), font=('Consolas',8))
        self.reload = window.create_text(self.side*center+center/2, canvasHeight - 50, anchor='center', text=str("Reload time: ") + str(int(150 - self.charge)), font=('Consolas',8))
        self.update()
        
    def update(self):
        window.itemconfig(self.nameText, text=self.name+str("'s health"))
        if self.charge >= self.cooldown:
            self.charge = self.cooldown
        self.x1Px = (center + pWidth*(self.x1 - len(Map[0])/2)) + pWidth/2
        self.y1Px = pHeight*self.y1 + pHeight/2
        self.xA = 7*math.cos(self.angle2)
        self.yA = 7*math.sin(self.angle2)
        window.coords(self.hitBox, self.x1Px-pWidth/2, self.y1Px-pHeight/2, self.x1Px+pWidth/2, self.y1Px+pHeight/2)
        window.coords(self.barrel, self.x1Px, self.y1Px, self.x1Px + self.xA, self.y1Px + self.yA)
        window.itemconfigure(self.reload, text=str("Reload time: ") + str(int(self.cooldown - self.charge)))
        window.coords(self.health, self.side*center+center/2-40,canvasHeight -80, (self.side*center+center/2-40)+80*(self.hitpoints/9), (canvasHeight -80)+15)
        if .2 < self.hitpoints/9 <= .4:
            window.itemconfig(self.health, fill='yellow')
        if self.hitpoints/9 <= .2:
            window.itemconfig(self.health, fill='red')
            
    def bTurn(self):
        if 0 < (abs(round((self.angle2 % (2* math.pi)),2) - round((self.angle % (2* math.pi)),2))) < math.pi:
            turn = .01
            if (abs(round((self.angle2 % (2* math.pi)),2) - round((self.angle % (2* math.pi)),2))) > 4*math.pi/180:
                turn = .04
            if (self.angle2 % (2* math.pi)) < (self.angle % (2* math.pi)):
                self.angle2 += turn * self.turnSpeed
            else:
                self.angle2 -= turn * self.turnSpeed
        elif math.pi < (abs(round((self.angle2 % (2* math.pi)),2) - round((self.angle % (2* math.pi)),2))) < 2*math.pi:
            turn = .04
            if (abs(round((self.angle2 % (2* math.pi)),2) - round((self.angle % (2* math.pi)),2))) > 176*math.pi/180:
                turn = .01
            if (self.angle2 % (2* math.pi)) < (self.angle % (2* math.pi)):
                self.angle2 -= turn * self.turnSpeed
            else:
                self.angle2 += turn * self.turnSpeed
        if 0 < ((self.angle2 % (2* math.pi)) - (self.angle % (2* math.pi))) <= .09:
            self.angle2 = self.angle
            
    def actions(self,others):
        for char in self.movements:
            if (gameBoard.keys[char] and not gameBoard.keys[self.fire]):
                move(self, others,char)
        self.speed += 1
        self.charge +=1
        self.update()
        for number in range(len(others)):
            angularPos(self,others[number])
            view = sight(self,self.angle,others[number])
            if (view[2] == others[number].look):
                self.bTurn()
                self.update()
            if gameBoard.keys[self.fire] and self.charge >= self.cooldown:
                crit = random.randint(1,20)
                target = sight(self, self.angle2,others[number])
                x1 = self.x1Px + self.xA
                y1 = self.y1Px + self.yA
                x2 = self.x1Px + pWidth*(target[0]-self.x1)
                y2 = self.y1Px + pHeight*(target[1]-self.y1)
                self.shoot = window.create_line(x1,y1,x2,y2,fill='cyan',width=1)
                if crit == 1:
                    window.itemconfig(self.shoot, width=3, fill='yellow')
                else:
                    window.itemconfig(self.shoot, width=1, fill='cyan')
                if (view[0] == target[0]) and (view[1] == target[1]) and (view[2] == others[number].look):
                    if crit == 1:
                        others[number].hitpoints -= 2
                        self.charge = 0
                    else:
                        others[number].hitpoints -= 1
                        self.charge = 0
                else:
                    self.charge = 0
                window.after(150, window.delete,self.shoot)
            self.update()
 
#function to determine orientation of turret
def angularPos(objectPov,object2):
    dis = math.sqrt((objectPov.x1Px-object2.x1Px)**2+(objectPov.y1Px-object2.y1Px)**2)
    angle = math.acos(abs(objectPov.y1Px-object2.y1Px)/dis)
    if (objectPov.y1Px < object2.y1Px) and (objectPov.x1Px < object2.x1Px):
        objectPov.angle = math.pi/2 - angle
    if (objectPov.y1Px < object2.y1Px) and (objectPov.x1Px > object2.x1Px):
        objectPov.angle = math.pi/2 + angle
    if (objectPov.y1Px > object2.y1Px) and (objectPov.x1Px > object2.x1Px):
        objectPov.angle = 3*math.pi/2 - angle
    if (objectPov.y1Px > object2.y1Px) and (objectPov.x1Px < object2.x1Px):
        objectPov.angle = 3*math.pi/2+angle
    if (objectPov.y1Px > object2.y1Px) and (objectPov.x1Px == object2.x1Px):
        objectPov.angle = 3*math.pi/2
    if (objectPov.y1Px < object2.y1Px) and (objectPov.x1Px == object2.x1Px):
        objectPov.angle = math.pi/2
    if (objectPov.y1Px == object2.y1Px) and (objectPov.x1Px > object2.x1Px):
        objectPov.angle = math.pi
    if (objectPov.y1Px == object2.y1Px) and (objectPov.x1Px < object2.x1Px):
        objectPov.angle = 2*math.pi      

def dist(x,y,x2,y2):
    return math.sqrt(((x-x2)**2+(y-y2)**2))

#stores the names of the players    
names =[]         
for i in range(2):
    names.append(input('Player ' + str(i+1) + '\'s name:'))

#creates the game window
pHeight = 9
pWidth = 8.05        
root = tkinter.Tk()
root.title("Simple")
window = tkinter.Canvas(root, height=100+pHeight*len(Map)-(pHeight/2-1), width=150+pWidth*len(Map[0])-4)
window.pack()
root.update()
center = root.winfo_width()/2
canvasHeight = root.winfo_height()

players = []

if len(names) == 2:
    player1 = Player('x', 'Player 1', 'salmon', 'dark green', 0,['w','a','s','d'],'space')
    players.append(player1)
    player2 = Player('+', 'Player 2', 'blue', 'orange',1, ['Up','Left','Down','Right'],'5')
    players.append(player2)
    
for i in range(len(names)):
    players[i].name = names[i]    

gameBoard = Board(window)

gameBoard.updateBoard()




root.mainloop()