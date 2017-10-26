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
from background import load_background
from database import get_events
from database import get_agenda
from mpd import MPDClient

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

STARTUP = pygame.font.SysFont('monospace', 25)
TEXT = pygame.font.SysFont('roboto', 35, bold=True)
TITLE = pygame.font.SysFont('roboto', 50, bold=True)
TITLE1 = pygame.font.SysFont('roboto', 75, bold=True)
WHITE = (255, 255, 255)
WAITTIME = 10  # default time to wait between images (in seconds)
THICKNESS = 40

# media files
LOCALEPATH = '/home/pi/welkomscherm/img/'
MOVIE = '/home/pi/Desktop/jaaroverzicht.mp4'
STREAM = "http://lb.zenfm.be/zenfm.mp3"

# set up the window, max screensize, fullscreen no frames

modes = pygame.display.list_modes()
screen = pygame.display.set_mode(max(modes), pygame.NOFRAME)
pygame.mouse.set_visible(False)
(x, y) = screen.get_size()

# locations
# TV Waasland resolutie 1920x1080 as refence to other resolutions

L_STARTUP_X = 700 * x / 1920
L_STARTUP_Y = 540 * y / 1080
L_WELCOME_X = 150 * x / 1920
L_WELCOME_Y = 800 * y / 1080
L_LOGO_X = 1350 * x / 1920
L_LOGO_Y = 800 * y / 1080
L_BORDER_AX = 100 * x / 1920
L_BORDER_AY = 100 * y / 1080
L_BORDER_BX = 1600 * x / 1920
L_BORDER_CY = 900 * y / 1080
L_EVENT_X = 150 * x / 1920
L_EVENTN_Y = 300 * y / 1080
L_EVENTT_Y = 500 * y / 1080
L_EVENTL_Y = 700 * y / 1080
L_KA_TITEL_X = 150 * x / 1920
L_KA_TITEL_Y = 150 * y / 1080
L_KA_ED_X = 150 * x / 1920  # horizontaal afstand voor kameragenda datum
L_KA_ET_X = 320 * x / 1920  # horizontaal afstand voor kameragenda event
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

# startup screen

label = STARTUP.render('... warming up, please wait ...', 5, WHITE)
screen.blit(label, (L_STARTUP_X, L_STARTUP_Y))
pygame.display.flip()

# image config

logo = pygame.image.load(LOCALEPATH + 'logo.png').convert_alpha()
sms = pygame.image.load(LOCALEPATH + '8876.jpg')
sms = sms.convert()
sms = pygame.transform.scale(sms, max(modes))

#event = pygame.image.load(LOCALEPATH +'EO.jpg')
#event = event.convert()
#event = pygame.transform.scale(event, max(modes))

partner1 = pygame.image.load(LOCALEPATH + 'PP_CORP.jpg')
partner1 = partner1.convert()
partner1 = pygame.transform.scale(partner1, max(modes))
partner2 = pygame.image.load(LOCALEPATH + 'PP_BUSIACT.jpg')
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
    
    screen.fill(load_background())
    pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1,
                     L_BORDER_AY), (L_BORDER_BX, L_BORDER_AY),
                     THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_AX, L_BORDER_AY),
                     (L_BORDER_AX, L_BORDER_CY), THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1,
                     L_BORDER_CY), (L_BORDER_BX, L_BORDER_CY),
                     THICKNESS)
    pygame.draw.line(screen, WHITE, (L_BORDER_BX - THICKNESS / 2,
                     L_BORDER_AY), (L_BORDER_BX - THICKNESS / 2,
                     L_BORDER_CY), THICKNESS)

    # render text
    welcome = TITLE.render('VAN HARTE WELKOM', 5, WHITE)
    screen.blit(welcome, (L_WELCOME_X, L_WELCOME_Y))

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
        screen.fill(load_background())
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_AY),(L_BORDER_BX, L_BORDER_AY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX,L_BORDER_AY), (L_BORDER_AX,L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_CY),(L_BORDER_BX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_BX - THICKNESS / 2, L_BORDER_AY),(L_BORDER_BX - THICKNESS / 2,L_BORDER_CY), THICKNESS)

        # render text
        titelevent = TITLE.render(events[teller][0], 5, WHITE)
        screen.blit(titelevent, (L_EVENT_X, L_EVENTN_Y))
        starttime = TITLE.render(events[teller][1], 5, WHITE)
        screen.blit(starttime, (L_EVENT_X, L_EVENTT_Y))
        location = TITLE.render(events[teller][2], 5, WHITE)
        screen.blit(location, (L_EVENT_X, L_EVENTL_Y))

        # add logo
        screen.blit(logo, pygame.rect.Rect(L_LOGO_X, L_LOGO_Y,128, 128))
        pygame.display.flip()
        time.sleep(WAITTIME)
        count = count - 1
        teller = teller + 1

    # reclame 8876
    if LOCATION_DETAIL != 'Auditorium':
        screen.blit(sms, (0, 0))
        pygame.display.flip()
        time.sleep(WAITTIME)

