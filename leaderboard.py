# File: leaderboard.py
# Project: BrickIn
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Date: 25 Dec 2023
# Purpose:
#   A simple singleton class for handling the leaderboard.
# Notes:

from os.path import exists, isfile

class Leaderboard:
    __FILE = "brickin.board"
    __INSTANCE = None

    @staticmethod
    def check(score: int) -> bool:
        """Checks the leaderboard and returns true if the given score is a top 10 score."""
        Leaderboard.__create()
        return Leaderboard.__INSTANCE.check_score(score)
    
    @staticmethod
    def register(name: str, score: int):
        """Registers the score with the leaderboard."""
        Leaderboard.__create()
        Leaderboard.__INSTANCE.register_score(name, score)

    @staticmethod
    def quit():
        """Writes out the leaderboard if needed, must be called to save progress."""
        Leaderboard.__create()
        Leaderboard.__INSTANCE.close()

    @staticmethod
    def get_scores() -> ((str, int), ...):
        """Returns a list of string, integer tuples representing the leaderboard scores."""
        Leaderboard.__create()
        return Leaderboard.__INSTANCE.scores

    @staticmethod
    def __create():
        """Creates a new instance of the Leaderboard, if needed."""
        if Leaderboard.__INSTANCE is None:
            Leaderboard.__INSTANCE = Leaderboard()

    def __init__(self):
        self.scores = []
        if exists(Leaderboard.__FILE) and isfile(Leaderboard.__FILE):
            with open(Leaderboard.__FILE) as fin:
                for line in fin:
                    line = line.strip()
                    if line != "":
                        name, score = line.split(',')
                        score = int(score)
                        self.scores.append((name, score))
        while len(self.scores) < 10:
            self.scores.append(("AAA", 0))
        self.changed = False

    def check_score(self, score: int) -> bool:
        """Returns true if the provided score is a high score."""
        for _, curr_score in self.scores:
            if curr_score < score:
                return True
        return False

    def register_score(self, name: str, score: int):
        """Registers the score with the leaderboard."""
        inserted = False
        for idx in range(len(self.scores)):
            if self.scores[idx][1] < score:
                self.scores.insert(idx, (name, score))
                inserted = True
                break
        if inserted:
            self.scores.pop()
            self.changed = True

    def close(self):
        """Closes the leaderboard by writing to its file if needed."""
        if self.changed:
            with open(Leaderboard.__FILE) as fout:
                for name, score in self.scores:
                    print(f"{name}, score", file=fout)
            self.changed = False
