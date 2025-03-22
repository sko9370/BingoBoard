import random

class BingoModel:
    def __init__(self):
        self.pattern = ''
        self.history = []
        self.pool = []
        self.reset_board()
    
    def set_win_pattern(self, pattern):
        self.pattern = pattern

    def create_pool(self):
        letters = 'BINGO'
        number = 1
        pool = []
        for letter in letters:
            for _ in range(15):
                pool.append(f'{letter} {number}')
                number += 1
        return pool

    def reset_board(self):
        self.history = []
        self.pool = self.create_pool()
        random.shuffle(self.pool)
        print("Bingo game reset!")

    def pick_number(self):
        if not self.pool:
            print("All numbers have been picked!")
            return None
        
        picked = self.pool.pop()
        self.history.append(picked)
        return picked

    def get_recent_history(self, length = 3):
        return self.history[-(length+1):-1]

    def get_history(self):
        return self.history