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
        # Winning pattern
        with ui.row(align_items='center'):
            ui.label('Winning Pattern: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(
                    self.model_dict, 'pattern'
                )
        # Last picked number
        with ui.row(align_items='center'):
            ui.label('Last Picked: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(self.model_dict, 'last')
            ui.space()
            # Last 3 picked
            ui.label('Last 3: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(
                    self.model_dict, 'recent',
                    backward=lambda r: r
                )
        # History (hidden by default)
        show_history = {'value': False}

        '''
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
        '''
        #ui.table().bind_visibility_from(show_history, 'value')

        with ui.row(align_items='center').bind_visibility_from(
            show_history, 'value'
        ):
            ui.label().classes('text-xl').bind_text_from(
                self.model_dict, 'history',
                backward=lambda recent: f'History (Oldest to Newest): {recent}'
            )
        ui.separator()


        # Buttons
        with ui.row():
            ui.button('Pick next', on_click=lambda: self.pick_number())
            ui.button('Restart', on_click=lambda: self.restart())
        

        # Bingo Checker
        with ui.expansion('Show Bingo Checker', icon='check').classes('w-full'):
            with ui.row(align_items='center'):
                #input method
                bingo_picks = ui.input(
                    label='Bingo Picks',
                    placeholder='1, 45, 16, etc'
                )
                #button to send input to model to check
                ui.button('Check bingo', on_click=lambda: self.check_bingo(bingo_picks.value))

        # Settings
        with ui.expansion('Expand Settings', icon='settings').classes('w-full'):
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

            with ui.row(align_items='center'):
                pattern = ui.input(
                    label='Set Custom Pattern',
                    placeholder='Pattern'
                )
                ui.button(
                    'Add Custom Pattern',
                    on_click=lambda: pattern_table.add_row(
                        {'pattern': str.upper(pattern.value)}
                    )
                )

        # Run web
        ui.run()
    
    def check_bingo(self, bingo_picks):
        self.model_dict['bingo'] = str(self.model.check_bingo(bingo_picks))
        with ui.dialog(value=True) as dialog, ui.card():
            with ui.row(align_items='center'):
                ui.label('Is it bingo?').classes('text-xl')
                with ui.card():
                    ui.label().classes('text-xl').bind_text_from(
                        self.model_dict,
                        'bingo'
                    )
            with ui.row(align_items='center').classes('w-full'):
                ui.space()
                ui.button('Close', on_click=dialog.close)
                ui.space()
    
    def pick_number(self):
        self.model.pick_number()
        self.refresh_dict()
    
    def restart(self):
        self.model.reset_board()
        self.refresh_dict()
    
    def refresh_dict(self):
        self.model_dict['pattern'] = self.model.pattern
        self.model_dict['last'] = self.model.get_last()
        self.model_dict['recent'] = ' - '.join(reversed(self.model.get_recent_history()))
        self.model_dict['history'] = ' - '.join(reversed(self.model.get_history()[:-1]))
        self.model_dict['bingo'] = 'False'

if __name__ in {'__main__', '__mp_main__'}:
    bingoWeb = BingoWeb()