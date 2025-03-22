from nicegui import ui

from BingoBackend.BingoModel import BingoModel
from BingoBackend.BingoGame import BingoGame

class bingo_label(ui.label):
    def _handle_text_change(self, text: str) -> None:
        super()._handle_text_change(text)
        if text[0] == ' ':
            self.classes(replace='text-xl text-positive')
        else:
            self.classes(replace='text-xl')

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

        # History Table
        bingo_word = 'BINGO'
        for i in range(5):
            with ui.row(align_items='center'):
                with ui.card().style('width: 40px').classes('items-center'):
                    ui.label(bingo_word[i]).classes('text-xl')
                for j in range(15):
                    with ui.card().style('width: 50px').classes('items-center'):
                        number = i*15 + j + 1
                        bingo_label().classes('text-xl').bind_text_from(self.model_dict['picked_dict'], number)

        # Last picked number
        with ui.row(align_items='center'):
            ui.label('Last Picked: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(self.model_dict, 'last')
        #with ui.row(align_items='center'):
            ui.space()
            # Last 3 picked
            ui.label('Last 3: ').classes('text-xl')
            with ui.card():
                ui.label().classes('text-xl').bind_text_from(
                    self.model_dict, 'recent',
                    backward=lambda r: r
                )
        # History
        show_history = {'value': False}
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
            with ui.table(
                columns=columns,
                rows=rows,
                row_key='pattern',
                selection='single',
                on_select=lambda p: self.model_dict.update({'pattern':p.selection[0]['pattern']}) if p.selection else False
            ) as pattern_table:
                pattern_table.selected = [{'pattern': '5 IN A ROW'}]
                with pattern_table.add_slot('bottom-row'):
                    with pattern_table.row():
                        with pattern_table.cell():
                            ui.button(on_click=lambda: (
                                pattern_table.add_row(
                                    {'pattern': str.upper(pattern.value)}
                                ), pattern.set_value(None)
                            ), icon='add').props('flat fab-mini')
                        with pattern_table.cell():
                            pattern = ui.input(
                                label='Add Custom Pattern',
                                placeholder='Pattern'
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
        self.model_dict['picked_dict'] = self.model.picked_dict

if __name__ in {'__main__', '__mp_main__'}:
    bingoWeb = BingoWeb()