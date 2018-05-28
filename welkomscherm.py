#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import time
import sys
import os
import subprocess
import json
from subprocess import Popen
from pygame.locals import *
from colors import *
from database import get_events
from database import get_agenda
##from mpd import MPDClient

pygame.init()

# location check
try:
    with open('/home/pi/Desktop/welkomscherm_conf.json', 'r') as f:
        config = json.load(f)
except ValueError:
     print 'Error: Decoding config has failed'

LOCATION = config['LOCATION']['vestiging']
LOCATION_DETAIL = config['LOCATION']['locatie']

# config
try:
    with open("./online.tmp", "w") as processid:
        processid.write(str(os.getpid()))
except IOError:
    print "Error: online.tmp cannot be made."

# media files
LOCALEPATHIMAGE = '/home/pi/welkomscherm/img/'
LOCALEPATHFONT = '/home/pi/welkomscherm/font/'
MOVIE = '/home/pi/Desktop/jaaroverzicht.mp4'
STREAM = "http://lb.zenfm.be/zenfm.mp3"

STARTUP = pygame.font.Font(LOCALEPATHFONT + 'Rubik-Regular.ttf', 25)
TEXT = pygame.font.Font(LOCALEPATHFONT + 'Rubik-Regular.ttf', 35, bold=True)
TITLE = pygame.font.Font(LOCALEPATHFONT + 'Rubik-Regular.ttf', 40, bold=True)
TITLE2 = pygame.font.Font(LOCALEPATHFONT + 'Rubik-Bold.ttf', 50, bold=True)
TITLE1 = pygame.font.Font(LOCALEPATHFONT + 'Rubik-Bold.ttf', 75, bold=True)
WHITE = (255, 255, 255)
WAITTIME = 10  # default time to wait between images (in seconds)
THICKNESS = 40


# set up the window, max screensize, fullscreen no frames

modes = pygame.display.list_modes()
screen = pygame.display.set_mode(max(modes), pygame.NOFRAME)
pygame.mouse.set_visible(False)
(x, y) = screen.get_size()

# locations
# TV Waasland resolutie 1920x1080 as refence to other resolutions

L_STARTUP_X = 700 * x / 1920
L_STARTUP_Y = 540 * y / 1080
L_WELCOME_X = 100 * x / 1920
L_WELCOME_Y = 800 * y / 1080
L_LOGO_X = 100 * x / 1920
L_LOGO_Y = 250 * y / 1080
L_EVENT_X = 100 * x / 1920
L_EVENTN_Y = 300 * y / 1080
L_EVENTT_Y = 500 * y / 1080
L_EVENTL_Y = 700 * y / 1080
L_KA_TITEL_X = 100 * x / 1920
L_KA_TITEL_Y = 100 * y / 1080
L_KA_ED_X = 100 * x / 1920  # horizontaal afstand voor kameragenda datum
L_KA_ET_X = 100 * x / 1920  # horizontaal afstand voor kameragenda event
L_KA_3_E1_Y = 300 * y / 1080
L_KA_3_E2_Y = 500 * y / 1080
L_KA_3_E3_Y = 700 * y / 1080
L_KA_2_E1_Y = 500 * y / 1080
L_KA_2_E2_Y = 800 * y / 1080
L_KA_1_E1_Y = 500 * y / 1080
L_KA_3_T1_Y = 375 * y / 1080
L_KA_3_T2_Y = 575 * y / 1080
L_KA_3_T3_Y = 775 * y / 1080
L_KA_2_T1_Y = 575 * y / 1080
L_KA_2_T2_Y = 875 * y / 1080
L_KA_1_T1_Y = 575 * y / 1080
L_RIGHT_X = 1252 * x / 1920       # positie rechtse afbeelding
L_RIGHT_Y = 0                     # positie rechtse afbeelding
L_SCALE_RIGHT_X = 668 * x / 1920  # schalen van rechtse afbeelding
L_SCALE_RIGHT_Y = y               # schalen van rechtse afbeelding

# startup screen

label = STARTUP.render('... warming up, please wait ...', 5, WHITE)
screen.blit(label, (L_STARTUP_X, L_STARTUP_Y))
pygame.display.flip()

# image config

logo = pygame.image.load(LOCALEPATHIMAGE + 'VOKA_AW_LOGO_CMYK668.jpg')
##sms = pygame.image.load(LOCALEPATHIMAGE + '8876.jpg')
##sms = sms.convert()
##sms = pygame.transform.scale(sms, max(modes))

event = pygame.image.load(LOCALEPATHIMAGE +'scherm.jpg')
event = event.convert()
event = pygame.transform.scale(event, max(modes))

partner1 = pygame.image.load(LOCALEPATHIMAGE + 'PP_CORP.jpg')
partner1 = partner1.convert()
partner1 = pygame.transform.scale(partner1, max(modes))
partner2 = pygame.image.load(LOCALEPATHIMAGE + 'PP_BUSIACT.jpg')
partner2 = partner2.convert()
partner2 = pygame.transform.scale(partner2, max(modes))

# run the loop

while True:
    # startscherm
    
    # play background sound zenfm radio in Auditorium
    if LOCATION_DETAIL == 'Auditorium':
        try:
            client = MPDClient()
            client.connect("localhost",6600)            
            if client.status()['state']in('pause','stop'):
                client.clear()
                client.add(STREAM)
                client.play()
        except:
            pass
    # tekenen van welkom scherm ipv afbeelding
    
    screen.fill(WHITE)
    ORANGE = load_ORANGE()
    GRAY = load_GRAY()
    RECHTS = pygame.image.load(LOCALEPATHIMAGE + load_RECHTS())
    RECHTS = RECHTS.convert()
    RECHTS = pygame.transform.scale(RECHTS, (L_SCALE_RIGHT_X,L_SCALE_RIGHT_Y))
    

    # render text
    welcome = TITLE1.render('VAN HARTE WELKOM', 5, GRAY)
    screen.blit(welcome, (L_WELCOME_X, L_WELCOME_Y))

    screen.blit(RECHTS,(L_RIGHT_X, L_RIGHT_Y))
    
    # add logo
    screen.blit(logo, pygame.rect.Rect(L_LOGO_X, L_LOGO_Y, 128, 128))
    pygame.display.flip()
    time.sleep(WAITTIME)

    # events
    # if check connection to mysql else goto reclame
    # if check event available in mysql else goto reclame
    # for each event teken event scherm
    
    teller = 0
    count = 0
    try:
        (events, count) = get_events(LOCATION,LOCATION_DETAIL)
    except:
        pass
     
    while count > 0:
        screen.fill(WHITE)
        ORANGE = load_ORANGE()
        GRAY = load_GRAY()
        RECHTS = pygame.image.load(LOCALEPATHIMAGE + load_RECHTS())
        RECHTS = RECHTS.convert()
        RECHTS = pygame.transform.scale(RECHTS, (L_SCALE_RIGHT_X,L_SCALE_RIGHT_Y))

        KA_TITEL = TITLE1.render('VANDAAG', 5, GRAY)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # render text
        titelevent = TITLE.render(events[teller][0], 5, GRAY)
        screen.blit(titelevent, (L_EVENT_X, L_EVENTN_Y))
        starttime = TITLE2.render(events[teller][1], 5, ORANGE)
        screen.blit(starttime, (L_EVENT_X, L_EVENTT_Y))
        location = TITLE2.render(events[teller][2], 5, ORANGE)
        screen.blit(location, (L_EVENT_X, L_EVENTL_Y))

        # add image right
        screen.blit(RECHTS,(L_RIGHT_X, L_RIGHT_Y))

        pygame.display.flip()
        time.sleep(WAITTIME)
        count = count - 1
        teller = teller + 1

##    # reclame 8876
##    if LOCATION_DETAIL != 'Auditorium':
##        screen.blit(sms, (0, 0))
##        pygame.display.flip()
##        time.sleep(WAITTIME)

