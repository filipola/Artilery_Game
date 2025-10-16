from gamemodel import *
from graphics import *


class GameGraphics:
    def __init__(self, game):
        self.game = game

        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
        
        line = Line(Point(-110,0),Point(110,0))
        line.draw(self.win) # here we create a line a draw it

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

    def drawCanon(self,playerNr):
        cannonsize = self.game.getCannonSize()
        player = self.game.getPlayers()[playerNr]
        cannon_xPos = player.getX()

        rect = Rectangle(Point(cannon_xPos - (cannonsize/2),0),Point(cannon_xPos + (cannonsize/2),cannonsize))
        rect.setFill(player.getColor())
        rect.draw(self.win)
        return rect
    
        # in this function we take in cannonsize and player from class Game and Player.
        # with this information we create and draw a square  and fill it with the right color
        # we return the rectangle

    def drawScore(self,playerNr):
        player = self.game.getPlayers()[playerNr]
        cannon_xPos = player.getX()
        player_score = player.getScore()
        text = Text(Point(cannon_xPos, -5), f'Score: {player_score}')
        text.draw(self.win)
        return text

        # here we also take in information from class Game and Player in gamemodel
        # we create and draw a text that prints player_score
        # we return the text

    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)

        circle_X = proj.getX()
        circle_Y = proj.getY()
        ballsize = self.game.getBallSize()

        currentPlayerNr = self.game.getCurrentPlayerNumber()
        if self.draw_projs[currentPlayerNr] is not None:
            self.draw_projs[currentPlayerNr].undraw()
        if self.draw_projs[1 - currentPlayerNr] is not None:
            self.draw_projs[1 - currentPlayerNr].undraw()

            # if the player hits the cannon we firt undraw the former score

        circle = Circle(Point(circle_X,circle_Y),ballsize)
        circle.setFill(player.getColor())
        circle.draw(self.win)
        self.draw_projs[currentPlayerNr] = circle

        # here we draw the circle that moves


        while proj.isMoving():
            proj.update(1/50)

            # move is a function in graphics. It moves an object dx units in x direction and dy units in y direction
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)

        return proj

    def updateScore(self,playerNr):
        
        if self.draw_scores[playerNr] is not None:
            self.draw_scores[playerNr].undraw()

        self.drawScore(playerNr)
        # here we see if the player hits we undraw the former score
        # we call the function drawScore which draws the new score
        
    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind)
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()
            
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.explode() # here we call the function explode
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()
    
    def explode(self):
        current_player = self.game.getCurrentPlayer()
        other_player = self.game.getOtherPlayer()

        ballsize = self.game.getBallSize()
        cannonsize = self.game.getCannonSize()
        for r in range(ballsize,(2*cannonsize)):
            circle_explode = Circle(Point(other_player.xPos,(cannonsize/2)),r)
            circle_explode.setFill(current_player.getColor())
            circle_explode.draw(self.win)
            update(50)
            circle_explode.undraw()

            # the function explode takes in current_player, other_player from class Player in gamemodel
            # and ballsize and cannonsize from class Game in gamemodel
            # the explosion is a circle that start with the radius ballsize and continues to grow until
            # its radius is as big as 2 * cannonsize, we do this in a for-loop
            # in the for loop we draw a circle, fills it with the right color, update(50) sets the speed
            # and in the end we undraw it just to draw it again later
            
        
        



class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
