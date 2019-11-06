


def list_selection(in_list, default=-1):
    def _try_parse_int(val):
        try:
            return int(val)
        except:
            return default
    
    list_len = len(in_list)
    for (i, val) in enumerate(in_list):
        print(f"{i+1}] {val}")
    
    selection = None
    while selection is None:
        inp = input(": ")
        selection = _try_parse_int(inp)
        if selection < 1 or selection > list_len:
            selection = None
    return in_list[selection-1]