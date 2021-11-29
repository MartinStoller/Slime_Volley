import pygame
import helper_functions
import Button
import sys
import ball
import game
import player
import numpy as np


class GUI:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("Marty´s Coding Palace: Slime Volley")
    FPS = 60
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    FONT = pygame.font.SysFont('bahnschrift', 30)
    BIG_FONT = pygame.font.SysFont('bahnschrift', 55)
    CLOCK = pygame.time.Clock()
    WIDTH, HEIGHT = 1200, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    ball_sound = pygame.mixer.Sound(helper_functions.get_img_loc("ball_hits_sth_sound.wav"))  # Load a sound.

    def run_menu_screen(self):
        """
        Shows menu to the user. The menu is what you see, after starting the game file.
        There is only one Button needed: Start game
        """
        button_start = Button.Button("Start", "Game", 200, 120, (740, 550), screen=self.SCREEN,
                                     clock=self.CLOCK, elevation=6, GUI_object=self)
        menu_img = pygame.image.load(helper_functions.get_img_loc("menu_pic_final.png"))
        menu_img.convert()

        while True:
            self.SCREEN.blit(menu_img, pygame.rect.Rect(0, 0, 592, 220))
            button_start.draw()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def run_playingscreen(self):
        current_game = game.Game()
        volleyball, player1, player2, countdown, current_game.running = self.initialize_new_round(current_game.serve)
        play_background_img = pygame.image.load(helper_functions.get_img_loc("playing_pitch.png"))
        play_background_img.convert()
        net = pygame.Rect(591, 335, 19, 520)
        frames_since_col = 999  # initialize for later
        run_countdown = False

        while True:
            self.SCREEN.blit(play_background_img, pygame.rect.Rect(0, 0, 592, 220))
            volleyball.render()
            player1.render()
            player2.render()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and countdown == 0:
                    current_game.running = True

            if current_game.running is True:
                volleyball.move()

                # shows the y coordinate of the ball (important if ball leaves the window, to know where its gonna fall down):
                ball_tracking_sign = pygame.Rect(volleyball.coordinates[0] + 6, 10, 5, 5)
                pygame.draw.rect(self.SCREEN, (0, 0, 0), ball_tracking_sign)

                # player controls:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player2.coordinates[0] > 610:
                    player2.move_left()
                if keys[pygame.K_RIGHT] and player2.coordinates[0] < 1118:
                    player2.move_right()
                if keys[pygame.K_d] and player1.coordinates[0] < 510:
                    player1.move_right()
                if keys[pygame.K_a] and player1.coordinates[0] > 0:
                    player1.move_left()
                if keys[pygame.K_w]:
                    player1.start_jump()
                if keys[pygame.K_UP]:
                    player2.start_jump()
                player1.jumps()
                player2.jumps()

            # if volleyball is on Floor or one player had 5 contacts, pause game for 100 frames, give points, start new round
            if volleyball.coordinates[1] > 619 and current_game.check_collisioncounter() is False:
                current_game.running = False
                countdown += 1
                if countdown >= 100:
                    if volleyball.coordinates[0] + 38 < 599:
                        scorer = 2
                    else:
                        scorer = 1
                    current_game.point_made(scorer)
                    volleyball, player1, player2, countdown, current_game.running = self.initialize_new_round(current_game.serve)

            if current_game.check_collisioncounter() is True or run_countdown is True:
                run_countdown = True
                current_game.running = False
                countdown += 1
                if countdown >= 100:
                    run_countdown = False
                    volleyball, player1, player2, countdown, current_game.running = self.initialize_new_round(
                        current_game.serve)

            self.blit_score(current_game.score)

            volleyball, frames_since_col = self.handle_collisions(volleyball, player1, player2, net,
                                                                  frames_since_col, current_game)
            player1.update_coordinate_queue_and_vel()
            player2.update_coordinate_queue_and_vel()

            if current_game.score[0] == 7:
                current_game.winner = 1
            if current_game.score[1] == 7:
                current_game.winner = 2

            if current_game.winner is not None:
                self.blit_winner_text(current_game.winner)
                countdown += 1
                if countdown >= 100:
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            self.run_menu_screen()

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def initialize_new_round(self, serve):
        volleyball = ball.Ball(self)
        if serve == 2:
            volleyball.coordinates = [1000, 400]
        player1 = player.Player("player1.png", [200, 540], self)
        player2 = player.Player("player2.png", [1000, 540], self)
        countdown = 0  # starts increasing after 1 point is over and determines the delay until the next round starts
        running = False
        return volleyball, player1, player2, countdown, running

    def handle_collisions(self, volleyball, player1, player2, net, frames_since_col, current_game):
        """
        Handles collisions of the ball with players and net (Physics + play sound).
        After a collision with a player, there is a amount of frames where the ball can not be
        accelerated again, in order to improve physics.
        """
        ball_sound = self.ball_sound
        collision_acceleration = 20
        volleyball_rect = pygame.Rect(volleyball.coordinates[0] + 11, volleyball.coordinates[1] + 11, 58, 69)
        player1_rect = pygame.Rect(player1.coordinates[0] + 8, player1.coordinates[1] + 4, 60, 105)
        player2_rect = pygame.Rect(player2.coordinates[0] + 10, player2.coordinates[1]+2, 60, 105)

        def accelerate_ball(player_rect, frames_since_col, current_game=current_game):
            refractory_time = 40  # Nr. of frames which have to pass until the function can be executed again
            if volleyball_rect.colliderect(player_rect) and frames_since_col > refractory_time:
                # get vector from player to ball and add standardized acceleration in that direction
                vector = [volleyball_rect.center[0] - player_rect.center[0], volleyball_rect.center[1] - player_rect.center[1]]
                vector = np.asarray(vector)
                unit_vector = vector / np.linalg.norm(vector)
                acceleration_vector = unit_vector*collision_acceleration
                volleyball.velocity[0] = acceleration_vector[0]
                volleyball.velocity[1] = acceleration_vector[1]
                frames_since_col = 0
                ball_sound.play()
                if player_rect == player1_rect:
                    current_game.collision_counter[0] += 1
                    current_game.collision_counter[1] = 0
                else:
                    current_game.collision_counter[0] = 0
                    current_game.collision_counter[1] += 1
            else:
                frames_since_col += 0.5
            return frames_since_col
        frames_since_col = accelerate_ball(player1_rect, frames_since_col)
        frames_since_col = accelerate_ball(player2_rect, frames_since_col)

        if volleyball_rect.colliderect(net):
            volleyball.velocity[0] *= -0.8
            if volleyball_rect.bottom >= net.top and volleyball_rect.center[1] <= net.top:
                volleyball.velocity[1] = -10

        return volleyball, frames_since_col

    def blit_score(self, score):
        p1_score = str(score[0])
        p2_score = str(score[1])
        p1_score_surface = self.BIG_FONT.render(p1_score, True, (0, 0, 0))
        p2_score_surface = self.BIG_FONT.render(p2_score, True, (0, 0, 0))
        self.SCREEN.blit(p1_score_surface, (550, 40))
        self.SCREEN.blit(p2_score_surface, (650, 40))

    def blit_winner_text(self, winner):
        if winner == 1:
            text0 = self.BIG_FONT.render("Congratulations, Blue! You won :)", True, (0, 0, 255))
        else:
            text0 = self.BIG_FONT.render("Congratulations, Red! You won :)", True, (255, 0, 0))
        text1 = self.FONT.render("Press any Key to get back to the menu", True, (0, 0, 0))
        self.SCREEN.blit(text0, (200, 400))
        self.SCREEN.blit(text1, (300, 600))


