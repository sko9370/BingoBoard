from BingoModel import BingoModel

class BingoGame:
    def __init__(self):
        self.model = BingoModel()
        self.game_loop()

    def game_loop(self):
        control = ''
        self.choose_pattern()

        while control != 'exit':
            print('Type [p]ick, [h]istory, [r]estart, or [e]xit')
            control = input('Enter next command: ')
            print()
            if control in ['p', 'pick']:
                self.last_pick = self.model.pick_number()
                self.print_state()
            elif control in ['r', 'restart']:
                self.model.reset_board()
                self.choose_pattern()
            elif control in ['h', 'history']:
                print('Oldest to Newest')
                print(self.model.get_history())
            elif control in ['e', 'exit']:
                print('Later!')
                break
            else:
                print('Not a valid choice, try again')
            print('-' * 50)
        
    def choose_pattern(self):
        pattern = str.upper(input('Choose the winning pattern: '))
        if not pattern:
            print('No winning pattern provided, defaulting to 5 in a row')
            pattern = '5 IN A ROW'
        self.model.set_win_pattern(pattern)
    
    def print_state(self):
        print(f'Winning Pattern: {self.model.pattern}')
        print('Last 3 (Oldest to Newest): ', self.model.get_recent_history())
        print('Picked: ', self.model.history[-1])

if __name__ == '__main__':
    bingo_game = BingoGame()