"""
COMP.CS.100 Programming 1

Student id number: 152251723
Creator: Hai Chu
Email: hai.m.chu@tuni.fi


1-player version Jahtzee game
Rules: The player needs to get as many points as possible by rolling five dice
        and the points are calculated based on some combinations of dice.
Gameplay: The player will have 13 turns in total. In each turn, the player
        throw 5 dices up to 3 times. In the second or third throw, the player
        doesn't have to roll all five dice - he/she can hold some dices and roll
        some others.
        In this program, the player clicks on the dice to hold it and then it will
        not be rolled the next time (clicks on it again to remove hold). After
        3 times of rolling, the player has to press five dices to hold all of them.
        At this point, the program will calculate the points player get in all
        combinations. Then, player presses which score they want to save.
Combinations:
    - Upper combinations:
        + Ones: Get as many ones as possible.
        + Twos: Get as many twos as possible.
        + Threes: Get as many threes as possible.
        + Fours: Get as many fours as possible.
        + Fives: Get as many fives as possible.
        + Sixes: Get as many sixes as possible.
    * For the upper combinations, the score for each of them is the sum of the
    dice of the right kind. E.g: If player gets 1,2,2,2,4 and chooses Twos, he/she
    will get 2*3 = 6. The sum of all the upper combinations is calculated and if
    it is 63 or more, the player will get a bonus of 35 points
    - Lower combinations:
        + Three of a kind: Get three dice with the same number.
          Points are the sum all dice (not just the three of a kind).
        + Four of a kind: Get four dice with the same number.
          Points are the sum all dice (not just the four of a kind).
        + Full house: Get three of a kind and a pair. Scores 25 points.
        + Small straight: Get four sequential dice. Scores 30 points.
        + Large straight: Get five sequential dice. Scores 40 points.
        + Chance: Any dices. The score is simply the sum of the dice.
        + YAHTZEE: Five of a kind. Scores 50 points.

About GUI of this program: There is a table of score, which consists of 2 columns.
The first one includes labels, whose texts are name of combinations and sums.
The second one includes buttons, which will show the scores correspond to the
label next to it once 5 dices are held. Also, if the player presses the button,
it will save that value for that turn. There is name of player, which you can
change, and image of cartoon. There is also 4 buttons to operate game and 5 dices

How to run this program: If you encounter the error of not finding such images,
you will have to extract (unzip) the zipped file and then choose right folder
to enter Pycharm. If this stills doesn't solve the problem, please contact me
at hai.m.chu@tuni.fi

For this program, I hope it implement an advanced GUI
"""

from tkinter import *
from tkinter import messagebox
import random
import time

# Image files for the dice faces
IMAGE_FILES = ["image_1.png", "image_2.png", "image_3.png", "image_4.png", "image_5.png", "image_6.png"]\

