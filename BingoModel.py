import random

class BingoModel:
    def __init__(self):
        self.pattern = '5 in a row'
        self.history = []
        self.pool = []
        self.reset_board()

    def create_pool(self):
        B_vals = [('B', i) for i in range(1, 16)]
        I_vals = [('I', i) for i in range(16, 31)]
        N_vals = [('N', i) for i in range(31, 46)]
        G_vals = [('G', i) for i in range(46, 61)]
        O_vals  = [('O', i) for i in range(61, 76)]
        pool = B_vals + I_vals + N_vals + G_vals + O_vals
        return pool

    def reset_board(self):
        self.history = []
        self.pool = self.create_pool()
        random.shuffle(self.pool)  # Shuffle the pool to randomize the order
        print("Bingo game reset!")

    def pick_number(self):
        if not self.pool:
            print("All numbers have been picked!")
            return None
        
        picked = self.pool.pop()
        self.history.append(picked)
        return picked

    def get_recent_history(self, length = 3):
        return self.history[-3:]

    def get_history(self):
        """Returns the history of picked numbers."""
        return self.history