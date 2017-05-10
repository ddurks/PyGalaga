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

class WilyEnemy(pygame.sprite.Sprite):
	enx=0
	eny=30

	def __init__(self, parent):
		self.parent=parent
		pygame.sprite.Sprite.__init__(self)
		self.enxspeed=random.randrange(-25,25)
		self.enyspeed=random.randrange(-25,25)
		self.en_xmax=WIN_RESX
		self.en_xmin=0
		self.en_Y_MAX=WIN_RESY-100
		self.en_Y_MIN=0
		self.en_state=-1
		self.wily_ship = (load_image('images/wily_ship.bmp'))
		self.image= self.wily_ship
		self.rect = self.image.get_rect()
		self.step = 0
		self.threshold = random.randrange(25,75)

	def is_wily(self):
		return True

	def set_pos(self):
		self.rect.move_ip(random.randrange(self.en_xmin,self.en_xmax),random.randrange(self.en_Y_MIN,self.en_Y_MAX-150))

	def set_speed(self, speed):
		self.enspeed=speed

	def get_range(self):
		return self.en_xmin,self.en_xmax

	def update(self):
		if self.step >= self.threshold:
			self.enxspeed = random.randrange(-25,25)
			self.enyspeed = random.randrange(-25,25)
			self.step = 0
			self.threshold = random.randrange(25,75)
		self.step += 1

		if (self.rect.x <0) or (self.rect.x > self.en_xmax):
			self.enxspeed *= -1
		if (self.rect.y<0) or (self.rect.y > self.en_Y_MAX-150):
			self.enyspeed *= -1

		self.rect.move_ip(self.enxspeed, self.enyspeed)
		self.next_state()

	def set_state(self, varr):
		self.en_state=varr

	def next_state(self):
		if self.en_state>=0 and self.en_state<5:
			self.image=explosions[self.en_state]
			self.en_state+=1
		elif self.en_state>4:
			self.parent.remove(self)

	def get_state(self):
		return self.en_state

	def shoot(self,shotslist):
		tempb=EnemyBullet(shotslist)
		tempb.set_pos(self.rect.left+self.rect.width/2,self.rect.bottom)
		shotslist.add(tempb)

class EnemyManager(pygame.sprite.RenderUpdates):
	def __init__(self):
		pygame.sprite.RenderUpdates.__init__(self)
		self.frames=0
		self.transition_speed=5
		self.transition_time=150/self.transition_speed
		self.current_transition=0

	def shoot(self,shotslist):
		self.frames=random.randint(0,15)
		if self.frames < len(self):
			self.sprites()[self.frames].shoot(shotslist)

	def update(self):
		if self.current_transition<self.transition_time:
			for e in self:
				if(e.is_wily() == True):
					e.update()
				else:
					e.update(self.transition_speed)
			self.current_transition+=1
		else:
			for e in self:
				if(e.is_wily() == True):
					e.update()
				else:
					e.update(0)

class Bullet(pygame.sprite.Sprite):

	def __init__(self, parentlist):
		self.parentlist=parentlist
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('images/player_laser.bmp')
		self.rect = self.image.get_rect()
		self.bspeed=10
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
		self.enemies = EnemyManager()
		self.bulletlist = []
		self.enemylist = []
		self.gs = pygame.display.get_surface()
		self.s = pygame.Surface((WIN_RESX,WIN_RESY))

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

		#draw players
		self.screen.blit(self.background, self.bgrect)
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)
		#draw bullets
		self.bullets1.clear(self.screen, self.background)
		self.bullets2.clear(self.screen, self.background)
		self.bulletlist+=self.bullets1.draw(self.screen)
		self.bulletlist+=self.bullets2.draw(self.screen)
		#draw enemies
		try:

			print(self.enemylist)
			if not self.enemies:
				for _ in range(5):
					print("making enemies")
					wily = WilyEnemy(self.enemies)
					wily.set_pos()
					self.enemies.add(wily)
			self.enemies.clear(self.screen, self.background)
			self.enemylist+=self.enemies.draw(self.screen)
		except Exception as e:
			print(e)

		self.bulletlist.update()
		self.enemies.update()
		pygame.display.update(self.bulletlist)
		pygame.display.update(self.enemylist)
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
