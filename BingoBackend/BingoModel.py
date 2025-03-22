import random

class BingoModel:
    def __init__(self):
        self.pattern = '5 IN A ROW'
        self.history = []
        self.pool = []
        self.picked_numbers = set()
        self.picked_dict = dict()
        self.reset_board()
    
    def set_win_pattern(self, pattern):
        self.pattern = pattern
        print(f'Setting win pattern to {pattern}')

    def create_pool(self):
        letters = 'BINGO'
        number = 1
        pool = []
        for letter in letters:
            for _ in range(15):
                pool.append(f'{letter} {number}')
                self.picked_dict[number] = str(number)
                number += 1
        return pool
    
    def check_bingo(self, bingo_picks: list):
        true_bingo = False
        if len(set(bingo_picks.split(', ')) - self.picked_numbers) == 0:
            true_bingo = True
        return true_bingo

    def reset_board(self):
        self.history = []
        self.pool = self.create_pool()
        self.picked_numbers = set()
        random.shuffle(self.pool)
        print("Bingo game reset!")

    def pick_number(self):
        if not self.pool:
            print("All numbers have been picked!")
            return None
        
        picked = self.pool.pop()
        self.history.append(picked)
        self.picked_numbers.add(picked[2:])
        self.picked_dict[int(picked[2:])] = f' {self.picked_dict[int(picked[2:])]} '
        return picked

    def get_recent_history(self, length = 3):
        if len(self.history)<2:
            return ['Pick!']
        else:
            return self.history[-(length+1):-1]

    def get_history(self):
        if len(self.history)==0:
            return []
        else:
            return self.history
        
    def get_last(self):
        if len(self.history)==0:
            return 'Pick!'
        else:
            return self.history[-1]