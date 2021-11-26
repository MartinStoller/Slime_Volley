class Game:
    """
    - Is the game running or over, in wich state is the game
    - What´s the current score
    """
    def __init__(self):
        self.running = False  # set to true after first button is pressed (gravity sets in and the game begins), False after each point and at the beginning of a new game
        self.score = [0, 0]
        self.serve = 1  # 1 if player 1 serves/served the current point, 2 otherwise
        self.collision_counter = [0, 0]  # each player is allowed to touch the ball 5 times in a row max
        self.winner = None  # None if game is not over, 1 if player1 is winner, 2 if player2 is winner

    def point_made(self, scorer):
        if scorer == 1:
            self.score[0] += 1
            self.collision_counter = [0, 0]
        if scorer == 2:
            self.score[1] += 1
            self.collision_counter = [0, 0]
        if 5 in self.score:
            self.gameover = True
        if self.serve == 1:
            self.serve = 2
        else:
            self.serve = 1

    def check_collisioncounter(self):
        """
        check if any player has 5 touches in a row. If yes, give point to other player.
        :return: True if one player had 5 ball contacts in a row.
        """
        if self.collision_counter[0] == 5:
            self.point_made(scorer=2)
            return True
        if self.collision_counter[1] == 5:
            self.point_made(scorer=1)
            self.running = False
            return True
        return False
