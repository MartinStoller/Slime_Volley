class Game:
    """
    - Is the game running or over, in wich state is the game
    - What´s the current score
    """
    def __init__(self):
        self.gameover = False # True when the first player has 5 points
        self.running = False  # set to true after first button is pressed (gravity sets in and the game begins), False after each point and at the beginning of a new game
        self.score = [0, 0]