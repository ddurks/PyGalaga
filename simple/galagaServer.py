# David Durkin, Christopher Beaufils
# 5/9/17
# galagaServer.py

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
import json
# import globalvars

################### Globals
PLAYER1_PORT = 40009
PLAYER1_HOST = ""

PLAYER2_PORT = 40021
PLAYER2_HOST = ""

# Global deferred queue, handles input from both players
dq = DeferredQueue()

















class GameState:
    #def main(self):
    def __init__(self):
        self.p1SHIP_r = '0'
        self.p1SHIP_l = '0'
        self.p2SHIP_r = '0'
        self.p2SHIP_l = '0'
        '''
        self.boost1_taken = False
        self.boost2_taken = False
        self.boost3_taken = False
        self.boost4_taken = False
        self.banana1_taken = False
        self.banana2_taken = False
        self.banana3_taken = False
        self.mario_speed = 5
        self.yoshi_speed = 5
        self.mario_in_banana = False
        self.yoshi_in_banana = False

        self.mario_was_in_box = False
        self.yoshi_was_in_box = False
        self.mario_cross_finish_line = False
        self.yoshi_cross_finish_line = False

        self.mario_won = False
        self.yoshi_won = False

        self.finish_start_x = 433
        '''
    def getPlayer1_Connection(self, p1CONN):
        self.player1_Conn = p1CONN

    def getPlayer2_Connection(self, p2CONN):
        self.player2_Conn = p2CONN
    '''
    def checkWinner(self):
        self.mario_was_in_box = True
        self.yoshi_was_in_box = True
        if self.p1SHIP_x > self.finish_start_x and self.p1SHIP_x < self.finish_start_x + 15 and self.p1SHIP_y < 257:
            print 'mario in finish box'
            if self.mario_was_in_box and self.mario_cross_finish_line:
                self.mario_won = True
                print 'mario won'
        elif self.p1SHIP_x < self.finish_start_x and self.p1SHIP_y < 257:
            self.mario_cross_finish_line = True

        if self.p2SHIP_x > self.finish_start_x and self.p2SHIP_x < self.finish_start_x + 15 and self.p2SHIP_y < 257:
            print 'yoshi in finish box'
            if self.yoshi_was_in_box and self.yoshi_cross_finish_line:
                self.yoshi_won = True
                print 'yoshi won'
        elif self.p2SHIP_x < self.finish_start_x and self.p2SHIP_y < 257:
            self.yoshi_cross_finish_line = True

    def check_track_bound(self, x, y):
		# If out of bounds, return false. If safe, return true
        if x <= 110 or x >= 1070 or y <= 110 or y >= 774:
            return False
        if y >= 250 and y <= 670 and x >= 255 and x <= 920:
            return False
        return True

    def applyBoosts(self):
        if not self.boost1_taken:
            # boost1 is still open for the taking
            if self.p1SHIP_x >= 320 and self.p1SHIP_x <= 345 and self.p1SHIP_y >= 160 and self.p1SHIP_y <= 185:
                self.mario_speed += 1
                self.boost1_taken = True
            elif self.p2SHIP_x >= 320 and self.p2SHIP_x <= 345 and self.p2SHIP_y >= 160 and self.p2SHIP_y <= 185:
                self.yoshi_speed += 1
                self.boost1_taken = True

        if not self.boost2_taken:
            # boost2 is still open for the taking
            if self.p1SHIP_x >= 140 and self.p1SHIP_x <= 165 and self.p1SHIP_y >= 420 and self.p1SHIP_y <= 445:
                self.mario_speed += 2
                self.boost2_taken = True
            elif self.p2SHIP_x >= 140 and self.p2SHIP_x <= 165 and self.p2SHIP_y >= 420 and self.p2SHIP_y <= 445:
                self.yoshi_speed += 2
                self.boost2_taken = True

        if not self.boost3_taken:
            # boost4 is still open for the taking
            if self.p1SHIP_x >= 530 and self.p1SHIP_x <= 555 and self.p1SHIP_y >= 710 and self.p1SHIP_y <= 735:
                self.mario_speed += 3
                self.boost3_taken = True
            elif self.p2SHIP_x >= 530 and self.p2SHIP_x <= 555 and self.p2SHIP_y >= 710 and self.p2SHIP_y <= 735:
                self.yoshi_speed += 3
                self.boost3_taken = True

        if not self.boost4_taken:
            # boost3 is still open for the taking
            if self.p1SHIP_x >= 930 and self.p1SHIP_x <= 955 and self.p1SHIP_y >= 490 and self.p1SHIP_y <= 515:
                self.mario_speed += 4
                self.boost4_taken = True
            elif self.p2SHIP_x >= 930 and self.p2SHIP_x <= 955 and self.p2SHIP_y >= 490 and self.p2SHIP_y <= 515:
                self.yoshi_speed += 4
                self.boost4_taken = True

    def apply_banana(self):
        if not self.banana1_taken:
            if self.p1SHIP_x >= 160 and self.p1SHIP_x <= 185 and self.p1SHIP_y >= 216 and self.p1SHIP_y <= 245:
                self.mario_in_banana = True
                self.banana1_taken = True
            elif self.p2SHIP_x >= 160 and self.p2SHIP_x <= 185 and self.p2SHIP_y >= 216 and self.p2SHIP_y <= 245:
                self.yoshi_in_banana = True
                self.banana1_taken = True
        else:
            self.mario_in_banana = False
            self.yoshi_in_banana = False
        if not self.banana2_taken:
            if self.p1SHIP_x >= 356 and self.p1SHIP_x <= 381 and self.p1SHIP_y >= 755 and self.p1SHIP_y <= 780:
                self.mario_in_banana = True
                self.banana2_taken = True
            elif self.p2SHIP_x >= 356 and self.p2SHIP_x <= 381 and self.p2SHIP_y >= 755 and self.p1SHIP_y <= 780:
                self.yoshi_in_banana = True
                self.banana2_taken = True
        else:
            self.mario_in_banana = False
            self.yoshi_in_banana = False
        if not self.banana3_taken:
            if self.p1SHIP_x >= 620 and self.p1SHIP_x <= 645 and self.p1SHIP_y >= 174 and self.p1SHIP_y <= 199:
                self.mario_in_banana = True
                self.banana3_taken = True
            elif self.p2SHIP_x >= 620 and self.p2SHIP_x <= 645 and self.p2SHIP_y >= 174 and self.p2SHIP_y <= 199:
                self.yoshi_in_banana = True
                self.banana3_taken = True
        else:
            self.mario_in_banana = False
            self.yoshi_in_banana = False
    '''

    def decode_data(self, data):


        self.p1SHIP_l = '0'
        self.p1SHIP_r = '0'
        self.p2SHIP_l = '0'
        self.p2SHIP_r = '0'

        dataList = data.split(":")
        if dataList[1] == '-1':
            return
        if dataList[0] == '1':
            # MARIO
            if dataList[1] == '275': # RIGHT
                self.p1SHIP_r = '1'
            elif dataList[1] == '276': # LEFT
                self.p1SHIP_l = '1'

        elif dataList[0] == '2':
			# YOSHI
            if dataList[1] == '275': # RIGHT
                self.p2SHIP_r = '1'
            elif dataList[1] == '276': # LEFT
                self.p2SHIP_l = '1'

        else:
            print "Error: unexpected data sent from Player"

        # self.applyBoosts() # if either player ran over a boost, apply it
        # self.checkWinner() # check at each tick if a player has won


        return_string = json.dumps({
                                    'p1Ship_l':self.p1SHIP_l,
                                    'p1Ship_r':self.p1SHIP_r,
                                    'p2Ship_l':self.p2SHIP_l,
                                    'p2Ship_r':self.p2SHIP_r,
                                    })
        self.player1_Conn.sendData(return_string)
        self.player2_Conn.sendData(return_string)
        dq.get().addCallback(self.decode_data) # after decode data, reattach callback












