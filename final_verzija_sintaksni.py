import sys

input = sys.stdin.readlines()
input = [redak.strip() for redak in input]  # input je sada lista linija iz unosa

tabs = 0
output = ''
current_line = 0


def program():  # {IDN, KR_ZA, ⏊}
    global input
    global output
    global current_line
    global tabs

    output += f"\n{' ' * tabs}<program>"

    if current_line == len(input):  # provjera za  ⏊
        print("err kraj")
        return False

    elif (input[current_line][0:3] == "IDN" or input[current_line][0:5] == "KR_ZA"):  # provjera za IDN
        if not lista_naredbi():
            return False
        return True

    print("err " + "".join(input[current_line]))
    return False


def za_petlja():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    output += f"\n{' ' * tabs}<za_petlja>"
    current_tabs = tabs

    if current_line == len(input):
        print("err kraj")
        return False

    elif input[current_line][0:5] == "KR_ZA":
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        za_tebz = tabs

        if current_line == len(input):
            print("err kraj")
            return False

        elif input[current_line].split(" ")[0] == "IDN":
            output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        else:
            print("err " + "".join(input[current_line]))
            return False
        current_line += 1

        if current_line == len(input):
            print("err kraj")
            return False

        elif input[current_line].split(" ")[0] == "KR_OD":
            output += f"\n{' ' * (tabs + 1)}{input[current_line]}"

        else:
            print("err " + " ".join(input[current_line]))
            return False
        current_line += 1

        if not E():
            print("err " + "".join(input[current_line]))
            return False

        if current_line == len(input):
            print("err kraj")
            return False

        elif input[current_line].split(" ")[0] == "KR_DO":
            tabs = current_tabs
            output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        else:
            print("err " + " ".join(input[current_line]))
            return False
        current_line += 1

        if not E():
            return False

        tabs = za_tebz  ######
        if not lista_naredbi():
            return False

        if current_line == len(input):
            print("err kraj")
            return False

        elif input[current_line].split(" ")[0] == "KR_AZ":
            tabs = current_tabs
            output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
            tabs -= 1
        else:
            print("err " + "".join(input[current_line]))
            return False
        current_line += 1
    else:
        print("err " + "".join(input[current_line]))
        return False
    return True


def E_lista():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    output += f"\n{' ' * tabs}<E_lista>"

    if current_line == len(input):
        output += f"\n{' ' * (tabs + 1)}$"
        tabs -= 2
        return True

    if (input[current_line].split(" ")[0] in ["IDN", "KR_ZA", "KR_DO", "KR_AZ", "D_ZAGRADA"]):
        output += f"\n{' ' * (tabs + 1)}$"

        if (input[current_line].split(" ")[0] == "D_ZAGRADA"):
            current_line += 1

        tabs -= 2
        return True

    elif (input[current_line][0:7] == "OP_PLUS" or input[current_line][0:8] == "OP_MINUS"):
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        if not E():
            return False
        return True

    return False


def E():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    trenutni_tabs = tabs
    output += f"\n{' ' * tabs}<E>"

    if current_line == len(input):  # provjera za  ⏊
        print("err kraj")
        return False

    if (input[current_line].split(" ")[0] in ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]):

        if not T():
            return False

        tabs = trenutni_tabs

        if not E_lista():
            return False
        return True

    return False


def T():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    trenutni_tab = tabs
    output += f"\n{' ' * tabs}<T>"



    if (input[current_line].split(" ")[0] in ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]):
        if not P():
            return False

        tabs = trenutni_tab

        if not T_lista():
            return False

        return True

    return False


def P():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    current_tabs = tabs
    output += f"\n{' ' * tabs}<P>"

    if (input[current_line].split(" ")[0] in ["OP_PLUS", "OP_MINUS"]):
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        if not P():
            return False
        return True

    elif (input[current_line].split(" ")[0] in ["IDN", "BROJ"]):
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        tabs -= 1
        current_line += 1
        return True

    elif (input[current_line][0:9] == "L_ZAGRADA"):
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        if not E():
            return False
        current_line -= 1
        tabs = current_tabs
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        return True

    return False


def T_lista():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    output += f"\n{' ' * tabs}<T_lista>"

    if (current_line == len(input)):
        output += f"\n{' ' * (tabs + 1)}$"
        tabs -= 2
        return True

    elif (input[current_line].split(" ")[0] in [
        "IDN", "KR_ZA", "KR_DO", "KR_AZ", "D_ZAGRADA", "OP_PLUS", "OP_MINUS"] or current_line == len(input)):
        output += f"\n{' ' * (tabs + 1)}$"
        tabs -= 2
        return True

    elif (input[current_line][0:7] == "OP_PUTA" or input[current_line][0:9] == "OP_DIJELI"):
        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        current_line += 1
        if not T():
            return False
        return True

    print("err " + "".join(input[current_line]))
    return False


def naredba():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    current_tab = tabs
    output += f"\n{' ' * tabs}<naredba>"

    if (input[current_line][0:3] == "IDN"):
        if not naredba_pridruzivanja():
            return False
        return True


    elif (input[current_line][0:5] == "KR_ZA"):
        tabs = current_tab  ###########
        if not za_petlja():
            return False
        return True
    return False


def naredba_pridruzivanja():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    output += f"\n{' ' * tabs}<naredba_pridruzivanja>"

    if (input[current_line][0:3] == "IDN"):

        uvjet = output.count("D_ZAGRADA") < output.count("L_ZAGRADA")

        if ( current_line > 0 and input[current_line - 1].split(" ")[0] == "BROJ" and uvjet):
            print("err " + "".join(input[current_line]))
            return False


        output += f"\n{' ' * (tabs + 1)}{input[current_line]}"
        output += f"\n{' ' * (tabs + 1)}{input[current_line + 1]}"
        current_line += 2
        if not E():
            return False
        return True


def lista_naredbi():
    global input
    global output
    global current_line
    global tabs
    tabs += 1
    current_tabs = tabs
    output += f"\n{' ' * tabs}<lista_naredbi>"

    if (current_line == len(input) or input[current_line][0:5] == "KR_AZ"):  # prvi slucaj, kada se dolazi do listova
        output += f"\n{' ' * (tabs + 1)}$"
        tabs -= 2
        return True

    elif (input[current_line][0:3] == "IDN" or input[current_line][0:5] == "KR_ZA"):  # drugi slucaj, kada se nastavljaju naredbe
        if not naredba():
            return False

        tabs = current_tabs
        
        if not lista_naredbi():
            return False
        return True

    return False

# ----------------------------------------------------------------------------------------------------------------------
if program():
    print(output[1:])