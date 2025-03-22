from nicegui import ui

from BingoBackend.BingoModel import BingoModel
from BingoBackend.BingoGame import BingoGame

class BingoWeb:
    def __init__(self):
        self.model = BingoModel()
        self.model_dict = {}
        self.refresh_dict()
        self.start_game()

    def start_game(self):
        ui.label().bind_text_from(
            self.model_dict, 'last',
            backward=lambda last: f'Last Pick: {last}'
        )
        ui.label().bind_text_from(
            self.model_dict, 'recent',
            backward=lambda recent: f'Last 3 (Oldest to Newest): {recent}'
        )
        ui.label().bind_text_from(
            self.model_dict, 'history',
            backward=lambda recent: f'History (Oldest to Newest): {recent}'
        )
        with ui.row():
            ui.button('Pick next', on_click=lambda: self.pick_number())
            ui.button('Restart', on_click=lambda: self.restart())
        ui.run()
    
    def pick_number(self):
        self.model.pick_number()
        self.refresh_dict()
    
    def restart(self):
        self.model.reset_board()
        self.refresh_dict()
    
    def refresh_dict(self):
        self.model_dict['last'] = self.model.get_last()
        self.model_dict['recent'] = ', '.join(self.model.get_recent_history())
        self.model_dict['history'] = ', '.join(self.model.get_history()[:-1])

if __name__ in {'__main__', '__mp_main__'}:
    bingoWeb = BingoWeb()