class Yahtzee:
    # Possible scoring combinations
    upper_combinations = ["Ones", "Twos", "Threes", "Fours", "Fives",
                          "Sixes"]
    lower_combinations = ["Three of a kind", "Four of a kind",
                          "Full house", "Small straight", "Large straight",
                          "Chance", "YAHTZEE"]
    def __init__(self):


        # Creating the main game window
        self.__window = Tk()
        self.__window.title("Yahtzee")


        # Loading dice face images
        self.__dice_faces = [PhotoImage(file=i) for i in IMAGE_FILES]

        #Creating the dices as buttons and placing them by grid. These button
        #will be held and disabled when cliked
        self.__dice_buttons = [Button(self.__window, image=self.__dice_faces[0],
                                    command=lambda a=i: self.hold_dice(a))
                             for i in range(5)]

        for index, button in enumerate(self.__dice_buttons):
            button.configure(bg="#4CAF50", fg="#FFFFFF",
                             borderwidth=2, relief="raised")
            button.grid(row=8, column=8 + index*2, rowspan=2, columnspan=2,
                                padx = 25)

        # Initializing game state variables
        self.__dice_values = [1] * 5  # Start with all dice showing '1'
        self.__dice_held = [False] * 5 # All dices are not held at beggining
        self.__rolls_left = 3
        self.__turns_left = 13   # Total turns for each 1-player Yahtzee game
        combinations = Yahtzee.upper_combinations + Yahtzee.lower_combinations
        self.__combination_score = {}   #Dict with key - combination and payload - score of that combination
        self.__score_history = []   #Save the points of each game for scoreboard

        # Game control buttons
        self.__newgame_button = Button(self.__window, text= "New game",width = 10,
                                      height= 1,font=("Open Sans", 12),
                                       bg="#4CAF50", fg= "#FFFFFF",
                                        command= self.new_game)
        self.__throw_button = Button(self.__window, text= "Throw",width = 5,
                                      height = 1,font=("Open Sans", 12),
                                      bg="#4CAF50", fg="#FFFFFF",
                                      command = self.throw)

        self.__scoreboard_button = Button(self.__window, text="Scoreboard",
                                    width = 5, height = 1,font=("Open Sans", 12),
                                    bg="#4CAF50",fg="#FFFFFF",
                                    command = self.scoreboard)

        self.__quit_button = Button(self.__window, text="Quit",
                                    width = 5, height = 1,font=("Open Sans", 12),
                                    bg="#4CAF50",fg="#FFFFFF",
                                    command = self.quit)

        # Placing game control buttons
        self.__newgame_button.grid(row=4, column=10, columnspan=2, sticky=NSEW)
        self.__throw_button.grid(row=4, column=12, sticky= NSEW)
        self.__scoreboard_button.grid(row=4, column=13, columnspan=3, sticky = NSEW)
        self.__quit_button.grid(row=16, column= 17)

        # Player's name and change name option
        self.__playername_1 = Label(self.__window, text="Player 1",
                                    font=("Open Sans", 13))
        self.__change_name_button = Button(self.__window, text="Change name",
                                           font=("Open Sans", 8), height=0,
                                           command=self.ask_name)
        self.__playername_1.grid(row=1, column=12)
        self.__change_name_button.grid(row=1, column=13, columnspan=2,
                                       sticky=NSEW)

        # Player's image
        self.__player1_image = PhotoImage(file="zyro-image.png")
        self.__image_1 = Label(self.__window, image=self.__player1_image)
        self.__image_1.grid(row=2, column=12, rowspan=2, sticky=N)


        # Player's status
        self.__status = Label(self.__window,
                              text=f"Rolls left: {self.__rolls_left}, Turns left: {self.__turns_left}"
                              , font=("Open Sans", 13))
        self.__status.grid(row=5, column=11, columnspan =3, sticky = NSEW)


        # Score table
        self.__cornertable = Label(self.__window, bg="#DBE8D8", bd=1, relief="solid")
        self.__cornertable.grid(row=0, column=0, columnspan =2, sticky=NSEW)

        # Place name of player
        self.__name_1 = Label(self.__window, text="Player 1",
                              font=("Open Sans", 10), bd=1, relief="solid",
                              width=10, height=2,bg="#DBE8D8")
        self.__name_1.grid(row=0, column=2, sticky=NSEW)

        # Create upper combination labels in first column
        for i, combination in enumerate(Yahtzee.upper_combinations, start=1):
            label = Label(text=combination, relief="solid", font=("Open Sans", "10"),
                            width=13, height=2,bd=1,bg="#DBE8D8")
            label.grid(row=i, column=0, columnspan = 2, sticky=NSEW)

        # Create sum and bonus labels in first column
        self.__sum_upper = Label(text="Sum", relief="solid", font=("Open Sans", "10"),
                                width=13, height=2,bg="#DBE8D8")
        self.__sum_upper.grid(row=len(Yahtzee.upper_combinations) + 1, column=0,
                              columnspan = 2, sticky=NSEW)
        self.__bonus = Label(text="Bonus", relief="solid", font=("Open Sans", "10"),
                             width = 13, height=2, bg="#DBE8D8")
        self.__bonus.grid(row=len(Yahtzee.upper_combinations) + 2, column=0,
                          columnspan = 2, sticky=NSEW)

        # Create lower combination labels in first column
        for i, combination in enumerate(Yahtzee.lower_combinations,                  #The row of these labels will be rows of upper
                                        start=len(Yahtzee.upper_combinations) + 3):  #combinations + 1 (of sum label) + 1 (of bonus label) + 1
            label = Label(text=combination, relief="solid", font=("Open Sans", "10"),
                            width=13, height=2, bd=1,bg="#DBE8D8")
            label.grid(row=i, column=0, columnspan = 2, sticky=NSEW)

        # Create total score label
        self.__total_score = Label(text="TOTAL SCORE", relief="solid", bg="#DBE8D8"
                                    ,font=("Open Sans", "10"), width=13,height=2)
        self.__total_score.grid(
            row=len(Yahtzee.upper_combinations) + len(Yahtzee.lower_combinations) + 3,
            column=0, columnspan = 2, sticky=NSEW)

        #Set up buttons in second column. The buttons will show scores
        #correspond to the label next to it once the dices are held.
        #Also, if the player choose that combination, it is disabled and return the result

        # A list will contain the all the score buttons except for the sum,
        # bonus, total one as they are calculated in different way
        self.__score_buttons = []

        row = 1
        for i in Yahtzee.upper_combinations:
            button = Button(self.__window, font=("Open Sans", 10), bd=1, relief="solid",
                            width=10, height=2,bg="#DBE8D8")
            button["command"] = lambda button=button,i=i: self.save_dice(button,i)
            button.grid(row=row, column=2, padx=0.1, pady=0.1, sticky=NSEW)
            row+= 1
            self.__score_buttons.append(button)

        self.__sum_button = Button(self.__window, font=("Open Sans", 10), bd=2, relief="solid",
                                   width=10, height=2, state="disabled", bg="#DBE8D8")
        self.__sum_button.grid(row=7, column=2, padx=0.1, pady=0.1, sticky=NSEW)
        self.__bonus_button = Button(self.__window, font=("Open Sans", 10), bd=2, relief="solid",
                                     width=10, height=2, state="disabled", bg="#DBE8D8")
        self.__bonus_button.grid(row=8, column=2, padx=0.1, pady=0.1, sticky=NSEW)

        r=9
        for i in Yahtzee.lower_combinations:
            button = Button(self.__window, font=("Open Sans", 10), bd=1, relief="solid",
                            width=10, height=2,bg="#DBE8D8")
            button["command"] = lambda button=button, i=i: self.save_dice(button,i)
            button.grid(row=r, column=2, padx=0.1, pady=0.1, sticky=NSEW)
            r+= 1
            self.__score_buttons.append(button)

        self.__total_score_button = Button(self.__window, font=("Open Sans", 10),
                                           bd=2, relief="solid", width=10, height=2,
                                           state = "disabled", bg="#DBE8D8")
        self.__total_score_button.grid(row=16, column=2, padx=0.1, pady=0.1, sticky=NSEW)

        #Start the loop
        self.__window.mainloop()

    def ask_name(self):
        # Create a new top-level window
        name_window = Toplevel(self.__window)
        name_window.title("Change Name")

        # Entry widget to type in player's name
        name_entry = Entry(name_window)
        name_entry.pack(padx=10, pady=10)

        #Set the name and close the new top-level window
        def set_name():
            if name_entry.get().strip():
                self.player_name = name_entry.get().strip()
            else:
                self.player_name = "Player 1"
            self.__playername_1.configure(text=self.player_name)
            self.__name_1.configure(text=self.player_name)
            name_window.destroy()

        # Button to submit the new name
        submit_button = Button(name_window, text="Submit", command=set_name)
        submit_button.pack(padx=10, pady=10)

        #Direct the user to interact with this top-level window
        name_window.grab_set()
        name_window.wait_window()
    def new_game(self):
        self.__dice_values = [1] * 5  # Reset dice values
        self.__dice_held = [False] * 5  # Reset all dice to not held
        self.__rolls_left = 3  # Reset the number of rolls
        self.__turns_left = 13
        self.__combination_score = {}
        self.__throw_button["state"] = "normal"

        for dice_button in self.__dice_buttons:
            dice_button.configure(state="normal")
            dice_button["bg"] = "#4CAF50"

        for score_button in self.__score_buttons:
            score_button["text"] = ""
            score_button["state"] = "normal"

        self.__sum_button["text"] = ""
        self.__bonus_button["text"] = ""
        self.__total_score_button["text"] = ""

        self.__status["text"] = f'Rolls left: {self.__rolls_left}, ' \
                                f'Turns left: {self.__turns_left}'
        self.update_dice()

    # This method will operate on all attribute when player throw the dices
    def throw(self):
        # Error for the situation when player has rolled 3 times
        if self.__rolls_left <= 0:
            messagebox.showinfo("No Throws Left",
                                "You have no throws left for this turn.")
            return

        # Create the random values for dices and show that with animation
        for i in range(10):
            for a in range(0,5):
                if not self.__dice_held[a]:
                    self.__dice_values[a] = random.randint(1, 6)
                    self.__dice_buttons[a]["image"] = self.__dice_faces[self.__dice_values[a] - 1]

            self.__window.update_idletasks()

            time.sleep(0.05)

        # Reset in the situation that player hold 5 dices and the values are shown
        for score_button in self.__score_buttons:
            if score_button["state"] == "normal":
                score_button["text"] = ""

        # Update status
        self.__rolls_left -= 1
        self.__status[
            "text"] = f'Rolls left: {self.__rolls_left}, Turns left: {self.__turns_left}'

    # This method will operate when player presses the dices to hold it
    def hold_dice(self, dice_index):
        # Error for the situation when player has not yet rolled the dices
        if self.__rolls_left == 3:
            messagebox.showinfo("Roll First",
                                "You need to roll the dice before you can hold.")
            return

        # Update which dices are being held
        self.__dice_held[dice_index] = not self.__dice_held[dice_index]

        # Set 2 state (held and not held) to 2 colors to see better which one is held
        if self.__dice_held[dice_index]:
            self.__dice_buttons[dice_index]["bg"] = "#ADD8E6"
        else:
            self.__dice_buttons[dice_index]["bg"] = "#4CAF50"

        self.calculate_score()
        self.update_dice()

    def calculate_score(self):
        # This make sure that only dices which are held are calculated
        if self.__dice_held != [True] * 5:
            return

        #Formula for upper combinations scores
        self.ones_score = self.__dice_values.count(1)
        self.twos_score = 2 * self.__dice_values.count(2)
        self.threes_score = 3 * self.__dice_values.count(3)
        self.fours_score = 4 * self.__dice_values.count(4)
        self.fives_score = 5 * self.__dice_values.count(5)
        self.sixes_score = 6 * self.__dice_values.count(6)

        self.three_of_kind = 0
        self.four_of_kind = 0
        self.sm_straight_score = 0
        self.la_straight_score = 0
        self.YAHTZEE_score = 0
        self.full_house_score = 0

        for i in set(self.__dice_values):
            count = self.__dice_values.count(i)
            if count == 3 and len(set(self.__dice_values)) == 2: # This happens only when it is full house
                self.full_house_score = 25
            if count >= 3:
                self.three_of_kind = sum(self.__dice_values)

            if count >= 4:
                self.four_of_kind = sum(self.__dice_values)

            if count == 5:
                self.YAHTZEE_score = 50


        small_straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        large_straights = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]

        for i in small_straights:
            if i.issubset(set(self.__dice_values)):
                self.sm_straight_score = 30           # Use .issubset method to
                                                      # identify if it is small
        for i in large_straights:                     # straight or large one
            if i.issubset(set(self.__dice_values)):
                self.la_straight_score = 40

        self.chance_score = sum(self.__dice_values)    # Chance is the sum of
                                                       # all dices values

        # Save all the scores in a list
        all_score = [self.ones_score, self.twos_score, self.threes_score,
                     self.fours_score, self.fives_score, self.sixes_score,
                     self.three_of_kind, self.four_of_kind,self.full_house_score,
                     self.sm_straight_score,self.la_straight_score,self.chance_score,
                     self.YAHTZEE_score]

        # Update the score button text when 5 dices are held
        a = -1
        for i in self.__score_buttons:
            a += 1
            if i["state"] != "disabled":
                i["text"] = all_score[a]

    def update_dice(self):
        for i, button in enumerate(self.__dice_buttons):
            button["image"] = self.__dice_faces[self.__dice_values[i] - 1]
            button["relief"] = "sunken" if self.__dice_held[i] else "raised"

    # This method to save score when player press the score button
    def save_dice(self, button, combination):
        # This handles error when player doesn't roll
        if button["text"] == "":
            messagebox.showinfo("Roll First",
                                "You need to roll the dice to get points")
            return

        # When player saves value, that button will be disabled
        button["state"] = "disabled"

        # Save the combination and its score to the dictionary implemented intially
        self.__combination_score[combination] = button["text"]

        # Update status
        self.__turns_left -= 1
        if self.__turns_left <= 0:
            self.__throw_button["state"] = "disabled"
        self.__status[
            "text"] = f'Rolls left: {self.__rolls_left}, Turns left: {self.__turns_left}'

        self.next_turn()

    # This method decides which is next step
    def next_turn(self):
        # If player played all 13 turns, it will calculate the sum,bonus and total score
        if self.__turns_left == 0:
            self.sum_score = 0
            self.bonus_score = 0

            # Calculate sum score, which is the sum of upper combinations
            for i in Yahtzee.upper_combinations:
                self.sum_score += self.__combination_score[i]

            # Calculate bonus
            if self.sum_score >= 63:
                self.bonus_score = 35

            # Calculate total score, which is the sum of sum_score and lower combinations scores
            self.total_score = self.sum_score
            for i in Yahtzee.lower_combinations:
                self.total_score += self.__combination_score[i]

            # Update the sum,bonus, total score
            self.__sum_button["text"] = self.sum_score
            self.__bonus_button["text"] = self.bonus_score
            self.__total_score_button["text"] = self.total_score

            # Save the total score for score board
            self.__score_history.append(self.total_score)
        else:
            # If player doesn't finish all the turns, the game will reset partly
            # some variables and continue
            self.__dice_values = [1] * 5  # Reset dice values
            self.__dice_held = [False] * 5  # Reset all dice to not held
            self.__rolls_left = 3  # Reset the number of rolls

            for dice_button in self.__dice_buttons:
                dice_button.configure(state="normal", bg = "#4CAF50")

            for score_button in self.__score_buttons:
                if score_button["state"] != "disabled":
                    score_button["text"] = ""

            self.__status[
                "text"] = f'Rolls left: {self.__rolls_left}, Turns left: {self.__turns_left}'
            self.update_dice()

    # This method will show the scoreboard after each game
    def scoreboard(self):
        #This handle error when player has not finished a game yet
        if not self.__score_history:
            messagebox.showinfo("Scoreboard", "You have not played any round")
        else:
            history_text = ""
            for i, score in enumerate(self.__score_history):
                if i > 0:
                    history_text += "\n"   #This to make sure that each game score on a different line
                history_text += f'Round {i+1}: {score}'
            messagebox.showinfo("Scoreboard", history_text)

    def quit(self):
        self.__window.destroy()

def main():
    Yahtzee()


if __name__ == "__main__":
    main()