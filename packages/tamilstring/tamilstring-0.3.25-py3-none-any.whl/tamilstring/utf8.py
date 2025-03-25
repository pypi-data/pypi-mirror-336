from .constant import VOULES_LET,VOULES_SYM

def english_range(code,specify=False):
    letter = None
    if 0x0000 <= code <= 0x007E:
        if 0x41 <= code <= 0x5A:
            letter = "UPP" 
        elif 0x61 <= code <= 0x7A:
            letter = "LOW"
        elif 0x30 <= code <= 0x39:
            letter = "NUM"
        elif code < 0x80: 
            letter = "SYM"
    if specify:
        return letter if letter != None else False
    else:
        return True if letter != None else False

def in_range(code):
    if 0x0B80 <= code <= 0x0BFF:
        return True
    else:
        return False

def tamil_range(code,specify=False):
    letter = None
    if in_range(code):
        if code == 0x0BCD or code == 0x0B82:
            letter = "CON"
        elif 0x0B85 <= code <= 0x0B94:
            letter = "VOL"
        elif 0x0B95 <= code <= 0x0BB9:
            if code == 0x0B9C or 0x0BB6 <= code <=0x0BB9:
                pass
            else:
                letter = "COM" 
        elif 0x0BBE <= code <= 0x0BCC:
            letter = "UNI"
        elif 0x0BE6 <= code <= 0x0BEF:
            letter = "NUM"
        elif 0x0BF1 <= code <= 0x0BFA:
            letter = "CAR" 
        elif code == 0x0B83:
            letter = "AUT"

    if specify:
        return letter if letter != None else False
    else:
        return True if letter != None else False
 
def sanskrit_range(code,specify=False):
    letter = None
    if in_range(code):
        if code == 0x0B9C or 0x0BB6 <= code <=0x0BB9:
            letter = "COM" 
    if not specify:
        return letter
    else:
        return True if letter != None else False

def get_letters(string,capsule=False,error=True):
    rt = []
    previous_compound = None
    for index,char in enumerate(string):
        code = ord(char ) 
         
        english = english_range(code,specify=True)
        if english != False:
            rt.append(("en",char,english)) 
            continue
        
        tamil = tamil_range(code,specify=True)
        if tamil != False:
            if tamil == "VOL":
                rt.append(("ta",char,"VOL"))
            elif tamil == "UNI":
                last = rt[-1] if rt else None
                if last != None:
                    if last[-1] == "COM":
                        rt[-1] = (last[0] ,last[1]+char, "COM")
                    if last[1] == "ஶ்ர":
                        rt[-1] = (last[0] ,last[1]+char, "SYM")
            elif tamil == "CON":
                last = rt[-1] if rt else None
                if last != None:
                    if last[-1] == "COM":
                        rt[-1] = (last[0] ,last[1]+char, "CON")
            elif code == 0x0BB0:
                last = rt[-1] if rt else None
                if last != None:
                    if last[1] == "ஶ்":
                        rt[-1] = ("sa" ,last[1]+char, "SYM")
                    else:
                        rt.append(("ta",char,tamil ))
            else:
                rt.append(("ta",char,tamil ))
            continue

        sanskrit = sanskrit_range(code,specify=True)
        if sanskrit != None:
            if code == 0x0BB7:
                last = rt[-1] if rt else None
                if last != None:
                    if last[1] == "க்":
                        rt[-1] = ("sa" ,last[1]+char, "COM")
                else:
                    rt.append( ("sa",char,"COM" ) )
            else:
                rt.append( ("sa",char,"COM" ) )
        else:
            rt.append(("~",char,"UNK"))

    if capsule:
        return rt
    else:
        return [ letter[1] for letter in rt]

def remove_voule(letter):
    pass

def split_compound(letter, strict=True):
    letter = get_letters(letter, capsule=True)[0]
    if letter[-1] == "COM":
        for voule_let, voule_sym in zip(VOULES_LET[1:],VOULES_SYM):
            if letter[1][-1] == voule_sym:
                return (letter[1][:-1]+'்', voule_let)
        else:
            return (letter[1]+'்', "அ")
    else:
        return None

def make_compound(letter1,letter2):
    letter1 = get_letters(letter1, capsule=True)
    letter2 = get_letters(letter2, capsule=True)
    if len(letter1) == 1 and len(letter2) == 1:
        letter1 , letter2 = letter1[0] , letter2[0]
        if (letter1[-1] == "CON" and letter2[-1] == "VOL") or (letter1[-1] == "VOL" and letter2[-1] == "CON"):
            constant = letter1 if letter1[-1] == "CON" else letter2
            constant = constant[1][:-1]
            voule = letter1 if letter1[-1] == "VOL" else letter2
            voule = voule[1][-1]
            for voule_let, voule_sym in zip(VOULES_LET[1:],VOULES_SYM):
                if voule == voule_let:
                    return constant + voule_sym
            else:
                return constant
        else:
            raise ValueError("unjoinable letter types")
    else:
        raise ValueError("more then two letter in any one parameter")
