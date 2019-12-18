import pygame
import sys
import os
import pickle
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class scores:

    def make(self, gameDisplay, totaltime, moves, sound):
        i = 0
        white = (255, 255, 255)
        disp_width = 900
        disp_height = 715
        crashed = False
        clock = pygame.time.Clock()
        pygame.font.init()
        mintime = 864000
        ex = 0
        newb = 0
        maxscore = 0
        scores = 0
        maxi = 0

        if os.path.getsize("lasttime.pkl") > 0:
            with open('lasttime.pkl', 'rb') as input:
                mintime = pickle.load(input)

        if os.path.getsize("maxscore.pkl") > 0:
            with open('maxscore.pkl', 'rb') as input:
                maxscore = pickle.load(input)

        if totaltime < mintime:
            newb = 1

        if totaltime < 30000:
            ex = 1

        if totaltime < mintime:
            with open('lasttime.pkl', 'wb') as output:
                pickle.dump(totaltime, output, pickle.HIGHEST_PROTOCOL)

        background = pygame.image.load(
            "buts/scorescreen/scorescreen.jpg").convert()
        background = pygame.transform.scale(
            background, (disp_width, disp_height))
        play = pygame.transform.scale(pygame.image.load(
            "buts/scorescreen/play.png"), (80, 80))
        restart = pygame.transform.scale(pygame.image.load(
            "buts/scorescreen/restart.png"), (80, 80))

        hours = 00
        minutes = 00
        seconds = 00
        totaltime = int(totaltime / 1000)  # seconds total
        black = (0, 0, 0)

        t = (100000 / (moves * totaltime))
        print(t)
        scores = int(t)

        if scores > maxscore:
            with open('maxscore.pkl', 'wb') as output:
                pickle.dump(scores, output, pickle.HIGHEST_PROTOCOL)

            maxi = 1

        if(int(totaltime / 3600) > 0):
            hours = int(totaltime / 3600)
            totaltime = int(totaltime % 3600)
        if(int(totaltime / 60) > 0):
            minutes = int(totaltime / 60)
            totaltime = int(totaltime % 60)

        seconds = int(totaltime)
        check = 0

        font_path = "fonts/arial.ttf"
        font_size = 50
        font1 = pygame.font.Font(font_path, font_size)

        font2 = pygame.font.Font(font_path, 25)
        checkimg = pygame.transform.scale(
            pygame.image.load("buts/scorescreen/check.png"), (30, 30))

        #Level=font.render("Score:"+str(score), 1,(255,255,255))
        Level = font1.render("Level", 1, (255, 255, 161))
        completed = font1.render("completed!", 1, (255, 255, 161))

        Score = font2.render("Time: " + str(hours) + ':' +
                             str(minutes) + ':' + str(seconds), 1, (255, 255, 161))
        t = 0
        scorex = -50
        Mintime = font2.render(str(mintime), 1, (255, 255, 161))
        Excellent = font2.render("Excellent!", 1, (255, 255, 161))
        Newbest = font2.render("New best score!", 1, (255, 255, 161))
        scores = font2.render("Score: " + str(scores), 1, (255, 255, 161))
        newhighscore = font2.render("New High Score!", 1, (255, 255, 161))
        if sound:
            pygame.mixer.stop()
            success = pygame.mixer.Sound("sound/levelcomplete.ogg")
            success.play(0)

        while not crashed:
            # Gtk events
            while Gtk.events_pending():
                Gtk.main_iteration()
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return 1

            if event.type == pygame.QUIT:
                crashed = True

            mos_x, mos_y = pygame.mouse.get_pos()
            gameDisplay.fill(black)
            gameDisplay.blit(background, (0 + 280, 0))

            if play.get_rect(center=(280 + 10 + 280 + 10, 400 + 10 + 20 + 50)).collidepoint(mos_x, mos_y):  # PLAY
                gameDisplay.blit(pygame.transform.scale(
                    play, (90, 90)), (280 + 280 + 10, 400 + 20 + 50))
                if (pygame.mouse.get_pressed())[0] == 1 and check == 0:
                    return 1
                    check = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    check = 0

            else:
                gameDisplay.blit(play, (280 + 280 + 10, 400 + 20 + 50))

            if restart.get_rect(center=(440 + 10 + 280 + 10, 400 + 10 + 20 + 50)).collidepoint(mos_x, mos_y):  # restart
                gameDisplay.blit(pygame.transform.scale(
                    restart, (90, 90)), (440 + 280 + 10, 400 + 20 + 50))
                if (pygame.mouse.get_pressed())[0] == 1 and check == 0:
                    return 2
                    check = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    check = 0

            else:
                gameDisplay.blit(restart, (440 + 280 + 10, 400 + 20 + 50))

            t += 1
            gameDisplay.blit(Level, (340 + 280 + 10, 50))
            gameDisplay.blit(completed, (280 + 280 + 10, 100))

            if(scorex + 280 > 0):
                gameDisplay.blit(Score, (scorex + 280, 230))
                gameDisplay.blit(scores, (scorex + 280, 260 + 10))
                if ex == 1:
                    gameDisplay.blit(
                        Excellent, (scorex + 5 + 10 + 280, 300 + 30))
                    gameDisplay.blit(
                        checkimg, (scorex - 40 + 10 + 280, 305 + 30))
                if newb == 1:
                    gameDisplay.blit(
                        Newbest, (scorex + 5 + 10 + 280, 380 + 30))
                    gameDisplay.blit(
                        checkimg, (scorex - 40 + 10 + 280, 385 + 30))
                if maxi == 1:
                    gameDisplay.blit(
                        newhighscore, (scorex + 5 + 10 + 280, 340 + 30))
                    gameDisplay.blit(
                        checkimg, (scorex - 40 + 10 + 280, 345 + 30))

            if(scorex + 280 < 320 + 280):
                scorex += 0.1 * (t**2)

            pygame.display.update()
            clock.tick(50)

            if crashed == True:                                   # Game crash or Close check
                pygame.quit()
                sys.exit()

        event1 = pygame.event.get()
        if event1.type == pygame.QUIT:
            crashed = True

        if crashed == True:
            pygame.quit()
            sys.exit()
