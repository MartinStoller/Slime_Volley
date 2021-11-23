import pygame
import helper_functions
from collections import deque


class Player:
    def __init__(self, img_name, coordinates, GUI):
        self.img_name = img_name
        self.coordinates = coordinates
        self.max_jumpspeed = 26
        self.current_jump_speed = self.max_jumpspeed
        self.GUI = GUI
        self.jump = False
        self.coordinate_queue = deque([coordinates, coordinates, coordinates])  # stores the coordinates of current + the 2 previous frames
        self.i = 0  # needed for queue
        self.velocity = [int((self.coordinate_queue[0][0] - self.coordinate_queue[2][0]) / 2),
                            int((self.coordinate_queue[0][1] - self.coordinate_queue[2][1]) / 2)]
    
    def render(self):
        player_img = pygame.image.load(helper_functions.get_img_loc(self.img_name))
        self.GUI.SCREEN.blit(player_img, pygame.rect.Rect(self.coordinates[0], self.coordinates[1], 70, 100))

    def jumps(self):
        if self.jump is True:
            self.coordinates[1] -= self.current_jump_speed
            self.current_jump_speed -= 1
            if self.current_jump_speed < -1 * self.max_jumpspeed:
                self.jump = False
                self.current_jump_speed = self.max_jumpspeed

    def update_coordinate_queue_and_vel(self):
        x = int(self.coordinates[0])
        y = int(self.coordinates[1])
        self.coordinate_queue.appendleft([x, y])
        self.coordinate_queue.pop()
        self.velocity = [int((self.coordinate_queue[0][0] - self.coordinate_queue[2][0]) / 2),
                         int((self.coordinate_queue[0][1] - self.coordinate_queue[2][1]) / 2)]


