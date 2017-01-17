from game import *
import random


class Hangman(Player):
    """
    Models a hangman player
    """

    def __init__(self, name):
        """
        Initialize the object
        :param name: str - name of player
        :return: None
        """

        super(Hangman, self).__init__(name)
        self.hm_word = ""
        self.hm_guess = ""
        self.hm_length = 0

    def intro(self):
        """
        Outputs introduction
        :return: None
        """

        print ""
        print "*" * 30
        print "{0:^30}".format("HANGMAN")
        print "*" * 30
        print "{0:^30}".format("Guess the mystery word to win!\nTopic: Computer Science")
        print """
        _______
        |/   |
        |   (_)
        |   \|/
        |    |
        |   / \\
        |
       _|___
            """

    def random_word(self):
        """
        Generates a random word
        :return: None
        """

        pos_words = ["POLYMORPHISM", "PSEUDOCODE", "SCOPE", "RECURSION", "COMPILATION",
                     "CONCATENATION", "CONDITIONAL", "ENCAPSULATION", "INHERITANCE", "IMMUTABILITY"]
        self.hm_word = pos_words[random.randint(0, 9)]

    def user_guess(self):
        """
        Allows to user guess a letter
        :return: str - user's guess
        """

        print ""
        self.hm_guess = raw_input(">>> Guess a letter (from A - Z): ").upper()
        return self.hm_guess

    def get_guess(self):
        """
        Returns user's guessed letter
        :return: str

        """

        return self.hm_guess

    def get_word(self):
        """
        Returns the word picked
        :return: str
        """

        return self.hm_word

    def __str__(self):
        """
        String representation of a Player
        :return: Name of the player
        """

        return self.name


class PlayMode(object):
    """
    Checks the mode the user wants to play
    :param mode: str - the chosen mode
    :param name: str - name of player
    :return: None
    """
    def __init__(self, mode, name):
        self.mode = mode
        self.name = name

    def check_mode(self):

        # checks the mode of the game
        if self.mode.lower() == "n" or self.mode.lower() == "normal" \
                or self.mode.lower() == "u" or self.mode.lower() == "unlimited":

            # plays the game in the proper mode
            if self.mode.lower() == "n" or self.mode.lower() == "normal":
                my_hm = HangmanGame(self.name)

            elif self.mode.lower() == "u" or self.mode.lower() == "unlimited":
                my_hm = TwentySixHangman(self.name)

            # plays the game in chosen mode, finds the result
            my_hm.play()
            my_hm.get_result()

        else:

            # asks for valid input
            print "Please enter a valid mode."
            mode = raw_input("Pick a game mode. Enter normal(n) or unlimited(u): ")
            play = PlayMode(mode, self.name)
            play.check_mode()


