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
        ui.markdown('# BINGO!')
        # Last picked number
        with ui.row(align_items='center'):
            ui.label('Last Picked: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(self.model_dict, 'last')
        # Last 3 picked
        with ui.row(align_items='center'):
            ui.label('Last 3 (Oldest to Newest): ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(
                    self.model_dict, 'recent',
                    backward=lambda r: r
                )
        # Winning pattern
        with ui.row(align_items='center'):
            ui.label('Winning Pattern: ').classes('text-xl')
            ui.label().classes('text-xl').bind_text_from(
                self.model_dict, 'pattern'
            )
            '''
            ui.select(
                ['5 IN A ROW', '4 CORNERS', 'PYRAMID'], value='5 IN A ROW'
            ).classes('text-xl').bind_value_to(
                self.model, 'self.pattern',
                forward=lambda pattern: self.model.set_win_pattern(pattern)
            )
            '''
        # History
        show_history = {'value': False}
        with ui.row(align_items='center').bind_visibility_from(show_history, 'value'):
            ui.label().classes('text-xl').bind_text_from(
                self.model_dict, 'history',
                backward=lambda recent: f'History (Oldest to Newest): {recent}'
            )
        ui.separator()
        # Buttons
        with ui.row():
            ui.button('Pick next', on_click=lambda: self.pick_number())
            ui.button('Restart', on_click=lambda: self.restart())
        
        # Settings
        visible = ui.checkbox('Show Settings', value=False)
        with ui.column().bind_visibility_from(visible, 'value'):
            with ui.row(align_items='center'):
                # Dark mode
                dark = ui.dark_mode(value=True)
                ui.switch('Dark mode').bind_value(dark)
                # Show full history
                ui.switch('Show full history').bind_value(show_history, 'value')

            # Set winning pattern and add custom ones
            columns = [{
                'name': 'pattern',
                'label': 'Set Winning Pattern',
                'field': 'pattern',
                'required': True,
                'sortable': True
            }]
            rows = [
                {'pattern': '5 IN A ROW'},
                {'pattern': '4 CORNERS'},
                {'pattern': 'PYRAMID'}
            ]
            pattern_table = ui.table(
                columns=columns,
                rows=rows,
                row_key='pattern',
                selection='single',
                on_select=lambda p: self.model_dict.update({'pattern':p.selection[0]['pattern']}) if p.selection else False
            )
            pattern_table.selected = [{'pattern': '5 IN A ROW'}]

        # Run web
        ui.run()
    
    def pick_number(self):
        self.model.pick_number()
        self.refresh_dict()
    
    def restart(self):
        self.model.reset_board()
        self.refresh_dict()
    
    def refresh_dict(self):
        self.model_dict['pattern'] = self.model.pattern
        self.model_dict['last'] = self.model.get_last()
        self.model_dict['recent'] = ' - '.join(self.model.get_recent_history())
        self.model_dict['history'] = ' - '.join(self.model.get_history()[:-1])

if __name__ in {'__main__', '__mp_main__'}:
    bingoWeb = BingoWeb()