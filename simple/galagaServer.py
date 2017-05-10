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
        self.p1Shot = '0'
        self.p2Shot = '0'
        self.startGame = '0'

    def getPlayer1_Connection(self, p1CONN):
        self.player1_Conn = p1CONN

    def getPlayer2_Connection(self, p2CONN):
        self.player2_Conn = p2CONN

    def decode_data(self, data):

        self.p1SHIP_l = '0'
        self.p1SHIP_r = '0'
        self.p2SHIP_l = '0'
        self.p2SHIP_r = '0'
        self.p1Shot = '0'
        self.p2Shot ='0'
        self.startGame = '0'


        dataList = data.split(":")
        if dataList[1] == '-1':
            return
        if dataList[0] == '1':
            if dataList[1] == '275': # RIGHT
                self.p1SHIP_r = '1'
            elif dataList[1] == '276': # LEFT
                self.p1SHIP_l = '1'
            elif dataList[1] == '32':
                self.p1Shot = '1'

        elif dataList[0] == '2':

            if dataList[1] == '275': # RIGHT
                self.p2SHIP_r = '1'
            elif dataList[1] == '276': # LEFT
                self.p2SHIP_l = '1'
            elif dataList[1] == '32':
                self.p2Shot = '1'
            elif dataList[1] == '0':
                print('ready to start')
                self.startGame = '1'

        else:
            print "Error: unexpected data sent from Player"


        return_string = json.dumps({
                                    'p1Ship_l':self.p1SHIP_l,
                                    'p1Ship_r':self.p1SHIP_r,
                                    'p2Ship_l':self.p2SHIP_l,
                                    'p2Ship_r':self.p2SHIP_r,
                                    'p1Shot':self.p1Shot,
                                    'p2Shot':self.p2Shot
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
        string = json.dumps({'start':'1'})
        self.sendData(string)

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
