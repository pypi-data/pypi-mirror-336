from .helper import String, Letter
from .constant import SOFT_CONSTANT,HARD_CONSTAND

letter_singleton_source = Letter(singleton = True)
letter_singleton_backup = letter_singleton_source.letter

string_singleton_source = String(singleton = True)
string_singleton_backup = string_singleton_source.string    

def is_english(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.lang == "en" else False
    restore_letter_backup()
    return return_bool

def is_tamil(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.lang == "ta" else False
    restore_letter_backup()
    return return_bool

def is_sanskrit(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.lang == "sa" else False
    restore_letter_backup()
    return return_bool

def is_tamil_num(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.lang == "ta" and letter_singleton_source.kind == "NUM" else False
    restore_letter_backup()
    return return_bool

def is_english_num(vowel):
    take_letter_backup(vowel)    
    return_bool = True if letter_singleton_source.lang == "en" and letter_singleton_source.kind == "NUM" else False
    restore_letter_backup()
    return return_bool

def is_tamil_char(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.kind == "CAR" else False
    restore_letter_backup()
    return return_bool

def is_vowel(vowel):
    take_letter_backup(vowel)
    return_bool = True if letter_singleton_source.is_voule else False
    restore_letter_backup()
    return return_bool

def is_constant(constant):
    take_letter_backup(constant)
    return_bool = True if letter_singleton_source.is_constant else False
    restore_letter_backup()
    return return_bool

def is_compound(compound):
    take_letter_backup(compound)
    return_bool = True if letter_singleton_source.is_compound else False
    restore_letter_backup()
    return return_bool

def is_aytham(aytham):
    if aytham == "ஃ":
        return True
    else:
        return False

def constant(letter):
    take_letter_backup(letter)
    return_constant = letter_singleton_source.constant 
    restore_letter_backup()
    return return_constant

def vowel(letter):
    take_letter_backup(letter)
    return_constant = letter_singleton_source.voule  
    restore_letter_backup()
    return return_constant

def hard_constant(letter):
    take_letter_backup(letter)
    constant_letter = letter_singleton_source.constant 
    return_constant = None
    for related , constant in zip(HARD_CONSTAND,SOFT_CONSTANT):
        if constant_letter == constant:
            return_constant = related 
            break
    restore_letter_backup()
    return return_constant

def soft_constant(letter):
    take_letter_backup(letter)
    constant_letter = letter_singleton_source.constant 
    return_constant = None
    for related , constant in zip(SOFT_CONSTANT,HARD_CONSTAND):
        if constant_letter == constant:
            return_constant = related 
            break
    restore_letter_backup()
    return return_constant 

def get_constants(value,index=False):
    take_string_backup(value)
    return_list = []
    for indces, letter in enumerate(string_singleton_source.capsules):
        if letter[-1] == "CON":
            return_list.append([indces,letter[1]])
    restore_letter_backup()
    if index:
        return return_list
    else:
        return [ each[-1] for each in return_list ]

def get_vowels(value,index=False):
    take_string_backup(value)
    return_list = []
    for indces, letter in enumerate(string_singleton_source.capsules):
        if letter[-1] == "VOL":
            return_list.append([indces,letter[1]])
    restore_letter_backup()
    if index:
        return return_list
    else:
        return [ each[-1] for each in return_list ]

def get_compounds(value,index=False):
    take_string_backup(value)
    return_list = []
    for indces, letter in enumerate(string_singleton_source.capsules):
        if letter[-1] == "COM":
            return_list.append([indces,letter[1]])
    restore_letter_backup()
    if index:
        return return_list
    else:
        return [ each[-1] for each in return_list ]

def get_tamil(string,only=[]):
    take_string_backup(string)
    return_list = []
    for letter in string_singleton_source.capsules:
        if letter[0] == "ta":
            if letter[-1] in only:
                return_list.append(letter)
            else:
                return_list.append(letter)
    restore_string_backup()
    return capsule_letter(return_list)

def get_english(string,only=[]):
    take_string_backup(string)
    return_list = []
    for letter in string_singleton_source.capsules:
        if letter[0] == "en":
            if letter[-1] in only:
                return_list.append(letter)
            else:
                return_list.append(letter)
    restore_string_backup()
    return capsule_letter(return_list)

def get_sanskrit(string,only=[]):
    take_string_backup(string)
    return_list = []
    for letter in string_singleton_source.capsules:
        if letter[0] == "sa":
            if letter[-1] in only:
                return_list.append(letter)
            else:
                return_list.append(letter)
    restore_string_backup()
    return capsule_letter(return_list)

def get_tamil_numerals(string):
    take_string_backup(string)
    return_list = []
    for letter in string_singleton_source.capsules:
        if letter[0] == "ta":
            if letter[-1] == "NUM":
                return_list.append(letter)
    restore_string_backup()
    return capsule_letter(return_list)

def get_tamil_symbols(string):
    take_string_backup(string)
    return_list = []
    for letter in string_singleton_source.capsules:
        if letter[0] == "ta":
            if letter[-1] == "CAR":
                return_list.append(letter)
    restore_string_backup()
    return capsule_letter(return_list)

def capsule_letter(capsules):
    if isinstance(capsules,tuple):
        return capsules[1]
    else:
        return_letters = []
        for letter in capsules:
            return_letters.append(letter[1])
        return return_letters

def take_letter_backup(value):
    if isinstance(value, Letter):
        letter_singleton_backup = value.letter
        letter_singleton_source.letter = value
    else:
        if letter_singleton_source.letter != None:
            letter_singleton_backup = letter_singleton_source.letter
        letter_singleton_source.letter = value

def restore_letter_backup():
    letter_singleton_source.letter =letter_singleton_backup

def take_string_backup(value):
    if isinstance(value, String):
        string_singleton_backup = value.string
        string_singleton_source.string = value
    else:
        if string_singleton_source.string != None:
            string_singleton_backup = string_singleton_source.string
        string_singleton_source.string = value
  
def restore_string_backup():
    string_singleton_source.string = string_singleton_backup
