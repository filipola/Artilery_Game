from math import sin,cos,radians
import random

#TODO: Deal with all TODOs in this file and also remove the TODO and HINT comments.

""" This is the model of the game"""
class Game:
    """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """
    
    def __init__(self, cannonSize, ballSize):
        self.cannonSize = cannonSize
        self.ballSize = ballSize
        self.getCurrentPlayerIndex = 0
        self.currentWind = (random.random() * 20) - 10

        self.players = [
            Player(self, False, -90, 'blue'),
            Player(self, True, 90, 'red')
        ]

        # Here we create two players in a list with self, if its reversed (what player it is)
        # a position and a color
        # we initialize in class Game and send in cannonSize, ballSize and also create currentWind

        

    #getters and setters for players, cannons, wind, rounds etc.
    """ A list containing both players """
    def getPlayers(self):
        return self.players

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize

    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        return self.players[self.getCurrentPlayerIndex]
    """ The opponent of the current player """
    def getOtherPlayer(self):
        return self.players[1 - self.getCurrentPlayerIndex]  
    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.getCurrentPlayerIndex
    
    """ Switch active player """
    def nextPlayer(self):
        self.getCurrentPlayerIndex = 1 - self.getCurrentPlayerIndex

    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.currentWind = wind
    
    def getCurrentWind(self):
        return self.currentWind

    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        self.currentWind = (random.random() * 20) - 10

""" Models a player """
class Player:

    def __init__(self, game, isReversed, xPos, color):
        self.game = game
        self.isReversed = isReversed
        self.xPos = xPos
        self.color = color
        self.angle = 0
        self.score = 0
        self.velocity = 0
        # we created a init constructor for class Player where we called class game in a variable game
        # set isReversed, xPos, color and also gave angle, score and velocity a staring value

    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        if self.isReversed:
            self.angle = 180 - angle
        else:
            self.angle = angle
        
        self.velocity = velocity

        return Projectile(self.angle,self.velocity, self.game.getCurrentWind(),self.xPos, self.game.getCannonSize() / 2, -110, 110)

        #we set if its player two the angle is 180 - angle and player 1 just angle, we set velocity as velocity
        # we return these values to class Projectile where we finalize the game

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj):
        ballsize = self.game.getBallSize()
        cannonsize = self.game.getCannonSize()
        proj_xPos = proj.getX()

        ball_leftedge = proj_xPos - ballsize
        ball_rightedge = proj_xPos + ballsize

        cannon_leftedge = (self.xPos - (cannonsize / 2))
        cannon_rightedge = (self.xPos + (cannonsize / 2))

        if ball_rightedge < cannon_leftedge:
            return ball_rightedge - cannon_leftedge
        
        if ball_leftedge > cannon_rightedge:
            return ball_leftedge - cannon_rightedge
        
        return 0
        # here we give the program the distance from where the projicle lands to the cannon.
        # if the projectile misses on the leftedge of the cannon it gives back a negative value
        # and if it misses on the rightedge it gives back a positive value.
        # if we hit (distance is zero) we return 0 to Projectile and it updates the score
        # (see Projectile)

    # getters and setter for class Player, sets and gets Scores, colors, xPos, angle and velocity
    """ The current score of this player """
    def getScore(self):
        return self.score

    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.score += 1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.color

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.xPos

    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return self.angle, self.velocity



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile:
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
        wind: The wind speed value affecting this projectile
        xPos and : The initial position of this projectile
        xLower and xUpper: The lowest and highest x-positions allowed
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind

        # initialize function for class Projectile


    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    # getters for class Projectile
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos
