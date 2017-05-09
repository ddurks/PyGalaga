
import pygame, os, sys, math, random
import globalvars
'''
class Points(pygame.sprite.Sprite):
	total_points=0
	temp=0
	pointstr="points:"

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font("freesansbold.ttf", 14)
		self.rect = pygame.Rect(globalvars.points_x, globalvars.points_y, 10, 10)
        	self.textimg=self.font.render(self.pointstr, 0, (128, 128, 128))
		self.textrect=self.textimg.get_rect()
		self.pointsimg=self.font.render(str(self.total_points), 0, (128, 128, 128))
		self.pointsrect=self.pointsimg.get_rect()
		self.pointsrect.move_ip(0,self.textrect.height)
		self.image= pygame.Surface((self.textrect.width,self.pointsrect.height+self.textrect.height))
		pygame.Surface.blit(self.image,self.textimg,self.textrect)
		pygame.Surface.blit(self.image,self.pointsimg,self.pointsrect)
		temp=1

	def add_points(self,points):
		self.total_points+=points
		self.temp=1

	def set_points(self,points):
		self.total_points=points
		self.temp=1

	def get_points(self):
		return self.total_points

	def sub_points(self,points):
		self.total_points-=points
		self.temp=1

	def update(self):
		if self.temp!=0:
			self.image.fill(globalvars.bgcolor,self.pointsrect)
			self.pointsimg=self.font.render(str(self.total_points), 0, (128, 128, 128))
			self.pointsrect=self.pointsimg.get_rect()
			self.pointsrect.move_ip(0,self.textrect.height)
			pygame.Surface.blit(self.image,self.pointsimg,self.pointsrect)
			self.temp=0

	def draw(self):
		text = self.font.render(self.pointstr+str(self.total_points), 0, (128, 128, 128))
		globalvars.surface.fill((0,0,0),self.rect)
    		globalvars.surface.blit(text, (globalvars.points_x,globalvars.points_y))

class Health(pygame.sprite.Sprite):
	total_health=100
	temp=0
	healthstr="health:"

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font("freesansbold.ttf", 14)
		self.rect = pygame.Rect(globalvars.health_x, globalvars.health_y, 10, 20)
		self.textimg=self.font.render(self.healthstr, 0, (128, 128, 128))
		self.textrect=self.textimg.get_rect()
		self.healthimg=self.font.render(str(self.total_health), 0, (128, 128, 128))
		self.healthrect=self.healthimg.get_rect()
		self.healthrect.move_ip(0,self.textrect.height)
		self.image= pygame.Surface((self.textrect.width,self.healthrect.height+self.textrect.height))
		pygame.Surface.blit(self.image,self.textimg,self.textrect)
		pygame.Surface.blit(self.image,self.healthimg,self.healthrect)
		temp=1

	def add_health(self,health):
		self.total_health+=points
		self.temp=1

	def set_health(self,health):
		self.total_health=health
		self.temp=1

	def get_health(self):
		return self.total_health

	def get_temp(self):
		return self.temp

	def get_size(self):
                return pygame.Rect.union(self.healthrect,self.textrect)

	def sub_health(self,health):
		self.total_health=self.total_health-(health)
		self.temp=1

	def hit(self):
		self.sub_health(1)

	def update(self):
		if self.temp!=0:
			self.image.fill(globalvars.bgcolor,self.healthrect)
			self.healthimg=self.font.render(str(self.total_health), 0, (128, 128, 128))
			self.healthrect=self.healthimg.get_rect()
			self.healthrect.move_ip(0,self.textrect.height)
			pygame.Surface.blit(self.image,self.healthimg,self.healthrect)
			self.temp=0


	def draw(self):
		text = self.font.render(str(self.total_health), 0, (128, 128, 128))
		globalvars.surface.fill((0,0,0),self.rect)
    		globalvars.surface.blit(text, (globalvars.points_x,globalvars.points_y))

class BulletNum(pygame.sprite.Sprite):
	total_bullets=0
	temp=0
	bulletstr="bullets:"

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font("freesansbold.ttf", 14)
		self.rect = pygame.Rect(globalvars.bullets_x, globalvars.bullets_y, 10, 10)
		self.textimg=self.font.render(self.bulletstr, 0, (128, 128, 128))
		self.textrect=self.textimg.get_rect()
		self.bulletsimg=self.font.render(str(25), 0, (128, 128, 128))
		self.bulletsrect=self.bulletsimg.get_rect()
		self.bulletsrect.move_ip(0,self.textrect.height)
		self.image= pygame.Surface((self.textrect.width,self.bulletsrect.height+self.textrect.height))
		pygame.Surface.blit(self.image,self.textimg,self.textrect)
		pygame.Surface.blit(self.image,self.bulletsimg,self.bulletsrect)
		temp=1

	def add_bullets(self,bullets):
		self.total_bullets+=bullets
		self.temp=1

	def set_bullets(self,bullets):
		self.total_bullets=bullets
		self.temp=1

	def get_bullets(self):
		return self.total_bullets

	def sub_bullets(self,bullets):
		self.total_bullets-=bullets
		self.temp=1

	def update(self):
		if self.temp!=0:
			self.image.fill(globalvars.bgcolor,self.bulletsrect)
			self.bulletsimg=self.font.render(str(self.total_bullets), 0, (128, 128, 128))
			self.bulletsrect=self.bulletsimg.get_rect()
			self.bulletsrect.move_ip(0,self.textrect.height)
			pygame.Surface.blit(self.image,self.bulletsimg,self.bulletsrect)
			self.temp=0

	def draw(self):
		text = self.font.render(self.bulletstr+str(self.total_bullets), 0, (128, 128, 128))
		globalvars.surface.fill((0,0,0),self.rect)
		globalvars.surface.blit(text, (globalvars.bullets_x,globalvars.bullets_y))

global points
points=Points()
globalvars.SIDE_PANEL.add(points)
global bullets
bullets=BulletNum()
globalvars.SIDE_PANEL.add(bullets)
global health
health=Health()
globalvars.SIDE_PANEL.add(health)
'''
