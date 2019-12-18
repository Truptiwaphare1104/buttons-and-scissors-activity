#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Buttons and Scissors
# Copyright (C) 2015  Utkarsh Tiwari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Utkarsh Tiwari    iamutkarshtiwari@gmail.com

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pickle
import pygame
import sys
from buttons import *
from random import *
from track import *
from setbuttons import *
from linetrack import *
from welcomescreen import *
from scorescreen import *
from about import *
from rules import *


class game:

    def make(self):
        pygame.init()
        sound = True
        try:
            pygame.mixer.init()
        except Exception as err:
            sound = False
            print('error with sound', err)

        i = 0
        gameDisplay = pygame.display.get_surface()
        if not(gameDisplay):
            info = pygame.display.Info()
            gameDisplay = pygame.display.set_mode(
                (info.current_w, info.current_h))  # initializing display surface
            # window name
            pygame.display.set_caption("Buttons & Scissors")
            gameicon = pygame.image.load('buts/icon2.png')
            pygame.display.set_icon(gameicon)

        disp_width = 800
        disp_height = 600

        clock = pygame.time.Clock()
        timer = pygame.time.Clock()

        background = pygame.image.load(
            "buts/background.jpg").convert()  # background image load
        background = pygame.transform.scale(
            background, (disp_width + 100, disp_height + 250))
        home = pygame.transform.scale(
            pygame.image.load("buts/home.png"), (80, 80))
        restart = pygame.transform.scale(
            pygame.image.load("buts/restart.png"), (80, 80))
        undo = pygame.transform.scale(
            pygame.image.load("buts/undo.png"), (80, 80))
        hlp = pygame.transform.scale(
            pygame.image.load("buts/help.png"), (80, 80))
        stitch = pygame.transform.scale(
            pygame.image.load("buts/stitch.png"), (40, 40))

        # SOUND FILES LOADED
        b = welcome()  # Welcome Screen Call
        bvalue = b.make(gameDisplay, sound)
        crashed = False
        black = (0, 0, 0)
        white = (255, 255, 255)
        horizontal = vertical = rightd = leftd = 0
        rightd = leftd = lastx = lasty = 0
        buttonslist = []
        x = [370 + 280, 435 + 280, 500 + 280, 565 + 280, 630 + 280]
        y = [235, 300, 365, 430, 495]
        backup = []
        backflag = 0
        homeflag = 0
        backreset = 0
        totaltime = 0
        temp = track()
        flag = 0
        helpf = 0
        end = 0
        Biglist = []
        ru = 0
        buttonup = 0
        moves = 0
        lastb = 0

        if bvalue == 1:                                                         # New Game
            buttonslist = list(setbuttons().buttonslist)
            backupbuttonslist = list(buttonslist)
            totaltime = 0
        if bvalue == 0:                                                           # Continue
            with open('score.pkl', 'rb') as input:
                buttonslist = pickle.load(input)
                backup = pickle.load(input)
                backupbuttonslist = pickle.load(input)
                totaltime = pickle.load(input)
                moves = pickle.load(input)

        print(moves)

        showline = linetrack(buttonslist[0], buttonslist)

        if sound:
            pygame.mixer.Sound("sound/gamestart.ogg").play(0)

        while not crashed:  # MAIN GAME LOOP BEGINS
            # Gtk events
            while Gtk.events_pending():
                Gtk.main_iteration()
            event = pygame.event.poll()
            totaltime += timer.tick()
            if event.type == pygame.QUIT:
                totaltime += timer.tick()
                with open('score.pkl', 'wb') as output:
                    pickle.dump(buttonslist, output, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(backup, output, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(backupbuttonslist, output,
                                pickle.HIGHEST_PROTOCOL)
                    pickle.dump(totaltime, output, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(moves, output, pickle.HIGHEST_PROTOCOL)

                crashed = True

            mos_x, mos_y = pygame.mouse.get_pos()

            if(not ((mos_x <= 675 + 280) and (mos_x >= 363 + 280) and (mos_y <= 532) and (mos_y >= 225))):
                temp = track()
                vertical = horizontal = rightd = leftd = 0
                lastx = lasty = 0

            gameDisplay.fill(black)
            gameDisplay.blit(background, (0 - 50 + 280, 0 - 140))

            for i in x:              # loop to display all stitches on their respactive positions #
                for j in y:
                    gameDisplay.blit(stitch, (i, j))

            if home.get_rect(center=(270 + 280, 255)).collidepoint(mos_x, mos_y):  # HOME
                gameDisplay.blit(pygame.transform.scale(
                    home, (90, 90)), (250 + 280, 235))
                if (pygame.mouse.get_pressed())[0] == 1 and homeflag == 0:
                    homeflag = 1
                    if sound:
                        pygame.mixer.stop()
                    with open('score.pkl', 'wb') as output:
                        pickle.dump(buttonslist, output,
                                    pickle.HIGHEST_PROTOCOL)
                        pickle.dump(backup, output, pickle.HIGHEST_PROTOCOL)
                        pickle.dump(backupbuttonslist, output,
                                    pickle.HIGHEST_PROTOCOL)
                        pickle.dump(totaltime, output, pickle.HIGHEST_PROTOCOL)
                        pickle.dump(moves, output, pickle.HIGHEST_PROTOCOL)

                    b = welcome()  # Welcome Screen Call
                    bvalue = b.make(gameDisplay, sound)
                    if bvalue == 1:                                                         # New Game
                        buttonslist = list(setbuttons().buttonslist)
                        backupbuttonslist = list(buttonslist)
                        totaltime = 0
                        lastb = 0
                        backup = []
                        moves = 0
                    if bvalue == 0:                                                           # Continue
                        with open('score.pkl', 'rb') as input:
                            buttonslist = pickle.load(input)
                            backup = pickle.load(input)
                            backupbuttonslist = pickle.load(input)
                            totaltime = pickle.load(input)
                            moves = pickle.load(input)

                    print(moves)
                    backflag = 0
                    homeflag = 0
                    backreset = 0
                    helpf = 0
                    temp = track()
                    flag = 0
                    Biglist = []
                    lastb = 0
                    buttonup = 0

                    showline = linetrack(buttonslist[0], buttonslist)

                    if sound:
                        pygame.mixer.music.load("sound/gamestart.ogg")
                        pygame.mixer.music.play(0)

                if event.type == pygame.MOUSEBUTTONUP:
                    homeflag = 0
            else:
                gameDisplay.blit(home, (250 + 280, 235))

            if undo.get_rect(center=(270 + 280, 335)).collidepoint(mos_x, mos_y):  # Undo
                gameDisplay.blit(pygame.transform.scale(
                    undo, (90, 90)), (250 + 280, 315))
                if (pygame.mouse.get_pressed())[0] == 1 and len(backup) != 0 and backflag == 0:
                    if sound:
                        pygame.mixer.music.load("sound/undo1.ogg")
                        pygame.mixer.music.play(0)

                    for j in backup[len(backup) - 1]:
                        j.flag = 0
                        j.i = 0

                    for i in backup[len(backup) - 1]:
                        buttonslist.append(i)

                    backup.remove(backup[len(backup) - 1])

                    backflag = 1
                    moves -= 1
                    flag = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    backflag = 0
                    flag = 0
            else:
                gameDisplay.blit(undo, (250 + 280, 315))

            if restart.get_rect(center=(270 + 280, 415)).collidepoint(mos_x, mos_y):  # Restart
                gameDisplay.blit(pygame.transform.scale(
                    restart, (90, 90)), (250 + 280, 395))
                if(pygame.mouse.get_pressed())[0] == 1 and backreset == 0:
                    if sound:
                        pygame.mixer.music.load("sound/button.ogg")
                        pygame.mixer.music.play(0)
                    totaltime = 0
                    backup = []
                    backflag = 0
                    temp = track()
                    flag = 0
                    end = 0
                    Biglist = []
                    backreset = 1
                    moves = 0
                    lastb = 0
                    helpf = 0
                    buttonup = 0
                    for j in backupbuttonslist:
                        j.flag = 0
                        j.i = 0
                    buttonslist = list(backupbuttonslist)
                if event.type == pygame.MOUSEBUTTONUP:
                    backreset = 0

            else:
                gameDisplay.blit(restart, (250 + 280, 395))

            if hlp.get_rect(center=(270 + 280, 495)).collidepoint(mos_x, mos_y):  # Help
                gameDisplay.blit(pygame.transform.scale(
                    hlp, (90, 90)), (250 + 280, 475))
                if(pygame.mouse.get_pressed())[0] == 1 and helpf == 0:
                    if sound:
                        pygame.mixer.music.load("sound/button.ogg")
                        pygame.mixer.music.play(0)
                    ru = rule()
                    ru.make(gameDisplay, sound)
                    helpf = 1

                if event.type == pygame.MOUSEBUTTONUP:
                    helpf = 0
            else:
                gameDisplay.blit(hlp, (250 + 280, 475))

            # BUTTON TRACKING BEGINS......
            for t in buttonslist:
                if t.but.get_rect(center=(t.x_axis + 25, t.y_axis + 25)).collidepoint(mos_x, mos_y):
                    if t.x_axis == lastx and t.y_axis == lasty:
                        break
                    button = t
                    buttoncheck = 1
                    diff = button.x_axis - button.y_axis
                    total = button.x_axis + button.y_axis

                    if (pygame.mouse.get_pressed())[0] == 1 and buttonup == 0:
                        flag = 1
                        if(len(temp.coordinatelist) != 0):
                            # SAME COLOR TEST ###
                            if (button.butno == temp.coordinatelist[len(temp.coordinatelist) - 1].butno):
                                if((lastx == button.x_axis) or (lasty == button.y_axis) or (lastdiff == diff) or (lasttotal == total)):
                                    if(lastdiff == diff):
                                        chkf = 0
                                        for chk in buttonslist:
                                            if (chk.x_axis - chk.y_axis == diff):
                                                if lasty > button.y_axis and lastx > button.x_axis:
                                                    if (chk.y_axis < lasty and chk.x_axis < lastx) and (chk.y_axis > button.y_axis and chk.x_axis > button.x_axis):
                                                        chkf = 1
                                                        break
                                                if lasty < button.y_axis and lastx < button.x_axis:
                                                    if (chk.y_axis > lasty and chk.x_axis > lastx) and (chk.y_axis < button.y_axis and chk.x_axis < button.x_axis):
                                                        chkf = 1
                                                        break
                                    elif(lasttotal == total):
                                        chkf = 0
                                        for chk in buttonslist:
                                            if (chk.x_axis + chk.y_axis == total):
                                                if lasty > button.y_axis and lastx < button.x_axis:
                                                    if (chk.y_axis < lasty and chk.x_axis > lastx) and (chk.y_axis > button.y_axis and chk.x_axis < button.x_axis):
                                                        chkf = 1
                                                        break
                                                if lasty < button.y_axis and lastx > button.x_axis:
                                                    if (chk.y_axis > lasty and chk.x_axis < lastx) and (chk.y_axis < button.y_axis and chk.x_axis > button.x_axis):
                                                        chkf = 1
                                                        break
                                    elif(lastx == button.x_axis):
                                        chkf = 0
                                        for chk in buttonslist:
                                            if chk.x_axis == lastx:
                                                if lasty > button.y_axis:
                                                    if (chk.y_axis < lasty and chk.x_axis == lastx) and (chk.y_axis > button.y_axis and chk.x_axis == lastx):
                                                        chkf = 1
                                                        break
                                                if lasty < button.y_axis:
                                                    if (chk.y_axis > lasty and chk.x_axis == lastx) and (chk.y_axis < button.y_axis and chk.x_axis == lastx):
                                                        chkf = 1
                                                        break
                                    else:
                                        chkf = 0
                                        for chk in buttonslist:
                                            if chk.y_axis == lasty:
                                                if lastx > button.x_axis:
                                                    if (chk.x_axis < lastx and chk.y_axis == lasty) and (chk.x_axis > button.x_axis and chk.y_axis == lasty):
                                                        chkf = 1
                                                        break
                                                if lastx < button.x_axis:
                                                    if (chk.x_axis > lastx and chk.y_axis == lasty) and (chk.x_axis < button.x_axis and chk.y_axis == lasty):
                                                        chkf = 1
                                                        break
                                    if(vertical == 0 and horizontal == 0 and rightd == 0 and leftd == 0):
                                        if chkf == 0:
                                            if lasttotal == total:
                                                rightd = 1
                                                temp.insert(button)
                                                lastdiff = button.x_axis - button.y_axis
                                                lasttotal = button.x_axis + button.y_axis
                                                lastx = button.x_axis
                                                lasty = button.y_axis
                                            elif lastdiff == diff:
                                                leftd = 1
                                                temp.insert(button)
                                                lastdiff = button.x_axis - button.y_axis
                                                lasttotal = button.x_axis + button.y_axis
                                                lastx = button.x_axis
                                                lasty = button.y_axis
                                            elif lastx == button.x_axis:
                                                vertical = 1
                                                temp.insert(button)
                                                lastdiff = button.x_axis - button.y_axis
                                                lasttotal = button.x_axis + button.y_axis
                                                lastx = button.x_axis
                                                lasty = button.y_axis
                                            else:
                                                horizontal = 1
                                                temp.insert(button)
                                                lastdiff = button.x_axis - button.y_axis
                                                lasttotal = button.x_axis + button.y_axis
                                                lastx = button.x_axis
                                                lasty = button.y_axis
                                        else:
                                            temp = track()
                                            buttonup = 1
                                            vertical = horizontal = rightd = leftd = 0
                                    else:
                                        if(vertical == 1):
                                            if(lastx == button.x_axis):
                                                if chkf == 0:
                                                    temp.insert(button)
                                                    lastdiff = button.x_axis - button.y_axis
                                                    lasttotal = button.x_axis + button.y_axis
                                                    lastx = button.x_axis
                                                    lasty = button.y_axis
                                                else:
                                                    temp = track()
                                                    buttonup = 1
                                                    vertical = horizontal = rightd = leftd = 0

                                        elif(horizontal == 1):
                                            if(lasty == button.y_axis):
                                                if chkf == 0:
                                                    temp.insert(button)
                                                    lastdiff = button.x_axis - button.y_axis
                                                    lasttotal = button.x_axis + button.y_axis
                                                    lastx = button.x_axis
                                                    lasty = button.y_axis
                                                else:
                                                    temp = track()
                                                    buttonup = 1
                                                    vertical = horizontal = rightd = leftd = 0

                                        elif(leftd == 1):
                                            if(lastdiff == diff):
                                                if chkf == 0:
                                                    temp.insert(button)
                                                    lastdiff = button.x_axis - button.y_axis
                                                    lasttotal = button.x_axis + button.y_axis
                                                    lastx = button.x_axis
                                                    lasty = button.y_axis
                                                else:
                                                    temp = track()
                                                    buttonup = 1
                                                    vertical = horizontal = rightd = leftd = 0
                                        else:
                                            if(lasttotal == total):
                                                if chkf == 0:
                                                    temp.insert(button)
                                                    lastdiff = button.x_axis - button.y_axis
                                                    lasttotal = button.x_axis + button.y_axis
                                                    lastx = button.x_axis
                                                    lasty = button.y_axis
                                                else:
                                                    temp = track()
                                                    buttonup = 1
                                                    vertical = horizontal = rightd = leftd = 0

                            else:  # to nullify the tracking if  other buttons are encountered in path
                                temp = track()
                                buttonup = 1
                                vertical = horizontal = rightd = leftd = 0
                                lastx = lasty = 0
                        else:
                            if sound:
                                pygame.mixer.music.load("sound/cbut.ogg")
                                pygame.mixer.music.play(0)
                            temp.insert(button)
                            lastdiff = button.x_axis - button.y_axis
                            lasttotal = button.x_axis + button.y_axis
                            lastx = button.x_axis
                            lasty = button.y_axis
                            showline = linetrack(
                                temp.coordinatelist[0], buttonslist)

                            vertical = horizontal = rightd = leftd = 0

            if flag == 1:
                if (pygame.mouse.get_pressed())[0] == 0:
                    if(len(temp.coordinatelist) != 0):
                        if(t.x_axis == temp.coordinatelist[0].x_axis and t.y_axis == temp.coordinatelist[0].y_axis):
                            temp = track()
                            vertical = horizontal = rightd = leftd = 0

                    if(len(temp.coordinatelist) == 1):
                        temp = track()
                        vertical = horizontal = rightd = leftd = 0
                        flag = 0

                    if(len(temp.coordinatelist) > 1 and len(buttonslist) != 0):
                        for j in temp.coordinatelist:
                            buttonslist.remove(j)
                        lastbackup = list(temp.coordinatelist)
                        backup.append(list(temp.coordinatelist))
                        temp2 = scissorrun(list(temp.coordinatelist))
                        Biglist.append(temp2)
                    flag = 0
                    temp = track()
                    buttonup = 0
                    lastx = lasty = 0
                    vertical = horizontal = rightd = leftd = 0

            if(len(temp.coordinatelist) != 0):          # White Circle Blitting
                temp.display(gameDisplay)

            # Button Display List
            for i in range(len(buttonslist)):        # Non Movable Buttons
                buttonslist[i].display(gameDisplay)

            if flag == 1:                                # White line display
                showline.displayline(gameDisplay)

            if(len(Biglist) != 0):
                for j in Biglist:  # Movable Buttons
                    if j.sentcoordinatelist[j.length - 1].y_axis + (0.2 * (j.sentcoordinatelist[j.length - 1].i**2)) > 620:
                        # checklist=j
                        Biglist.remove(j)
                        moves += 1
                        if len(buttonslist) == 0 and len(Biglist) == 0:
                            end = 1
                        continue
                    j.display(gameDisplay)

            if len(buttonslist) == 0 and end == 1:
                b = scores()
                b = b.make(gameDisplay, totaltime, moves, sound)
                if b == 1:
                    buttonslist = list(setbuttons().buttonslist)
                    backupbuttonslist = list(buttonslist)
                    totaltime = 0
                    backup = []
                    backflag = 0
                    homeflag = 0
                    backreset = 0
                    totaltime = 0
                    temp = track()
                    moves = 0
                    flag = 0
                    end = 0
                    Biglist = []
                    lastb = 0
                    helpf = 0
                    buttonup = 0
                    showline = linetrack(buttonslist[0], buttonslist)

                    if sound:
                        pygame.mixer.music.load("sound/gamestart.ogg")
                        pygame.mixer.music.play(0)
                if b == 2:
                    totaltime = 0
                    backup = []
                    backflag = 0
                    helpf = 0
                    temp = track()
                    flag = 0
                    end = 0
                    Biglist = []
                    lastb = 0
                    backreset = 1
                    moves = 0
                    buttonup = 0
                    for j in backupbuttonslist:
                        j.flag = 0
                        j.i = 0
                    buttonslist = list(backupbuttonslist)
                    if sound:
                        pygame.mixer.music.load("sound/gamestart.ogg")
                        pygame.mixer.music.play(0)

            pygame.display.update()
            clock.tick(50)

            if crashed == True:                                   # Game crash or Close check
                pygame.quit()
                sys.exit()

        # Just a window exception check condition
        event1 = pygame.event.get()
        if event1.type == pygame.QUIT:
            crashed = True

        if crashed == True:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    g = game()
    g.make()
