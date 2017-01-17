class Player(object):
    """
    A generic model of a player within a game
    """

    def __init__(self, name):
        """
        Initializes the Player object
        :return None
        """

        self.name = name
        self.score = 0

    def __str__(self):
        """
        String representation of a Player
        :return:
        """
        pass  # implement this method in your extension (child) of this class




class Game(object):
    """
    A generic model of a game
    """


    def __init__(self,name):
        """
        Game object constructor
        :param first_name: str - first name of the game player
        :param last_name: str - last name of the game player
        """
        self.player = Player(name)


    def play(self):
        """
        Stub method to be implemented in a child

        :return: None
        """
        pass  # implement this method in your extension (child) of this class


    def __str__(self):
        """
        String representation of a Game, use this for presenting the status of the game
        :return:
        """
        pass  # implement this method in your extension (child) of this class