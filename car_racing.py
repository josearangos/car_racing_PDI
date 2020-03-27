import pygame
import time
import random
import cv2
import numpy as np

camera = cv2.VideoCapture(-1)

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)

car_width = 50
car_height = 100
#start_music = pygame.mixer.Sound("Hurry_Up.mp3")
pygame.mixer.music.load("assets/Hurry_Up.mp3")
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

carImg = pygame.image.load("assets/car3.png") #load the car image
car2Img = pygame.image.load("assets/car2.png")
bgImg = pygame.image.load("assets/back2.jpg")
bgImg2 = pygame.image.load("assets/back3.jpg")
crash_img = pygame.image.load("assets/crash.png")
def intro():
	#pygame.mixr.Sound.play(start_music)
	intro = True
	menu1_x = 200
	menu1_y = 400
	menu2_x = 500
	menu2_y = 400
	menu_width = 100
	menu_height = 50
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		pygame.display.set_icon(carImg)
		
		pygame.draw.rect(gameDisplay,black,(200,400,100,50))
		pygame.draw.rect(gameDisplay,black,(500,400,100,50))
			
		gameDisplay.fill(white)
		message_display("CAR RACING",100,display_width/2,display_height/2)
		gameDisplay.blit(carImg,((display_width/2)-100,10))	
		pygame.draw.rect(gameDisplay,green,(200,400,100,50))
		pygame.draw.rect(gameDisplay,red,(500,400,100,50))
		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		
		if menu1_x < mouse[0] < menu1_x+menu_width and menu1_y < mouse[1] < menu1_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(200,400,100,50))
			if click[0] == 1:
				intro = False
		if menu2_x < mouse[0] < menu2_x+menu_width and menu2_y < mouse[1] < menu2_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(500,400,100,50))
			if click[0] == 1:
				pygame.quit()
				quit()
	
		message_display("Go",40,menu1_x+menu_width/2,menu1_y+menu_height/2)
		message_display("Exit",40,menu2_x+menu_width/2,menu2_y+menu_height/2)




		pygame.display.update()
		clock.tick(50)

#This function update the score
def highscore(count):
	font = pygame.font.SysFont(None,60)
	text = font.render("Score : "+str(count),True,black)
	gameDisplay.blit(text,(0,0))

def try_again_counter(count,score):
	#Try Again Timer
	font = pygame.font.SysFont(None,250)
	text = font.render(str(count),True,black)
	gameDisplay.blit(text,(350,250))

	#Final Score
	font = pygame.font.SysFont(None,115)
	text = font.render("Score : "+str(score),True,black)
	gameDisplay.blit(text,(165,170))
	
#This function print obstacle cars
def draw_things(thingx,thingy,thing):
	gameDisplay.blit(thing,(thingx,thingy))
	
#This function print our car
def car(x,y):
	gameDisplay.blit(carImg,(x,y))

#this function make the rectangles for buttons from initial menu
def text_objects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface,textSurface.get_rect()
	
#This functio print buttons
def message_display(text,size,x,y):
	font = pygame.font.Font("assets/CaviarDreams.ttf",size)
	text_surface , text_rectangle = text_objects(text,font)
	text_rectangle.center =(x,y)
	gameDisplay.blit(text_surface,text_rectangle)
	
	
	
	
def crash(x,y,score):
	reset = 3
	#Stop Music
	pygame.mixer.music.stop()

	#this put the crach img in the cash car position
	gameDisplay.blit(crash_img,(x,y))

	#Put Message, update display, and wait 
	message_display("You Crashed",115,display_width/2,display_height/2)
	pygame.display.update()
	time.sleep(3)

	while reset > -1:
		gameDisplay.fill(white)
		try_again_counter(reset,score)
		time.sleep(1)
		reset-=1
		pygame.display.update()
	intro()
	gameloop() #for restart the game
	
def gameloop():
	#pygame.mixer.Sound.stop()
	#pygame.mixer.music.play(-1)
	bg_x1 = 0
	bg_x2 = 0
	bg_y1 = 0
	bg_y2 = -600
	bg_speed = 6
	bg_speed_change = 0
	car_x = ((display_width / 2) - (car_width / 2))
	car_y = (display_height - car_height)
	car_x_change = 0
	road_start_x =  (display_width/2)-112
	road_end_x = (display_width/2)+112
	
	thing_startx = random.randrange(road_start_x,road_end_x-car_width)
	thing_starty = -600
	thingw = 50
	thingh = 100
	thing_speed = 3
	count=0
	gameExit = False
	
	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
				pygame.quit()
				quit()
			
			if event.type == pygame.KEYDOWN:
				#Here we can put the camera results
				if event.key == pygame.K_LEFT:
					car_x_change = -1.5
				elif event.key == pygame.K_RIGHT:
					car_x_change = 1.5
				
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					car_x_change = 0
			
			
		car_x+=car_x_change
		
		if car_x > road_end_x-car_width:
			crash(car_x,car_y,count)
		if car_x < road_start_x:
			crash(car_x-car_width,car_y,count)
		
		
		if car_y < thing_starty + thingh-25:
			if car_x >= thing_startx+10 and car_x <= thing_startx+thingw-10:
				#Left Crash
				crash(car_x-25,car_y-car_height/2,count)
			if car_x+car_width >= thing_startx-10 and car_x+car_width <= thing_startx+thingw+10:
			 	#Right Crash
			 	crash(car_x,car_y-car_height/2,count)


				
		gameDisplay.blit(bgImg,(bg_x1,bg_y1))
		gameDisplay.blit(bgImg2,(bg_x2,bg_y2))


		car(car_x,car_y) #display car
		draw_things(thing_startx,thing_starty,car2Img)
		highscore(count)
		count+=1

		#Update Speed Obstacle Cars
		thing_speed += 0.003
		thing_starty += thing_speed
		
		if thing_starty > display_height:
			thing_startx = random.randrange(road_start_x,road_end_x-car_width)
			thing_starty = -200
			
		bg_y1 += bg_speed
		bg_y2 += bg_speed
		
		if bg_y1 >= display_height:
			bg_y1 = -600
			
		if bg_y2 >= display_height:
			bg_y2 = -600



		pygame.display.update() # update the screen
		clock.tick(128) # frame per sec

intro()

gameloop()	

#this is not yet completed there are many changes required to improve this game
#By_Sumit_Patidar