gs = GameState()







class Player1_Connection(Protocol):

    def __init__(self, addr):
        self.addr = addr
        PLAYER1_HOST = addr.host

    def dataReceived(self, data):
        # data received from player 1
        dq.put(data)

    def connectionMade(self):
        print "Connection receieved from player 1"
        # listen for player 2
        gs.getPlayer1_Connection(self)
        reactor.listenTCP(PLAYER2_PORT, Player2_ConnFactory(self))

    def connectionLost(self, reason):
        print "Lost connection from player 1:", str(reason)

    def startForwarding(self):
        # start forwarding the player 1 data
        print "sendData"
        dq.get().addCallback(gs.decode_data)

    def sendData(self, data):
        self.transport.write(data + '\r\n')

    def getPlayer2_Connection(self, player2_conn):
        self.player2_conn = player2_conn

class Player1_ConnFactory(Factory):

    def buildProtocol(self, addr):
        return Player1_Connection(addr)

class Player2_Connection(Protocol):

    def __init__(self, addr, player1_conn):
        self.addr = addr
        print addr
        PLAYER2_HOST = addr.host
        self.player1_conn = player1_conn

    def dataReceived(self, data):
        # data received from player 2
        dq.put(data)

    def connectionMade(self):
        print "Connection receieved from player 2"
        print "ready to begin game"
        self.player1_conn.getPlayer2_Connection(self)
        gs.getPlayer2_Connection(self)
        self.startForwarding()

    def connectionLost(self, reason):
        print "Lost connection from player 2:", str(reason)

    def startForwarding(self):
        # start forwarding the player 2 data
        dq.get().addCallback(gs.decode_data)

    def sendData(self, data):
        self.transport.write(data + '\r\n')

class Player2_ConnFactory(Factory):

    def __init__(self, player1_conn):
        self.player1_conn = player1_conn

    def buildProtocol(self, addr):
        return Player2_Connection(addr, self.player1_conn)

if __name__ == "__main__":
    reactor.listenTCP(PLAYER1_PORT, Player1_ConnFactory())
    reactor.run()
