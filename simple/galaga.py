import pygame, os, sys, math, random
from twisted.internet import reactor

global WIN_RESX, WIN_RESY
WIN_RESX=800
WIN_RESY=600

global CLOCK
CLOCK = pygame.time.Clock()

def load_image(name):
	try:
		imgfile=name
		return pygame.image.load(imgfile).convert()
	except:
		print( "Failed while loading " + name )

class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.player_ship = []
		self.player_ship.append(load_image('images/player_ship.bmp'))
		self.player_ship.append(load_image('images/player_ship1.bmp'))
		self.player_ship.append(load_image('images/player_ship2.bmp'))
		self.player_ship.append(load_image('images/player_ship3.bmp'))

		self.image= self.player_ship[0]
		self.rect = self.image.get_rect()
		self.state=0
		self.speed=10
		self.bullets=20

	def get_pos(self):
		return self.rect

	def move(self, x,y):
		self.rect.topleft=(x,y)

	def move_one(self,direction):
		if direction == 1:
			if self.rect.right <= WIN_RESX:
				self.rect.move_ip(self.speed,0)

		elif direction == 0:
			if self.rect.left >= 0:
				self.rect.move_ip((-1)*self.speed,0)


	def set_pos(self, tempx,tempy):
		self.rect.move_ip(tempx,tempy)

	def set_hit(self):
		self.state=1

	def shoot(self,shotslist,locx,locy):
		if(self.bullets > 0):
			self.boom=Bullet(shotslist)
			self.boom.set_pos(locx,locy)
			shotslist.add(self.boom)
			self.bullets -= 1
						#bullets.sub_bullets(1)
		else:
			print("out of bullets")

	def update(self):
		if self.state > 0:
			self.image=self.player_ship[self.state/explosion_speed]
			self.state+=1
			if self.state >= len(self.player_ship)*explosion_speed:
				self.state=0
				self.image=self.player_ship[0]

class Bullet(pygame.sprite.Sprite):

	def __init__(self, parentlist):
		self.parentlist=parentlist
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('images/player_laser.bmp')
		self.rect = self.image.get_rect()
		self.bspeed=globalvars.BULLET_SPEED
		self.health=1

	def set_pos(self, tempx,tempy):
		self.rect.move_ip(tempx,tempy)

	def set_hit(self):
		self.health-=1

	def set_speed(self, speed):
		self.bspeed=speed

	def update(self):
		self.rect.move_ip(0,-1*(self.bspeed))
		if self.rect.bottom <= 0 or self.health <= 0:
			self.parentlist.remove(self)

class Galaga:
	def __init__(self, playerNum):
		self.isPlayer1 = False
		if playerNum == 1:
			self.isPlayer1 = True
		pygame.init()
		self.screen = pygame.display.set_mode ((WIN_RESX, WIN_RESY))
		self.background = load_image("images/stars.bmp")
		self.bgrect = self.background.get_rect()
		pygame.display.set_caption("PyGalaga")
		self.screen.fill((0,0,0))
		self.player1=Player()
		self.player2=Player()
		self.player1.set_pos(400,550)
		self.player2.set_pos(400,550)
		self.bullets1 = pygame.sprite.RenderUpdates()
		self.bullets2 = pygame.sprite.RenderUpdates()
		self.bulletlist = []

		pygame.key.set_repeat(1,30)

	def tick(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				reactor.stop()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit(0)
				if event.key == pygame.K_p:
					sys.exit(0)
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
				if event.key == 276 or event.key == 275 or event.key == 32:
					self.sendData(event.key)

		self.screen.blit(self.background, self.bgrect)
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)
		self.bullets1.clear(self.screen, self.background)
		self.bullets2.clear(self.screen, self.background)
		self.bulletlist+=self.bullets1.draw(self.screen, self.background)
		self.bulletlist+=self.bullets2.draw(self.screen, self.background)

		pygame.display.update(self.bulletlist)
		pygame.display.flip()

	def sendData(self, keyNum):
		if self.isPlayer1:
			self.outgoingConn.transport.write("1:" + str(keyNum))
		else:
			self.outgoingConn.transport.write("2:" + str(keyNum))

	def transferConnectionObject(self, obj):
		self.outgoingConn = obj

	def handleData(self, data):
		if data['p1Ship_l'] == '1':
			self.player1.move_one(0)
		elif data['p1Ship_r'] == '1':
			self.player1.move_one(1)
		if data['p2Ship_l'] == '1':
			self.player2.move_one(0)
		elif data['p2Ship_r'] == '1':
			self.player2.move_one(1)
		if data['p1Shot'] == '1':
			self.player1.shoot(self.bullets1, self.player1.rect.centerx, self.player1.rect.top)
		elif data['p2Shot'] == '1':
			self.player2.shoot(self.bullets2, self.player2.rect.centerx, self.player2.rect.top)


if __name__ == "__main__":
	game=Galaga(1)
