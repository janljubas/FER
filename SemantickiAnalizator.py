import sys

input = sys.stdin.readlines()
input = [redak.strip() for redak in input]  # input je sada lista linija iz unosa
output, k = '', 0
posljednji_za = 0

# lista izlaza leksicke analize
prave_naredbe = [line for line in input if (not line.startswith('<') and not(line.startswith('$') ) and len(line) > 0  ) ]
broj_redaka = int(prave_naredbe[-1].split(" ")[1])

# naredbe leksicke analize rasporedene po retcima
lines = [ [] for _ in range(broj_redaka) ] 
for i in range (1, broj_redaka + 1):
    lines[i-1] = [line for line in prave_naredbe if (int(line.split(" ")[1]) == i ) ]

# print(*lines, sep = "\n")

rjecnik_varijabli = dict()

def chk_dict(ime_var, dict):
    if (ime_var not in dict):
        return False
    return True

def idn(ime_var, rbr, right_side):
    global output
    global k
    # najprvije provjera koliki je k, verzija ako nije 0 je u else

    if (k < 1):
        for i in range (len(right_side)):

            # prvo provjera je li desna strana definirana + izbjegavanje circular definition problema
            if (right_side[i].split(" ")[0] == "IDN" ):
                if not chk_dict( right_side[i].split(" ")[2], rjecnik_varijabli ) :
                    output += f"err {right_side[i].split(' ')[1]} {right_side[i].split(' ')[2]}\n"
                    return False 
                else:
                    output += f"{ right_side[i].split(' ')[1] } {rjecnik_varijabli.get( right_side[i].split(' ')[2] ) } { right_side[i].split(' ')[2] }\n"

        # ako je varijabla prvi put definirana, unesi ju u rjecnik
        if not chk_dict(ime_var, rjecnik_varijabli):
            rjecnik_varijabli[ime_var] = int(rbr)
            return True
        
        return True
    
    else:
        
        nadvarijable = rjecnik_varijabli[k]['lista_nadvarijabli']   # mozda bug -> ne collecta direktno sve u najdonju listu nadvarijabli
        
        for i in range (len(right_side)):

            var = right_side[i].split(" ")[2]

            # prvo provjera je li desna strana definirana + izbjegavanje circular definition problema
            if (right_side[i].split(" ")[0] == "IDN" ):

                
                if not chk_dict( var, rjecnik_varijabli[k]) and var not in nadvarijable:
                    output += f"err {right_side[i].split(' ')[1]} {var}\n"
                    return False 
                
                elif (rjecnik_varijabli[k].get(var) != None and var in lines[posljednji_za][1].split(" ") ):
                    output += f"{ right_side[i].split(' ')[1] } {rjecnik_varijabli[k].get( var ) } { var }\n"
                
                elif (rjecnik_varijabli.get(var) != None):
                    output += f"{ right_side[i].split(' ')[1] } {rjecnik_varijabli.get( var ) } { var }\n"
                
                else:
                    if (nadvarijable.get(var) != None):
                        output += f"{ right_side[i].split(' ')[1] } {nadvarijable.get( var ) } { var }\n"
                    else:
                        output += f"{ right_side[i].split(' ')[1] } {rjecnik_varijabli[k].get( var ) } { var }\n"

        
            # ako je varijabla prvi put definirana, unesi ju u rjecnik
            if not chk_dict(ime_var, rjecnik_varijabli[k]) and ime_var not in nadvarijable:
                rjecnik_varijabli[k][ime_var] = int(rbr)    # eventualni bug jer dodaje i non-IDN stvari
    
    return True

def za(line):

    global rjecnik_varijabli
    global k
    global output
    global posljednji_za

    posljednji_za = int( line[0].split(" ")[1] ) - 1    # mozda -1 jos

    if k < 2:      # lista_nadvarijabli = [*rjecnik_varijabli]
        lista_nadvarijabli = rjecnik_varijabli.copy()
    else: ##################################################################################
        lista_nadvarijabli = rjecnik_varijabli.copy()
        for z in range (k-1):
            pomocna = {k: v for k, v in rjecnik_varijabli[z+1].items() if k not in ['desno', 'iterator', 'lista_nadvarijabli']}
            lista_nadvarijabli.update(pomocna)
    
    iterator = line[1].split(" ")[2]
    desno = line[3:]

    rjecnik_varijabli[k], rjecnik_varijabli[k]["desno"], rjecnik_varijabli[k]["iterator"], rjecnik_varijabli[k]["lista_nadvarijabli"] = dict(), desno, iterator, lista_nadvarijabli

    rjecnik_varijabli[k][iterator] = line[1].split(" ")[1]

    for naredba in desno:

        var = naredba.split(" ")[2]
        
        if var == iterator:
            output += f"err {naredba.split(' ')[1]} {var}"
            return False
        
        if var in lista_nadvarijabli:
            output += f"{ naredba.split(' ')[1] } {lista_nadvarijabli.get( var ) } { var }\n"
        
        elif (naredba.split(" ")[0] == "IDN"):
            if var not in rjecnik_varijabli:
                output += f"err {naredba.split(' ')[1]} {var}"  #########
                return False
            rjecnik_varijabli[var] = line[1].split(" ")[1]  ############## je li ovo utjece na druge testove

    return True

def az(k):
    global rjecnik_varijabli
    if k > 0:
        del rjecnik_varijabli[k]

# samo 3 mogucnosti za sintaksno ispravne programe -> IDN, KR_AZ i KR_ZA su na pocetku linije
def program_brate():

    global k

    for line in lines :

        elem = line[0].split(" ")

        if (elem[0] == ( "IDN" ) ):
            if not idn( elem[2], elem[1] , line[2:]) :
                return False

        elif (elem[0] == ( "KR_ZA" )):
            k += 1   
            if not za(line):
                return False

        elif (elem[0] == ( "KR_AZ" ) ):
            az(k)
            k -= 1
        
        
    return True

# True samo ako su prosle sve linije i nije javljen error   < - krivo?

program_brate()

print(output)