#    #reclame hoofdevent
    screen.blit(event,(0,0))
    pygame.display.flip()
    time.sleep(WAITTIME)
    
    # try handling instead of ping result

    count = 0
    try:
        (agenda, count) = get_agenda()
    except:
        pass
        
    
    if count == 3:
        screen.fill(WHITE)
        ORANGE = load_ORANGE()
        GRAY = load_GRAY()
        RECHTS = pygame.image.load(LOCALEPATHIMAGE + load_RECHTS())
        RECHTS = RECHTS.convert()
        RECHTS = pygame.transform.scale(RECHTS, (L_SCALE_RIGHT_X,L_SCALE_RIGHT_Y))


        # render text
        KA_TITEL = TITLE1.render('AGENDA', 5, GRAY)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE2.render(agenda[0][1], 5, ORANGE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_3_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, GRAY)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_3_T1_Y))
        #agendatype1 = TEXT.render(agenda[0][2], 5, GRAY)
        #screen.blit(agendatype1, (L_KA_ET_X, L_KA_3_T1_Y))

        # event2
        agendadatum2 = TITLE2.render(agenda[1][1], 5, ORANGE)
        screen.blit(agendadatum2, (L_KA_ED_X, L_KA_3_E2_Y))
        agendaitem2 = TITLE.render(agenda[1][0], 5, GRAY)
        screen.blit(agendaitem2, (L_KA_ET_X, L_KA_3_T2_Y))
        #agendatype2 = TEXT.render(agenda[1][2], 5, GRAY)
        #screen.blit(agendatype2, (L_KA_ET_X, L_KA_3_T2_Y))

        # event3
        agendadatum3 = TITLE2.render(agenda[2][1], 5, ORANGE)
        screen.blit(agendadatum3, (L_KA_ED_X, L_KA_3_E3_Y))
        agendaitem3 = TITLE.render(agenda[2][0], 5, GRAY)
        screen.blit(agendaitem3, (L_KA_ET_X, L_KA_3_T3_Y))
        #agendatype3 = TEXT.render(agenda[2][2], 5, GRAY)
        #screen.blit(agendatype3, (L_KA_ET_X, L_KA_3_T3_Y))

        # add image right
        screen.blit(RECHTS,(L_RIGHT_X, L_RIGHT_Y))

        pygame.display.flip()
        time.sleep(WAITTIME)

    if count == 2:
        screen.fill(WHITE)
        ORANGE = load_ORANGE()
        GRAY = load_GRAY()
        RECHTS = pygame.image.load(LOCALEPATHIMAGE + load_RECHTS())
        RECHTS = RECHTS.convert()
        RECHTS = pygame.transform.scale(RECHTS, (L_SCALE_RIGHT_X,L_SCALE_RIGHT_Y))


        # render text
        KA_TITEL = TITLE1.render('AGENDA', 5, GRAY)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE2.render(agenda[0][1], 5, ORANGE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_2_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, GRAY)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_2_T1_Y))
        #agendatype1 = TEXT.render(agenda[0][2], 5, GRAY)
        #screen.blit(agendatype1, (L_KA_ET_X, L_KA_2_T1_Y))

        # event2
        agendadatum2 = TITLE2.render(agenda[1][1], 5, ORANGE)
        screen.blit(agendadatum2, (L_KA_ED_X, L_KA_2_E2_Y))
        agendaitem2 = TITLE.render(agenda[1][0], 5, GRAY)
        screen.blit(agendaitem2, (L_KA_ET_X, L_KA_2_T2_Y))
        #agendatype2 = TEXT.render(agenda[1][2], 5, GRAY)
        #screen.blit(agendatype2, (L_KA_ET_X, L_KA_2_T2_Y))

        # add image right
        screen.blit(RECHTS,(L_RIGHT_X, L_RIGHT_Y))
        
        pygame.display.flip()
        time.sleep(WAITTIME)

    if count == 1:
        screen.fill(WHITE)
        ORANGE = load_ORANGE()
        GRAY = load_GRAY()
        RECHTS = pygame.image.load(LOCALEPATHIMAGE + load_RECHTS())
        RECHTS = RECHTS.convert()
        RECHTS = pygame.transform.scale(RECHTS, (L_SCALE_RIGHT_X,L_SCALE_RIGHT_Y))


        # render text
        KA_TITEL = TITLE1.render('AGENDA', 5, GRAY)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE2.render(agenda[0][1], 5, ORANGE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_1_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, GRAY)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_1_T1_Y))
        #agendatype1 = TEXT.render(agenda[0][2], 5, GRAY)
        #screen.blit(agendatype1, (L_KA_ET_X, L_KA_1_T1_Y))
        
        # add image right
        screen.blit(RECHTS,(L_RIGHT_X, L_RIGHT_Y))

        pygame.display.flip()
        time.sleep(WAITTIME)

    # partners Waasland

    if LOCATION == 'Waasland':
        screen.blit(partner1, (0, 0))
        pygame.display.flip()
        time.sleep(WAITTIME)
        screen.blit(partner2, (0, 0))
        pygame.display.flip()
        time.sleep(WAITTIME)

    # jaarverslag film Antwerpen Wintertuin

    minute = time.strftime("%M")
    movie_check = int(minute) % 10

    if movie_check == 0 and LOCATION_DETAIL == 'Wintertuin':
        try:
            minute_played = open('./movie.tmp','r').read()
        except IOError:
            print "Error: movie.tmp does not appear to exist."
            minute_played = "OK"
      

        if minute_played != minute or minute_played == "OK":
            omxp = Popen(['omxplayer', MOVIE])
            try:
                with open('./movie.tmp', 'w') as movielog:
                    movielog.write(minute)
            except IOError:
                print "Error: movie.tmp cannot be made."

       

