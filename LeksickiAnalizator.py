import sys
ulaz = []
ulaz = sys.stdin.readlines()                # ulaz je sada lista linija iz unosa
ulaz = [redak.strip() for redak in ulaz]

# definicije funkcija
def sredi_current_line(current_line):
    separator = "//"
    if (current_line.find(separator) != -1):
        current_line = current_line.partition(separator)[0]    # micanje svega nakon "//"
    
    current_line = current_line.replace("\t", "")
    for hehehaha in range(6):
        current_line = current_line.replace("  ", " ")  # vrati na 1 i 0 razmaka
    return current_line

def printaj(jedinka, rbr, type):
    print(type + " " + str(rbr) + " " + "".join(jedinka) )

def chk_num(jedinka):
    return all(item.isnumeric() for item in jedinka)

def chk_alpha(jedinka):
    return all(item.isalpha() for item in jedinka)

def dupli_extend(jedinka, redak, m):
    jedinka.extend((redak[m], redak[m+1]))
    m += 2
    return jedinka, m

def keyword_ispis(jedinka, redak, m, rbr, dva_znaka,  string):
    if (len(redak) == 2 or (len(redak) > 2  and  len(jedinka)== 0 )):
        print(string + str(rbr) + " " + "".join(dva_znaka) )
        m += 2
        jedinka.clear()
    return jedinka, redak, m, rbr, dva_znaka

def obradi_keyword(redak, jedinka, m, rbr):
    if (m+2 <= len(redak)-1):
        if (len(jedinka) != 0 and redak[m+2] != ' '):
            printaj(jedinka, rbr, "BROJ") if (chk_num(jedinka)) else printaj(jedinka, rbr, "IDN")
            jedinka.clear()

        elif(redak[m+2].isalpha()):
            [jedinka, m] = dupli_extend(jedinka, redak, m)
    return redak, jedinka, m, rbr

def obradi_operator(jedinka, redak, rbr, m, string):
    if (len(jedinka) != 0):
                printaj(jedinka, rbr, "BROJ") if (jedinka[0].isnumeric()) else printaj(jedinka, rbr, "IDN") 
    else:
        jedinka.append(redak[m])
        print(string + str(rbr) + " " + "".join(jedinka) )
        m += 1
    jedinka.clear()    
    return jedinka, redak, rbr, m

def parsiraj_redak(redak, rbr):
    m = 0
    jedinka = []

    while( m != len(redak)):

        dva_znaka = []

        if (m != len(redak)-1):
            for index in range(m, m+2):
                dva_znaka.append(redak[index])    

        if ("".join(dva_znaka).lower() == "za"):
            [redak, jedinka, m, rbr] = obradi_keyword(redak, jedinka, m, rbr)
            [jedinka, redak, m, rbr, dva_znaka] = keyword_ispis(jedinka, redak, m, rbr, dva_znaka, "KR_ZA ")

        elif ("".join(dva_znaka).lower() == "az"):
            [redak, jedinka, m, rbr] = obradi_keyword(redak, jedinka, m, rbr)            
            [jedinka, redak, m, rbr, dva_znaka] = keyword_ispis(jedinka, redak, m, rbr, dva_znaka, "KR_AZ ")

        elif ("".join(dva_znaka).lower() == "od"):
            [redak, jedinka, m, rbr] = obradi_keyword(redak, jedinka, m, rbr)
            [jedinka, redak, m, rbr, dva_znaka] = keyword_ispis(jedinka, redak, m, rbr, dva_znaka, "KR_OD ")

        elif ("".join(dva_znaka).lower() == "do"):
            [redak, jedinka, m, rbr] = obradi_keyword(redak, jedinka, m, rbr)
            [jedinka, redak, m, rbr, dva_znaka] = keyword_ispis(jedinka, redak, m, rbr, dva_znaka, "KR_DO ")

        elif (redak[m] == "+"):
            [jedinka, redak, rbr, m] = obradi_operator(jedinka, redak, rbr, m, "OP_PLUS ")

        elif (redak[m] == "-"):
            [jedinka, redak, rbr, m] = obradi_operator(jedinka, redak, rbr, m, "OP_MINUS ")

        elif (redak[m] == "*"):
            [jedinka, redak, rbr, m] = obradi_operator(jedinka, redak, rbr, m, "OP_PUTA ")

        elif (redak[m] == "/"):
            [jedinka, redak, rbr, m] = obradi_operator(jedinka, redak, rbr, m, "OP_DIJELI ")

        elif (redak[m] == "="):
            [jedinka, redak, rbr, m] = obradi_operator(jedinka, redak, rbr, m, "OP_PRIDRUZI ")

        elif (redak[m] == "("):
            print("L_ZAGRADA " + str(rbr) + " " + "(")
            m += 1
        
        elif (redak[m] == ")"):
            if (len(jedinka) != 0):
                printaj(jedinka, rbr, "BROJ") if (jedinka[0].isnumeric()) else printaj(jedinka, rbr, "IDN")
            
            print("D_ZAGRADA " + str(rbr) + " " + ")")
            m += 1
            jedinka.clear()

        elif ( redak[m].isalpha() ):
            if (len(jedinka) != 0 and (not jedinka[len(jedinka) - 1].isnumeric()) and m != len(redak) - 1 ):
                jedinka.append(redak[m])
            elif (len(jedinka) != 0 and jedinka[len(jedinka) - 1].isnumeric() ):
                printaj(jedinka, rbr, "IDN") if (not chk_num(jedinka) ) else printaj(jedinka, rbr, "BROJ")
                jedinka.clear()
                m -= 1
            else:
                jedinka.append(redak[m])
                if (m == len(redak) - 1):
                    printaj(jedinka, rbr, "IDN")
            m += 1

        elif( redak[m].isnumeric() ):
            if (len(jedinka) != 0 and jedinka[0].isnumeric() and m != len(redak) - 1 ):    
                jedinka.append(redak[m])
            elif (len(jedinka) != 0 and not (jedinka[0].isnumeric() or jedinka[0].isalpha() ) ):
                printaj(jedinka, rbr, "IDN")
                jedinka.clear()
                m -= 1
            else:
                jedinka.append(redak[m])
                if (m == len(redak) - 1 and chk_num(jedinka) ):
                    printaj(jedinka, rbr, "BROJ")
                elif(m == len(redak) - 1):
                    printaj(jedinka, rbr, "IDN")
            m += 1
        
        elif (redak[m] == " "):
            if (len(jedinka) != 0):
                printaj(jedinka, rbr, "IDN") if (not chk_num(jedinka) ) else printaj(jedinka, rbr, "BROJ")
            jedinka.clear()
            m += 1

# glavni program
count_redak = len(ulaz)     # broj redaka

for i in range (count_redak) :
    current_line = ulaz[i]  # odvajanje s obzirom na "\n"
    current_line = sredi_current_line(current_line)
    parsiraj_redak(current_line, i+1)