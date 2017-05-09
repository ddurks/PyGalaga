import pygame, os, sys, math, random
import globalvars
from display import points

def load_image(name):
    try:
        imgfile=os.path.join(name)
        return pygame.image.load(imgfile).convert()
    except:
        print ("Failed while loading " + name)

class Menu:
	def __init__(self, menulabels):
		self.clear_screen()
		self.font_size=50
		self.offset_x=100
		self.offset_y=300
		self.spacing=20
		self.font = pygame.font.Font(globalvars.defaultfont,self.font_size)
		self.titles = []
		self.rects =[]

		for label in menulabels:
			menulabel=self.font.render(label, 1, globalvars.menucolor)
			menurect=menulabel.get_rect()
			width = menurect.width
			self.offset_x = ((globalvars.WIN_RESX - menurect.width) / 2) - 10

			if not self.titles:
				menurect.move_ip(self.offset_x,self.offset_y)
			else:
				menurect.move_ip(self.offset_x,self.rects[x-1].bottom+self.spacing)
			self.titles.append(menulabel)
			self.rects.append(menurect)

			x=0
			for menulabel in self.titles:
				globalvars.surface.blit(menulabel,self.rects[x])
				x+=1

			logoimage=(load_image('images/pyGalaga.jpeg'))
			logorect=logoimage.get_rect()
			logorect.centerx = 400
			logorect.centery = 150
			globalvars.surface.blit(logoimage,logorect)
			pygame.display.flip()

		selected = -1
		while True:
			events=pygame.event.get()
			selected=self.action(events)
			if selected >= 0:
				if selected == 0:
					break
				if selected == 1:
					sys.exit(0)
			globalvars.CLOCK.tick(globalvars.FPS)

		self.clear_screen()
		pygame.mouse.set_visible(0)
		pygame.event.set_grab(1)

	def action(self, events):
		selected=-1
		pygame.event.pump()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit(0)
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
				if event.key == pygame.K_RETURN:
					selected=0
		return selected

	def clear_screen(self):
		globalvars.surface.fill(globalvars.bgcolor)
		pygame.display.flip()
