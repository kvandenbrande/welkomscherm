import pygame, time, sys, os
import subprocess, shlex
from pygame.locals import *
from background import load_background
from database import get_events
 
pygame.init()

#location check
strs = subprocess.check_output(shlex.split('ip r l'))
gateway = strs.split('default via')[-1].split()[0]
LOCATION = "Antwerpen" #default gateway

if gateway == "10.0.0.249":
    LOCATION = "Antwerpen"
if gateway == "10.1.0.1":
    LOCATION = "Waasland"


#config
STARTUP = pygame.font.SysFont("monospace", 25)
TITLE = pygame.font.SysFont("roboto", 50, bold=True)
WHITE = (255, 255, 255)
WAITTIME = 10   #default time to wait between images (in seconds)
MYSQLSERVER = "10.0.0.205"
THICKNESS = 40
LOCALEPATH = "/home/pi/welkomscherm/img/"

#set up the window, max screensize, fullscreen no frames
modes = pygame.display.list_modes()
screen = pygame.display.set_mode((max(modes)),pygame.NOFRAME)
pygame.mouse.set_visible(False)
x, y = screen.get_size()


#locations
#TV Waasland resolutie 1920x1080 as refence to other resolutions
if x == 1920 and y == 1080:
    L_STARTUP_X= 700
    L_STARTUP_Y= 540
    L_WELCOME_X= 150
    L_WELCOME_Y= 800
    L_LOGO_X= 1150
    L_LOGO_Y= 800
    L_BORDER_AX= 100
    L_BORDER_AY= 100
    L_BORDER_BX= 1400
    L_BORDER_CY= 900
    L_EVENT_X= 150
    L_EVENTN_Y= 300
    L_EVENTT_Y= 500
    L_EVENTL_Y= 700
else:
    L_STARTUP_X= (700*x)/1920
    L_STARTUP_Y= (540*y)/1080
    L_WELCOME_X= (150*x)/1920
    L_WELCOME_Y= (800*y)/1080
    L_LOGO_X= (1150*x)/1920
    L_LOGO_Y= (800*y)/1080
    L_BORDER_AX= (100*x)/1920
    L_BORDER_AY= (100*y)/1080
    L_BORDER_BX= (1400*x)/1920
    L_BORDER_CY= (900*y)/1080
    L_EVENT_X= (150*x)/1920
    L_EVENTN_Y= (300*y)/1080
    L_EVENTT_Y= (500*y)/1080
    L_EVENTL_Y= (700*y)/1080

#startup screen 
label = STARTUP.render("... warming up, please wait ...", 5, (WHITE))
screen.blit(label, (L_STARTUP_X, L_STARTUP_Y))
pygame.display.flip()


#image config
logo = pygame.image.load(LOCALEPATH +'logo.png').convert_alpha()
sms = pygame.image.load(LOCALEPATH +'8876.jpg')
sms = sms.convert()
sms = pygame.transform.scale(sms, max(modes))
event = pygame.image.load(LOCALEPATH +'scherm.jpg')
event = event.convert()
event = pygame.transform.scale(event, max(modes))
partner1 = pygame.image.load(LOCALEPATH +'PP_CORP.jpg')
partner1 = partner1.convert()
partner1 = pygame.transform.scale(partner1, max(modes))
partner2 = pygame.image.load(LOCALEPATH +'PP_BUSIACT.jpg')
partner2 = partner2.convert()
partner2 = pygame.transform.scale(partner2, max(modes))

#run the loop
while True:
    #startscherm
    #tekenen van welkom scherm ipv afbeelding
    screen.fill(load_background())
    pygame.draw.line(screen, WHITE, (L_BORDER_AX-(THICKNESS/2)+1,L_BORDER_AY),(L_BORDER_BX,L_BORDER_AY),THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_AX,L_BORDER_AY),(L_BORDER_AX,L_BORDER_CY),THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_AX-(THICKNESS/2)+1,L_BORDER_CY),(L_BORDER_BX,L_BORDER_CY),THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_BX-(THICKNESS/2),L_BORDER_AY),(L_BORDER_BX-(THICKNESS/2),L_BORDER_CY),THICKNESS)
    #render text
    welcome= TITLE.render("VAN HARTE WELKOM", 5, (WHITE))
    screen.blit(welcome, (L_WELCOME_X, L_WELCOME_Y))
    #add logo
    screen.blit(logo, pygame.rect.Rect(L_LOGO_X,L_LOGO_Y,128,128))
    pygame.display.flip()
    time.sleep(WAITTIME)
    
    #events
    #if check connection to mysql else goto reclame
    #if check event available in mysql else goto reclame
    #for each event teken event scherm
    response = os.system("ping -c 1 " + MYSQLSERVER)
    if response == 0:
        if get_events(LOCATION):
            teller=0
            events,count = get_events(LOCATION)
            while count > 0:
                screen.fill(load_background())
                pygame.draw.line(screen, WHITE, (L_BORDER_AX-(THICKNESS/2)+1,L_BORDER_AY),(L_BORDER_BX,L_BORDER_AY),THICKNESS)
                pygame.draw.line(screen, WHITE, (L_BORDER_AX,L_BORDER_AY),(L_BORDER_AX,L_BORDER_CY),THICKNESS)
                pygame.draw.line(screen, WHITE, (L_BORDER_AX-(THICKNESS/2)+1,L_BORDER_CY),(L_BORDER_BX,L_BORDER_CY),THICKNESS)
                pygame.draw.line(screen, WHITE, (L_BORDER_BX-(THICKNESS/2),L_BORDER_AY),(L_BORDER_BX-(THICKNESS/2),L_BORDER_CY),THICKNESS)
                #render text
                titelevent = TITLE.render(events[teller][0], 5, (WHITE))
                screen.blit(titelevent, (L_EVENT_X, L_EVENTN_Y))
                starttime = TITLE.render(events[teller][1], 5, (WHITE))
                screen.blit(starttime, (L_EVENT_X, L_EVENTT_Y))
                location = TITLE.render(events[teller][2], 5, (WHITE))
                screen.blit(location, (L_EVENT_X, L_EVENTL_Y))
                #add logo
                screen.blit(logo, pygame.rect.Rect(L_LOGO_X,L_LOGO_Y,128,128))
                pygame.display.flip()
                time.sleep(WAITTIME)
                count = count-1
                teller = teller+1
            
    #reclame 8876
    screen.blit(sms,(0,0))
    pygame.display.flip()
    time.sleep(WAITTIME)

    #reclame events
    screen.blit(event,(0,0))
    pygame.display.flip()
    time.sleep(WAITTIME)

    #partners waasland
    if LOCATION == "Waasland":
        screen.blit(partner1,(0,0))
        pygame.display.flip()
        time.sleep(WAITTIME)
        screen.blit(partner2,(0,0))
        pygame.display.flip()
        time.sleep(WAITTIME)
    
    
    pygame.display.update()
