import pygame     #library for Keyboard input and output Window
import time       #library for time in sec

from pyfirmata import Arduino, util     #pyfirmata for communication with Arduino
board = Arduino('/dev/ttyACM0')         #Arduino board connected to Pi over USB. Port Arduino is connected to
speed = board.digital[12]               #PinMode(12, Output)
steering = board.get_pin('d:6:s')       #d= digitalPin; 6= Pin6; s=Servo Output

pygame.init()     # initalisierung of pygame. Needed at Programm start
x_max = 400       #size of Window
y_max = 400

screen = pygame.display.set_mode([x_max, y_max])     #generate the display
clock = pygame.time.Clock()
screen.fill([255, 255, 255])                         #set background white color
stil = pygame.font.SysFont("Tahoma", 25, False, False) #set font

Quit = False     #set to True, when Program will be Quit
count = 0
out_string = "Program Startet:"    #Ausgabe

while not Quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     #Rotes Kreuz oben rechts beendet das Programm
            Quit = True

        elif event.type == pygame.KEYDOWN:     #event Key pressed down
            if event.key == pygame.K_w:        #Key "W"
                out_string = "Forward"         #Output
                speed.write(1)                 #Write Pin 12 to HIGH      
                count+=1                       #count + 1 to write Text in new line
            if event.key == pygame.K_s:
                out_string = "Backward"
#                speed.write(1)
                count+=1
            if event.key == pygame.K_a:
                out_string = "Left"
                steering.write(40)
                count+=1
            if event.key == pygame.K_d:
                out_string = "Right"
                steering.write(150)
                count+=1
        elif event.type == pygame.KEYUP:            #event Key released
            if event.key == pygame.K_w:
                out_string = "Forward losgelassen"
                speed.write(0)
                count+=1
            if event.key == pygame.K_s:
                out_string = "Backward losgelassen"
#                speed.write(1)
                count+=1
            if event.key == pygame.K_a:
                out_string = "Left losgelassen"
                steering.write(90)
                count+=1
            if event.key == pygame.K_d:
                out_string = "Right losgelassen"
                steering.write(90)
                count+=1

            
    text_bild = stil.render (out_string, True, [0, 0, 0])     #print out_string = Text ausgabe
    screen.blit(text_bild, [25, 25+count*25])                 #new text print 25pixel down
    
    if count >= 14:                   #clear Window by over write with white color
        screen.fill([255, 255, 255])
        count = 0
    
    pygame.display.flip()        #refresh Window
    clock.tick(30)               #frame rate 30Fps 
    
pygame.quit()             #Quit Program