class HangmanGame(Game):
    """
    Models a 'normal' hangman game
    """

    def __init__(self, name):
        """
        Game object constructor
        :param name: str - name of the game player
        :return: None
        """

        # initialize the player instance, lives, guesses
        self.player = Hangman(name)
        self.guess_num = 0
        self.lives_used = 0
        self.extra_life = True

    def __intro(self):
        """
        Print the game instructions
        :return: None
        """
        answer = raw_input("Press enter to continue: ")
        if answer == "":
            print "\nInstructions:\n- Pick a letter you think is in the word."
            print "- For normal mode, you have 10 chances to guess the word."
            print "- Every time you guess incorrectly, a part of the hangman will be drawn."
            print "- Enter quit if you give up and want to end the game.\nGood luck!"

    def __body_part(self, body_count):
        """
        Updates which body parts are drawn
        :param body_count: int - the body part being drawn
        :return: None
        """

        # tells user the body part being drawn
        body_parts = ["A head", "The body", "The left arm", "The right arm", "The left leg",
                      "The right left", "The left eye", "The right eye", "The nose", "The mouth", "Nothing"]
        print "Sorry, that letter is NOT in the word. "
        print body_parts[body_count] + " has been drawn."

    def __fill_blanks(self, visual_word, locations):
        """
        Updates what the user has guessed
        :param visual_word: list - the letters the user guessed
        :param locations: list - where the letter guessed is
        :return: None
        """

        # initialize variables
        visual_word_str = ""
        word = self.player.get_word()

        if not locations:

            # create empty word user fills in
            blanks_word = "_" * len(word)
            visual_word = list(blanks_word)

            # formats the word
            s = " "
            visual_word_str = s.join(visual_word)

        else:
            for y in locations:
                # puts correct letters guessed in their locations
                visual_word[y] = word[y]

                # formats the word
                s = " "
                visual_word_str = s.join(visual_word)

        print visual_word_str

    def __check_word(self, locations, body_count):
        """
        Checks if the guessed letter is correct
        :param locations: list - locations of correct letters
        :param body_count: int - number of incorrect guesses
        :return: locations - updated location of letters
        :return: body_count - updated number of guesses
        """

        # gets user's guess and correct word
        user_guess = self.player.get_guess()
        word = self.player.get_word()

        for x in range(len(word)):

            # checks if letter guessed in word
            if user_guess == word[x]:

                # puts location of letter in list
                location = x
                locations.append(location)

            elif user_guess not in word:

                # prints the body part drawn
                self.__body_part(body_count)

                # updates number of wrong guesses
                body_count += 1
                self.lives_used += 1
                break

        return locations, body_count

    def play(self):
        """
        Play the game
        :return: None
        """

        # initialize variables
        guess_list = []
        locations = []
        body_count = 0

        # finds word to be guessed
        self.player.random_word()
        word = self.player.get_word()

        # prints instructions
        self.player.intro()
        self.__intro()

        # create empty word to be guessed
        blanks_word = "_" * len(word)
        visual_word = list(blanks_word)

        # run as long user guessed < 10 wrong and word not guessed
        while self.lives_used <= 10 and "_" in visual_word:

            # if all the lives are used, let user answer a riddle
            if self.lives_used == 10 and "_" in visual_word and self.extra_life:
                print ""
                print "Sorry you have no more lives left."
                print "Answer this riddle for an extra life."
                user = TryAgain()
                user_answer = user.questions()

                if user_answer:

                    # if user answers correctly, give them a life
                    self.lives_used = 9

                    # let the user answer the riddle once
                    self.extra_life = False

                else:

                    # if the user is incorrect, end the game
                    break

            # if the user has used 10 lives, end the game
            elif self.lives_used == 10:
                break

            # outputs which letters have been guessed
            if self.guess_num > 0:
                s = " "
                print ""
                print "-" * 26
                print "Letter(s) guessed already:", s.join(guess_list)
                print "-" * 26

            # prints how many more times users can guess
            print "\nYou have", 10 - self.lives_used, "chance(s) left."

            # asks user for a letter
            user_guess = self.player.user_guess().upper()

            # if the user puts quit, end game
            if user_guess == "QUIT":
                self.lives_used = 10
                break

            # if the letter is already guessed
            while user_guess in guess_list:

                # tell user, let them guess again
                print "You have already guessed that letter. Please make another guess."
                user_guess = self.player.user_guess().upper()

            else:
                # increase the number of guesses
                self.guess_num += 1

            # adds guess to list of guesses
            print ""
            guess_list.append(user_guess)

            # updates word the user is guessing, penalizes user if incorrect
            locations, body_count = self.__check_word(locations, body_count)
            self.__fill_blanks(visual_word, locations)

    def get_result(self):
        """
        Checks if the user has won
        :return: None
        """

        # gets player name
        name = self.player.name

        # check if user has won
        if self.lives_used < 10:
            print ""
            print "*" * 10 + "*" * len(name) + "*" * 10
            print "Good job", name, "you WIN!"
            print "*" * 10 + "*" * len(name) + "*" * 10

        else:
            print ""
            print "*" * 29 + "*" * len(self.player.get_word()) + "*" * 2
            print "Sorry, you lost. " + self.__str__()
            print "Try again " + str(name) + "?"
            print "*" * 29 + "*" * len(self.player.get_word()) + "*" * 2

    def __str__(self):
        """
        String output of the object
        :return: str
        """
        return "The word is " + str(self.player.get_word()) + "."


