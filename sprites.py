

import pygame, os, sys, math, random
from globalvars import explosion_speed, GAMEWINDOW
import globalvars
from display import bullets

def load_image(name):
    try:
        imgfile=os.path.join(name)
        return pygame.image.load(imgfile).convert()
    except:
        print( "Failed while loading " + name )

global explosions
explosions=[]
explosions.append(load_image('images/boom1.bmp'))
explosions.append(load_image('images/boom2.bmp'))
explosions.append(load_image('images/boom3.bmp'))
explosions.append(load_image('images/boom4.bmp'))
explosions.append(load_image('images/boom5.bmp'))

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
                bullets.set_bullets(20)

	def get_pos(self):
		return self.rect

	def move(self, x,y):
		self.rect.topleft=(x,y)

	def move_one(self,direction):
		if direction == 1:
			self.rect.move_ip(self.speed,0)
			if not self.in_range(self.rect):
				self.rect.move_ip((-1)*self.speed,0)
		elif direction == 0:
			self.rect.move_ip((-1)*self.speed,0)
			if not self.in_range(self.rect):
				self.rect.move_ip(self.speed,0)

	def in_range(self,rect):
		if GAMEWINDOW.contains(rect):
			return True
		return False

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
                        bullets.sub_bullets(1)
		else:
			print("out of bullets")

	def update(self):
		if self.state > 0:
			self.image=self.player_ship[self.state/explosion_speed]
			self.state+=1
			if self.state >= len(self.player_ship)*explosion_speed:
				self.state=0
				self.image=self.player_ship[0]

class EnemyManager(pygame.sprite.RenderUpdates):
	def __init__(self):
		pygame.sprite.RenderUpdates.__init__(self)
		self.frames=0
		self.transition_speed=5
		self.transition_time=150/self.transition_speed
		self.current_transition=0

	def shoot(self,shotslist):
		self.frames=random.randint(0,globalvars.enemy_bullet_odds)
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

class Enemy(pygame.sprite.Sprite):
	enx=0
	eny=30

	def __init__(self, parent):
		self.parent=parent
		pygame.sprite.Sprite.__init__(self)
		self.enspeed=globalvars.init_enemy_speed
		self.envel=1
		self.en_xmax=globalvars.X_MAX
		self.en_xmin=globalvars.X_MIN
		self.en_state=(-1)*(1)
		self.enemy_ship = (load_image('images/enemy_ship.bmp'))
		self.image=self.enemy_ship
		self.rect = self.image.get_rect()

	def is_wily(self):
		return False

	def set_pos(self, tempx,tempy):
		self.rect.move_ip(tempx,tempy)

	def set_speed(self, speed):
		self.enspeed=speed

	def set_range(self,tempmin,tempmax):
		self.en_xmax=tempmax
		self.en_xmin=tempmin

	def get_range(self):
		return self.en_xmin,self.en_xmax

	def update(self, transition_speed):
		if transition_speed > 0:
			self.rect.bottom+=transition_speed
		elif self.envel <= 0:
			if self.rect.left < self.en_xmax:
				self.rect.right+=self.enspeed
			elif self.rect.left >= self.en_xmax:
				self.envel = 1
		else:
			if self.rect.left > self.en_xmin:
				self.rect.right+=((-1)*self.enspeed)
			elif self.rect.left <= self.en_xmin:
				self.envel = 0
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

class WilyEnemy(pygame.sprite.Sprite):
	enx=0
	eny=30

	def __init__(self, parent):
		self.parent=parent
		pygame.sprite.Sprite.__init__(self)
		self.enxspeed=random.randrange(-25,25)
		self.enyspeed=random.randrange(-25,25)
		self.en_xmax=globalvars.X_MAX
		self.en_xmin=globalvars.X_MIN
		self.en_Y_MAX=globalvars.Y_MAX
		self.en_Y_MIN=globalvars.Y_MIN
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

class EnemyBullet(Bullet):
	def __init__(self, parentlist):
		self.parentlist=parentlist
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('images/enemy_laser.bmp')
		self.rect = self.image.get_rect()
		self.bspeed=globalvars.BULLET_SPEED
		self.health=1

	def update(self):
		self.rect.move_ip(0,(self.bspeed))
		if self.rect.bottom > globalvars.WIN_RESY:
			self.parentlist.remove(self)

class BackgroundManager(pygame.sprite.Sprite):
	stars=[ ]
	last_stars=[ ]

	def __init__(self):
		for x in range(globalvars.init_stars):
			self.add_star()

	def update(self):
		for counter,star in enumerate(self.stars):
			if star.top > globalvars.WIN_RESY:
				del self.stars[counter]
				del self.last_stars[counter]
				self.add_star()
			else:
				self.last_stars[counter].topleft=star.topleft
				star.top+=star.speed

	def draw(self):
		for star in self.stars:
			globalvars.surface.fill(globalvars.star_color,star)
		return self.stars

	def clear(self):
		for star in self.last_stars:
			globalvars.surface.fill(globalvars.bgcolor,star)
		return self.last_stars

	def add_star(self):
		size=random.randint(2,7)
		size1=size
		x=random.randint(0,globalvars.WIN_RESX)
		rect=star(x,0,size,size1)
		rect.set_speed(random.randint(2,globalvars.BG_Speed))
		self.stars.append(rect)
		self.last_stars.append(pygame.Rect(rect))

class star(pygame.Rect):
	def set_speed(self,tspeed):
		self.speed=tspeed
	def get_speed(self):
		return self.speed

global bgstars
bgstars=BackgroundManager()
