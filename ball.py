import pygame
import helper_functions


class Ball:
    def __init__(self, GUI):
        self.coordinates = [200, 400]
        self. velocity = [0, 0]
        self.acceleration = [0, 0.5]
        self.GUI = GUI
        self.ball_img = pygame.image.load(helper_functions.get_img_loc("head_ball2.png"))
        self.ball_img.convert()

    def render(self):
        self.GUI.SCREEN.blit(self.ball_img, pygame.rect.Rect(self.coordinates[0], self.coordinates[1], 40, 50))
    
    def move(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if 5 > self.coordinates[0] or 1115 < self.coordinates[0]:
            self.velocity[0] *= -0.8

        try:
            self.coordinates[0] = int(self.coordinates[0] + self.velocity[0])
        except:
            pass
        
        if self.coordinates[1] > 620:
            self.velocity[1] = 0
        try:
            self.coordinates[1] = int(self.coordinates[1] + self.velocity[1])
        except:
            pass
        
