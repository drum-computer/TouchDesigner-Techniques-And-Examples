class customBaseEXT:
    def __init__(self, ownerComp: baseCOMP):
        pass

    def on_pulse(self):
        print('on_pulse pressed')

    def on_value(self, val: int):
        print(f'on_value called, with val = {val}')

    def on_name(self, name: str):
        print(f'on_name called, with name = {name}')

    def on_options(self, option: str):
        print(f'on_option called, with option = {option}')

    def on_toggle(self, val: bool):
        print(f'on_toggle called, with toggle = {val}')

