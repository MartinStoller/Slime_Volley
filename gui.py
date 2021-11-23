import time
import pygame
import helper_functions
import Button
import sys
import ball
import game
import player

class GUI:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("Marty´s Coding Palace: Slime Volley")
    FPS = 75
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    FONT = pygame.font.SysFont('bahnschrift', 30)
    BIG_FONT = pygame.font.SysFont('bahnschrift', 55)
    CLOCK = pygame.time.Clock()
    WIDTH, HEIGHT = 1200, 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SOUND = pygame.mixer.Sound(helper_functions.get_img_loc("ball_hits_sth_sound.wav"))

    def run_menu_screen(self):
        """
        Shows menu to the user. The menu is what you see, after starting the game file.
        There is only one Button needed: Start game
        """
        button_start = Button.Button("Start", "Game", 200, 120, (740, 550), screen=self.SCREEN,
                                     clock=self.CLOCK, elevation=6, GUI_object=self)
        menu_img = pygame.image.load(helper_functions.get_img_loc("menu_pic_final.png"))

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
        volleyball, player1, player2, countdown, current_game.running = self.initialize_new_round()
        play_background_img = pygame.image.load(helper_functions.get_img_loc("playing_pitch.png"))

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
                # player controls:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player2.coordinates[0] > 610:
                    player2.coordinates[0] -= 6
                if keys[pygame.K_RIGHT] and player2.coordinates[0] < 1118:
                    player2.coordinates[0] += 6
                if keys[pygame.K_d] and player1.coordinates[0] < 510:
                    player1.coordinates[0] += 6
                if keys[pygame.K_a] and player1.coordinates[0] > 0:
                    player1.coordinates[0] -= 6
                if keys[pygame.K_w]:
                    player1.jump = True
                if keys[pygame.K_UP]:
                    player2.jump = True
                player1.jumps()
                player2.jumps()

            if volleyball.coordinates[1] > 619:
                current_game.running = False
                countdown += 1
                if countdown >= 100:
                    # TODO: give point to correct player
                    volleyball, player1, player2, countdown, current_game.running = self.initialize_new_round()

            # shows the y coordinate of the ball (important if ball leaves the window, to know where its gonna fall down):
            ball_tracking_sign = pygame.Rect(volleyball.coordinates[0] + 6, 10, 5, 5)
            pygame.draw.rect(self.SCREEN, (0, 0, 0), ball_tracking_sign)

            # volleyball_rect = pygame.Rect(volleyball.coordinates[0]+6, volleyball.coordinates[1]+11, 50, 67)
            # player1_rect = pygame.Rect(player1.coordinates[0]+8, player1.coordinates[1]+4, 60, 105)
            # player2_rect = pygame.Rect(player2.coordinates[0] + 10, player2.coordinates[1]+2, 60, 105)
            # pygame.draw.rect(self.SCREEN, (255, 0, 0), volleyball_rect)
            # pygame.draw.rect(self.SCREEN, (255, 0, 0), player1_rect)
            # pygame.draw.rect(self.SCREEN, (25, 255, 0), player2_rect)
            volleyball = self.handle_p2b_collisions(volleyball, player1, player2)
            player1.update_coordinate_queue_and_vel()
            player2.update_coordinate_queue_and_vel()

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def initialize_new_round(self):
        volleyball = ball.Ball(self)
        player1 = player.Player("player1.png", [200, 540], self)
        player2 = player.Player("player2.png", [1000, 540], self)
        countdown = 0  # starts increasing after 1 point is over and determines the delay until the next round starts
        running = False
        return volleyball, player1, player2, countdown, running

    def handle_p2b_collisions(self, volleyball, player1, player2):
        collision_acceleration = 20
        max_acceleration = 30
        volleyball_rect = pygame.Rect(volleyball.coordinates[0] + 6, volleyball.coordinates[1] + 11, 50, 67)
        player1_rect = pygame.Rect(player1.coordinates[0] + 8, player1.coordinates[1] + 4, 60, 105)
        player2_rect = pygame.Rect(player2.coordinates[0] + 10, player2.coordinates[1]+2, 60, 105)
        if volleyball_rect.colliderect(player1_rect):
            # get vector from player to ball and add standardized acceleration in that direction
            vector = [volleyball_rect.center[0] - player1_rect.center[0], volleyball_rect.center[1] - player1_rect.center[1]]
            unit_vector = vector / (vector**2).sum()**0.5
            print(unit_vector*20)
        if volleyball_rect.colliderect(player2_rect):
            volleyball.velocity = player2.velocity

        return volleyball