class TwentySixHangman(Game):
    """
    Models a 'unlimited' guesses hangman game
    """

    def __init__(self, name):
        """
        Game object constructor
        :param name: name of game player
        :return: None
        """

        # initialize the player instance, lives, guesses
        self.player = Hangman(name)
        self.guess_num = 0
        self.visual_word = []

    def __intro(self):
        """
        Prints instructions
        :return: None
        """

        print "\nInstructions:\n- Pick a letter you think is in the word."
        print "- For the unlimited mode, you have an unlimited amount of guesses.\n- No hangman will be drawn."
        print "- Enter quit if you give up and want to end the game.\nGood luck!"

    def __fill_blanks(self, locations):
        """
        Updates the user's guesses visually
        :param locations: list - location of correct letters
        :return: None
        """

        # initialize variables
        word = self.player.get_word()
        visual_word_str = ""
        s = " "

        if not locations:

            # make a empty word for user to guess
            visual_word_str = s.join(self.visual_word)

        else:
            for y in locations:
                # adds a correct letter to designated spot
                self.visual_word[y] = word[y]
                visual_word_str = s.join(self.visual_word)

        print visual_word_str

    def __check_word(self, locations):
        """
        Checks if letter entered is right
        :param locations: list - locations of correct letters
        :return: updated list of locations
        """

        # initialize variables
        user_guess = self.player.get_guess()
        word = self.player.get_word()

        for x in range(len(word)):

            # checks to see if the letter guessed is correct
            if user_guess == word[x]:
                # if so, add the location to the list
                location = x
                locations.append(location)

        return locations

    def __init_visual_word(self):
        """
        Creates a blank word to be guessed
        :return: None
        """

        # number of blanks added according to correct word
        word = self.player.get_word()
        blanks_word = "_" * len(word)
        self.visual_word = list(blanks_word)

    def play(self):
        """
        Plays game
        :return: None
        """

        # initialize lists
        guess_list = []
        locations = []
        self.player.random_word()

        # prints instructions
        self.player.intro()
        self.__intro()
        self.__init_visual_word()

        # checks to see if entire word has been guessed
        while "_" in self.visual_word:

            # asks user for letter
            user_guess = self.player.user_guess().upper()

            # checks to see if the user wants to quit
            if user_guess == "QUIT":
                break

            # checks if inputted letter is already guessed
            while user_guess in guess_list:
                print "You have already guessed that letter. Please make another guess."
                print ""
                user_guess = self.player.user_guess().upper()

            # adds user guess to total list of guessed letters
            guess_list.append(user_guess)

            # if letter correct, adds location of the correct letter
            locations = self.__check_word(locations)

            # if letter correct, adds the letter to its location
            self.__fill_blanks(locations)

            # outputs all the letters already guessed
            s = " "
            print "-" * 26
            print "Letter(s) guessed already:", s.join(guess_list)
            print "-" * 26

    def get_result(self):
        """
        Checks to see if the user has won/lost
        :return: None
        """

        # gets name of player
        name = self.player.name

        # checks to see if the entire word is found
        if "_" not in self.visual_word:

            # if so, congratulate the player
            print ""
            print "*" * 10 + "*" * len(name) + "*" * 10
            print "Good job " + str(name) + ", you WIN!"
            print "*" * 10 + "*" * len(name) + "*" * 10

        else:

            # outputs correct word, asks to play again
            print ""
            print "*" * 29 + "*" * len(self.player.get_word()) + "*" * 2
            print "Sorry, you lost. " + self.__str__()
            print "Try again " + str(name) + "?"
            print "*" * 29 + "*" * len(self.player.get_word()) + "*" * 2

    def __str__(self):
        """
        String output of the object
        :return: str - the correct word
        """
        return "The word is " + str(self.player.get_word()) + "."


class TryAgain(object):
    """
    Lets the user get another life
    """

    def __init__(self):
        """
        Object constructor
        :return: None
        """

        # initialize variables
        self.riddle_list = []

    def questions(self):
        """
        Riddle questions and answers
        :return: None
        """

        # gets riddle questions and answers from text file
        self.riddle_list = (open("riddle_questions.txt", "r")).readlines()

        # pick a random riddle
        rand_riddle = random.randrange(0, 19, 6)

        # display riddle question and answer options
        print "\n{0}".format((" ".join(self.riddle_list[rand_riddle].split())))
        print "A) {0}".format((" ".join(self.riddle_list[rand_riddle + 1].split())))
        print "B) {0}".format((" ".join(self.riddle_list[rand_riddle + 2].split())))
        print "C) {0}".format((" ".join(self.riddle_list[rand_riddle + 3].split())))
        print "D) {0}".format((" ".join(self.riddle_list[rand_riddle + 4].split())))

        # initialize variables
        user_ans = ""

        while True:

            # ask for user input
            user_ans = raw_input("\nChoose the correct answer. Pick a, b, c, or d: ")

            # checks if the user entered a valid response
            if user_ans.lower() != "a" and user_ans.lower() != "b" and user_ans.lower() != "c" \
                    and user_ans.lower() != "d":
                print "Please enter a valid selection."
                continue
            break

        # check if the answer is correct
        correct_ans = "".join(((self.riddle_list[rand_riddle + 5]).split()))

        if correct_ans == user_ans.lower():
            print "Congrats you got another chance to play."
            return True
        else:
            print "Sorry, you answered incorrectly. The correct answer was " + str(correct_ans.upper()) + "."
            return False


def main():
    """
    Main executable code
    :return: None
    """

    your_name = raw_input("Please enter your name: ")
    mode = raw_input("Pick a game mode. Enter normal(n) or unlimited(u): ")
    play = PlayMode(mode, your_name)
    play.check_mode()

main()