##    #reclame hoofdevent
#    screen.blit(event,(0,0))
#    pygame.display.flip()
#    time.sleep(WAITTIME)
    
    # try handling instead of ping result

    count = 0
    try:
        (agenda, count) = get_agenda()
    except:
        pass
        
    
    if count == 3:
        screen.fill(load_background())
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_AY),(L_BORDER_BX, L_BORDER_AY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX, L_BORDER_AY), (L_BORDER_AX,L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_CY),(L_BORDER_BX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_BX - THICKNESS / 2, L_BORDER_AY),(L_BORDER_BX - THICKNESS / 2,L_BORDER_CY), THICKNESS)

        # render text
        KA_TITEL = TITLE1.render('Kameragenda', 5, WHITE)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE.render(agenda[0][1], 5, WHITE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_3_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, WHITE)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_3_E1_Y))
        agendatype1 = TEXT.render(agenda[0][2], 5, WHITE)
        screen.blit(agendatype1, (L_KA_ET_X, L_KA_3_T1_Y))

        # event2
        agendadatum2 = TITLE.render(agenda[1][1], 5, WHITE)
        screen.blit(agendadatum2, (L_KA_ED_X, L_KA_3_E2_Y))
        agendaitem2 = TITLE.render(agenda[1][0], 5, WHITE)
        screen.blit(agendaitem2, (L_KA_ET_X, L_KA_3_E2_Y))
        agendatype2 = TEXT.render(agenda[1][2], 5, WHITE)
        screen.blit(agendatype2, (L_KA_ET_X, L_KA_3_T2_Y))

        # event3
        agendadatum3 = TITLE.render(agenda[2][1], 5, WHITE)
        screen.blit(agendadatum3, (L_KA_ED_X, L_KA_3_E3_Y))
        agendaitem3 = TITLE.render(agenda[2][0], 5, WHITE)
        screen.blit(agendaitem3, (L_KA_ET_X, L_KA_3_E3_Y))
        agendatype3 = TEXT.render(agenda[2][2], 5, WHITE)
        screen.blit(agendatype3, (L_KA_ET_X, L_KA_3_T3_Y))

        # add logo
        screen.blit(logo, pygame.rect.Rect(L_LOGO_X, L_LOGO_Y,128, 128))
        pygame.display.flip()
        time.sleep(WAITTIME)

    if count == 2:
        screen.fill(load_background())
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_AY),(L_BORDER_BX, L_BORDER_AY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX, L_BORDER_AY), (L_BORDER_AX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_CY),(L_BORDER_BX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_BX - THICKNESS / 2, L_BORDER_AY),(L_BORDER_BX - THICKNESS / 2, L_BORDER_CY), THICKNESS)

        # render text
        KA_TITEL = TITLE1.render('Kameragenda', 5, WHITE)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE.render(agenda[0][1], 5, WHITE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_2_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, WHITE)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_2_E1_Y))
        agendatype1 = TEXT.render(agenda[0][2], 5, WHITE)
        screen.blit(agendatype1, (L_KA_ET_X, L_KA_2_T1_Y))

        # event2
        agendadatum2 = TITLE.render(agenda[1][1], 5, WHITE)
        screen.blit(agendadatum2, (L_KA_ED_X, L_KA_2_E2_Y))
        agendaitem2 = TITLE.render(agenda[1][0], 5, WHITE)
        screen.blit(agendaitem2, (L_KA_ET_X, L_KA_2_E2_Y))
        agendatype2 = TEXT.render(agenda[1][2], 5, WHITE)
        screen.blit(agendatype2, (L_KA_ET_X, L_KA_2_T2_Y))

        # add logo
        screen.blit(logo, pygame.rect.Rect(L_LOGO_X, L_LOGO_Y,128, 128))
        pygame.display.flip()
        time.sleep(WAITTIME)

    if count == 1:
        screen.fill(load_background())
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_AY),(L_BORDER_BX, L_BORDER_AY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX, L_BORDER_AY), (L_BORDER_AX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_AX - THICKNESS / 2 + 1, L_BORDER_CY),(L_BORDER_BX, L_BORDER_CY), THICKNESS)
        pygame.draw.line(screen, WHITE, (L_BORDER_BX - THICKNESS / 2, L_BORDER_AY),(L_BORDER_BX - THICKNESS / 2, L_BORDER_CY), THICKNESS)

        # render text
        KA_TITEL = TITLE1.render('Kameragenda', 5, WHITE)
        screen.blit(KA_TITEL, (L_KA_TITEL_X, L_KA_TITEL_Y))

        # event1
        agendadatum1 = TITLE.render(agenda[0][1], 5, WHITE)
        screen.blit(agendadatum1, (L_KA_ED_X, L_KA_1_E1_Y))
        agendaitem1 = TITLE.render(agenda[0][0], 5, WHITE)
        screen.blit(agendaitem1, (L_KA_ET_X, L_KA_1_E1_Y))
        agendatype1 = TEXT.render(agenda[0][2], 5, WHITE)
        screen.blit(agendatype1, (L_KA_ET_X, L_KA_1_T1_Y))

        # add logo
        screen.blit(logo, pygame.rect.Rect(L_LOGO_X, L_LOGO_Y,128, 128))
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

       
