from BingoModel import BingoModel

class BingoGame:
    def __init__(self):
        self.model = BingoModel()
        self.game_loop()
        self.last_pick = None

    def game_loop(self):
        control = ''
        while control != 'exit':
            print('Type [p]ick, [h]istory, [r]estart, or [e]xit')
            control = input('Enter next command: ')
            print()
            if control in ['p', 'pick']:
                self.last_pick = self.model.pick_number()
                self.print_state()
            elif control in ['r', 'restart']:
                self.model.reset_board()
            elif control in ['h', 'history']:
                print('Oldest to Newest')
                print(self.model.get_history())
            else:
                print('Not a valid choice, try again')
            print('-' * 50)
    
    def print_state(self):
        print(f'Winning Pattern: {self.model.pattern}')
        print('Last 3 (Oldest to Newest): ', self.model.get_recent_history())
        print('Picked: ', self.last_pick)

if __name__ == '__main__':
    bingo_game = BingoGame()