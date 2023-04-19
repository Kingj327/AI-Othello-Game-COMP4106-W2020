TRANSLATE_CHAR = {0:" ", 1:"W", 2:"B", 3:"R", 4:"G"}

def view1(state):
    UI = []
    UI.append("╔═" + "═" + ("═╤══" * (len(state[0])-1)) + "═╗")
    for y in range(len(state)):
        row = "║ "
        for x in range(len(state[y])):
            row += TRANSLATE_CHAR[state[x][y]] if (x == 0) else " │ "+TRANSLATE_CHAR[state[x][y]]
        row += " ║"
        UI.append(row)
        if (y != len(state)-1): UI.append("╟─" + "─" + ("─┼──" * (len(state[y])-1)) + "─╢")
    UI.append("╚═" + "═" + ("═╧══" * (len(state[0])-1)) + "═╝")
    return UI

def displayUI(state):
    UI = view1(state)
    for i in range(len(UI)):
        print(UI[i])
