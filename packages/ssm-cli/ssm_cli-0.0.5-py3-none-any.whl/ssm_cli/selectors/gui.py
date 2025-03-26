def select(instances: list) -> dict:
    try:
        from easygui import choicebox
    except ModuleNotFoundError:
        raise ModuleNotFoundError("tkinter missing, see README")
    selection = choicebox("Select a host", choices=instances)
    return selection
