from nicegui import events, ui, app


def float_validator(val):
    try:
        float(val)
        return None
    except:
        return 'Value must be a float'


def int_validator(val):
    try:
        int(val)
        return None
    except:
        return 'Value must be an integer'


class IntegerInput(ui.input):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         validation=int_validator,
                         **kwargs)


class FloatInput(ui.input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         validation=float_validator,
                         **kwargs)
