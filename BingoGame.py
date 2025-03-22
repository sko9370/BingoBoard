from BingoModel import BingoModel

class BingoGame:
    def __init__(self):
        self.model = BingoModel()
        self.game_loop()

    def game_loop(self):
        control = ''
        while control != 'exit':
            print('Type "pick", "history", "restart", or "exit"')
            control = input('Enter next command: ')
            if control in ['p', 'pick']:
                self.pick_number()
            elif control in ['r', 'restart']:
                self.reset_board()
            elif control in ['h', 'history']:
                print(self.model.get_history())
            else:
                print('Not a valid choice, try again')
    
    def pick_number(self):
        print(self.model.get_recent_history())
        print(self.model.pick_number())
    
    def reset_board(self):
        self.model.reset_board()

if __name__ == "__main__":
    bingo_game = BingoGame()