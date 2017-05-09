
import pygame, os, sys, math, random
from pygame.locals import*
import globalvars
from sprites import Player, Enemy, WilyEnemy, EnemyManager, Bullet, EnemyBullet, bgstars
from display import *
from menu import Menu
from display import points, bullets
from twisted.internet import reactor

class Galaga:
	def __init__(self, player=0):
		self.isPlayer1 = False
		if player == 1:
			self.isPlayer1 = True
		globalvars.frames = 0
		self.lagcount=0
		self.enemy_list=[]
		self.list_enemies=EnemyManager()
		self.level=level(self.list_enemies,globalvars.PLAYERS)
		self.ally_bullets=pygame.sprite.RenderUpdates()
		self.enemy_bullets=pygame.sprite.RenderUpdates()

	def start(self):
		self.clear()
		self.player1=Player()
		self.player2=Player()
		globalvars.PLAYERS.add(self.player1)
		globalvars.PLAYERS.add(self.player2)
		self.player1.set_pos(globalvars.x,globalvars.y)
		self.player2.set_pos(globalvars.x,globalvars.y)
		self.loop()

	def clear(self):
		self.leftkeydown=0
		self.rightkeydown=0
		health.set_health(globalvars.max_health)
		points.set_points(0)
		globalvars.x=400
		globalvars.y=globalvars.WIN_RESY-60
		self.level.set_level(-1) #hax
		globalvars.enemy_bullet_odds=100
		self.list_enemies.empty()
		self.ally_bullets.empty()
		globalvars.PLAYERS.empty()
		self.enemy_bullets.empty()
		print ("Restart")

	def player_move(self, x,y):
		globalvars.PLAYERS.clear(globalvars.surface,globalvars.screen)
		self.enemy_list+=globalvars.PLAYERS.draw(globalvars.surface)

	def enemy_move(self):
		self.list_enemies.clear(globalvars.surface, globalvars.screen)
		self.enemy_list+=self.list_enemies.draw(globalvars.surface)

	def draw_enemies(self):
		for _ in range(self.level.get_levelnum()):
			wily = WilyEnemy(self.list_enemies)
			wily.set_pos()
			self.list_enemies.add(wily)

		for enemycol in range(self.level.get_level()[0]):
			for enemyrow in range(self.level.get_level()[1]):
				tempenemy=Enemy(self.list_enemies)
				tempenemy.set_pos(globalvars.X_MIN+enemycol*(globalvars.enemy_width+globalvars.enemy_spacing_x),globalvars.Y_MIN+enemyrow*(globalvars.enemy_height+globalvars.enemy_spacing_y)-150)
				tempenemy.set_range(globalvars.X_MIN+enemycol*(globalvars.enemy_width+globalvars.enemy_spacing_x),globalvars.X_MAX-(self.level.get_level()[0]-enemycol)*(globalvars.enemy_height+globalvars.enemy_spacing_x))
				self.list_enemies.add(tempenemy)

	def check_collision(self):
		todie=pygame.sprite.groupcollide(self.list_enemies, self.ally_bullets,0,0)
		for enemy,bullet in todie.iteritems():
			self.ally_bullets.remove(bullet)
			enemy.set_state(0)
			points.add_points(1)
			self.player1.bullets += 5
			bullets.add_bullets(5)
		if pygame.sprite.spritecollideany(self.player1, self.enemy_bullets):
			self.player1.set_hit()
			health.hit()

	def check_over(self):
		if not self.list_enemies:
			self.level.next_level()
			self.draw_enemies()
			self.player1.bullets += 10
			bullets.add_bullets(10)

	def check_rows(self):
		if globalvars.frames % 20==0:
			highest=globalvars.X_MIN
			lowest=globalvars.X_MAX
			for enemy in self.list_enemies:
				if enemy.get_range()[1] > highest:
					highest=enemy.get_range()[1]
				if enemy.get_range()[0] < lowest:
					lowest=enemy.get_range()[0]
			highest=globalvars.X_MAX-highest
			lowest=lowest-globalvars.X_MIN
			if highest != 0 or lowest != 0:
				for enemy in self.list_enemies:
					e_range=enemy.get_range()
					enemy.set_range(e_range[0]-lowest,e_range[1]+highest)

	def again(self):
				if health.get_health() <= 0:
						return False
				return True

	def pshoot(self, sx, sy):
		self.player1.shoot(self.ally_bullets,sx,sy)

	def drawbullets(self):
		self.ally_bullets.clear(globalvars.surface,globalvars.screen)
		self.enemy_bullets.clear(globalvars.surface,globalvars.screen)
		self.enemy_list+=self.ally_bullets.draw(globalvars.surface)
		self.enemy_list+=self.enemy_bullets.draw(globalvars.surface)

	def draw_stats(self):
		if globalvars.frames%5==0:
			globalvars.SIDE_PANEL.update()
		globalvars.SIDE_PANEL.clear(globalvars.surface,globalvars.screen)
		self.enemy_list+=globalvars.SIDE_PANEL.draw(globalvars.surface)

	def check(self):
		self.check_over()
		self.check_collision()
		self.check_rows()
		bgstars.update()
		self.list_enemies.shoot(self.enemy_bullets)
		self.player1.update()
		self.player2.update()
		#print(self.player.bullets)

	def draw(self):
		self.enemy_list+=bgstars.draw()
		self.enemy_list+=bgstars.clear()
		self.drawbullets()
		self.player_move(globalvars.x,globalvars.y)
		self.enemy_move()
		self.draw_stats()

	def clear_screen(self):
		globalvars.surface.fill(globalvars.bgcolor)
		pygame.display.flip()

	def tick(self):

		pygame.event.pump()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				reactor.stop()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit(0)
				if event.key == pygame.K_p:
					Menu(("Press Enter To Continue", "Press Q or esc to Quit"))
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
				if event.key == 276 or event.key == 275 or event.key == 32:
					self.sendData(event.key)

		self.ally_bullets.update()
		self.list_enemies.update()
		self.enemy_bullets.update()

		pygame.event.clear()

	def loop(self):
		while self.again():

			if globalvars.frames>=globalvars.REFRESH_TIME:
				globalvars.frames=0
			globalvars.frames+=1

			self.check()

			self.draw()

			self.tick()

			pygame.display.update(self.enemy_list)
			self.enemy_list=[]

			timeittook=globalvars.CLOCK.tick(globalvars.FPS)

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

class level:
	enemy_levels=[(4,2),(5,3),(6,4)]
	current_level=0

	def __init__(self,enemymanager,playermanager):
		self.enemymanager=enemymanager
		self.playermanager=playermanager

	def next_level(self):
		if len(self.enemy_levels) > self.current_level+1:
			self.current_level+=1
		if globalvars.enemy_bullet_odds > 15:
			globalvars.enemy_bullet_odds-=15
		self.enemymanager.current_transition=0

	def set_level(self, level):
		self.current_level=level

	def get_level(self):
		return self.enemy_levels[self.current_level]

	def get_levelnum(self):
		return self.current_level + 1

if __name__ == "__main__":
	game=Galaga()
	Menu(("Press Enter To Begin", "Press Q or esc to Exit"))

	game.start()
	while Menu(("Score: %s"%points.get_points(),"Press Enter to Return to Main")):
		Menu(("Press Enter To Begin", "Press Q or esc to Exit"))
		game.start()
