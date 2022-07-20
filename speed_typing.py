import pygame
from pygame.locals import *
import sys
import time
import random
import mysql.connector

class Game:
   
    def __init__(self):
        self.w=950
        self.h=700
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (57, 96, 204)
        self.TEXT_C = (0,0,0)
        self.RESULT_C = (255,70,70)
        self.BLACK = (255,255,255)
        
       
        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))


        self.bg = pygame.image.load('background.png')
        self.bg = pygame.transform.scale(self.bg, (950,700))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')
        
        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Typing Test')
        
        
        
    def reset_game(self):
    	self.screen.blit(self.open_img, (0,0))
    	pygame.display.update()
    	time.sleep(1)
    	
    	self.reset=False
    	self.end=False
    	
    	self.input_text=''
    	self.word = ''
    	self.time_start = 0
    	self.total_time = 0
    	self.wpm = 0
    	
    	pygame.draw.rect(self.screen,(255,192,25), (150,250,350,50), 2)
    	self.word = self.get_sentence()
    	if (not self.word): self.reset_game()
    	self.screen.fill((0,0,0))
    	self.screen.blit(self.bg,(0,0))
    	msg = "Typing Speed Test"
    	self.draw_text(self.screen, msg,90, 90,self.HEAD_C)
    	pygame.draw.rect(self.screen,(255,192,25), (150,300,650,50), 2)
    	self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)
    	pygame.display.update()
        
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update() 
    
    def draw_left(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/3.3, y))
        screen.blit(text, text_rect)
        pygame.display.update()  
    
    def draw_right(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(650, y))
        screen.blit(text, text_rect)
        pygame.display.update()   
        
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence
    
    def insert1(self, T, A, W):
    	mydb = mysql.connector.connect(
    		host="localhost",
    		user="root",
    		password="khadde",
    		database="Typing"
    	)
    	mycursor = mydb.cursor()
    	Text=""
    	sql = "INSERT INTO Data (Time, Accuracy, WPM) VALUES (%s, %s, %s)"
    	val = (T,A,W)
    	mycursor.execute(sql, val)
    	mydb.commit()
	
    def get(self):
    	a = []
    	mydb = mysql.connector.connect(
    	  host="localhost",
    	  user="root",
    	  password="khadde",
    	  database="Typing"
    	  )
    	mycursor = mydb.cursor()
    	mycursor.execute("SELECT Time, Accuracy, WPM FROM Data ORDER BY id DESC")
    	myresult = mycursor.fetchall()
    	for x in myresult:
    		a += [x]
    	return a

    def show_results(self, screen):
        if(not self.end):
            #Calculate time
            self.total_time = time.time() - self.time_start
               
            #Calculate accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100
           
            #Calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
                
            self.results = 'Time:'+str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))
            self.insert1(self.total_time, self.accuracy, self.wpm)
            
	    #database connectivity
	    
            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150,150))
            #screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w/2-75,self.h-140))
            self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))
            
            print(self.results)
            
            pygame.display.update()
            
    def button(self, screen):
    	button = pygame.Rect(400, 400, 150, 50)
    	button1 = pygame.Rect(400,600,150,50)
    	count = 0
    	pygame.draw.rect(self.screen, [255, 0, 0], button)
    	msg = "show statistics"
    	self.draw_text(self.screen, msg, 425, 26,self.TEXT_C)
    	while True :
    		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
    				return False
    			if event.type == pygame.MOUSEBUTTONDOWN:
    				mouse_pos = event.pos
    				if button.collidepoint(mouse_pos):
    					self.Statistics(self)
    					count += 1
    					if(count > 1):
    						Game().run()
    				if button1.collidepoint(mouse_pos):
    					Game().run()

    def button1(self, screen):
    	button1 = pygame.Rect(400, 600, 150, 100)
    	while True :
    		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
    				return False
    			if event.type == pygame.MOUSEBUTTONDOWN:
    				mouse_pos1 = event.pos
    				if button1.collidepoint(mouse_pos1):
    					Game().run()
    						
    
    def Statistics(self, screen):
    	self.screen.blit(self.bg, (0,0))
    	msg = "Database"
    	self.draw_text(self.screen, msg,90, 45,self.HEAD_C)
    	
    	msg="Time"
    	pygame.draw.rect(self.screen,self.HEAD_C, (200,120,175,40), 2)
    	self.draw_left(self.screen, msg, 140, 26,self.TEXT_C)
    	
    	msg="Accuracy"
    	pygame.draw.rect(self.screen,self.HEAD_C, (373,120,175,40), 2)
    	self.draw_text(self.screen, msg, 140, 26,self.TEXT_C)
    	
    	msg="Wpm"
    	pygame.draw.rect(self.screen,self.HEAD_C, (546,120,175,40), 2)
    	self.draw_right(self.screen, msg, 140, 26,self.TEXT_C)
    	
    	a = self.get()
    	c=158
    	for i in range(5):
    		d=c+20
    		msg = str(a[i][0])
    		msg = msg+" sec"
    		pygame.draw.rect(self.screen,self.HEAD_C, (200,c,175,40), 2)
    		self.draw_left(self.screen, msg, d, 26,self.TEXT_C)
    		msg = str(a[i][1])
    		msg = msg+" %"
    		pygame.draw.rect(self.screen,self.HEAD_C, (373,c,175,40), 2)
    		self.draw_text(self.screen, msg, d, 26,self.TEXT_C)
    		msg = str(a[i][2])
    		pygame.draw.rect(self.screen,self.HEAD_C, (546,c,175,40), 2)
    		self.draw_right(self.screen, msg, d, 26,self.TEXT_C)
    		c=c+38
    		
    	self.time_img = pygame.image.load('icon.png')
    	self.time_img = pygame.transform.scale(self.time_img, (150,150))
    	self.screen.blit(self.time_img, (400,370))
    	self.draw_text(self.screen,"Reset",440, 26, (100,100,100))
        
    	pygame.display.update()
		
    def run(self):
        self.reset_game()
    
       
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            pygame.draw.rect(self.screen,self.HEAD_C, (150,150,650,100), 2)
            
            self.screen.fill((0,0,0), (150,300,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (150,300,650,50), 2)
            

            self.draw_text(self.screen, self.input_text, 325, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=100 and x<=650 and y>=300 and y<=400):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # position of reset box
                    if(x>=300 and x<=500 and y>=500 and self.end):
                    	print('button was pressed at {0}'.format(mouse_pos))
                    	self.reset_game()
                    	x,y = pygame.mouse.get_pos()
        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 500, 28, self.RESULT_C)
                            print(self.button)
                            self.button(self.screen)
                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()

Game().run()

