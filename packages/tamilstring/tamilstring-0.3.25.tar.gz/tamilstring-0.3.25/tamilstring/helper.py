from . import utf8 


class Letter:
    _instance = None  
    def __new__(cls, *args, **kwargs):
        singleton = kwargs.pop('singleton', False)
        if singleton:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = True
            return cls._instance
        else: 
            return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        if not getattr(self, '_initialized', True):
            super().__init__(*args, **kwargs)
            self._initialized = True 
        if len(args) == 1:
            args1 = args[0]
            if isinstance(args1, str):
                args1 = str(args1)
            self.__root = utf8.get_letters(args1,capsule=True)[0]
        else:
            self.__root = None
        self.output = kwargs.pop('obj', False)
        
    def __add__(self,other):        
        if not isinstance(other,Letter):
            other_letters =  utf8.get_letters(other,capsule=True)
            if len(other_letters) != 1: 
                other = take_string_backup(other)
            else:
                other = take_letter_backup(other)
        if not isinstance(other, Letter):
            if self.is_constant and other.singleton(0).is_voule:
                other.string = utf8.make_compound(self.letter,other.singleton(0).letter) + other[1:]
                return other if self.output else other.string
            else:
                other.string = self.letter+other[:]
                return other if self.output else other.string
        if self.is_constant and other.is_voule:
            other = utf8.make_compound(self.letter,other.letter)
            return Letter(other) if self.output else other
        else:
            other = self.letter + other.letter
            return String(other) if self.output else other
            
    def __sub__(self, other):
        if  not isinstance(other,Letter):
            other_ =  utf8.get_letters(other)
            if len(other_) != 1:
                raise ValueError("only tamil letter can be add.")
            else:
                other = Letter(other)
        if self.is_compound:
            if other.is_constant or other.is_voule:
                if other.is_voule:
                    return Letter(self.constant) if self.output else self.constant
                elif other.is_constant:
                    return Letter(self.voule)  if self.output else self.voule           
            else:
                raise ValueError("voule or constant can subract only from compound")     
        else:
            raise ValueError("non compound kind can not subractable")

    def __contains__(self, item):
        if item in self.letter:
            return True
        else:
            return False

    def __str__(self):
        return self.letter
    
    def root(self,index): 
        if self.__root != None: 
            return self.__root[index]
        else:
            return None

    @property
    def kind(self): 
        return self.root(-1)

    @property
    def lang(self): 
        return self.root(0)

    @property
    def letter(self):
        return self.root(1)

    @letter.setter
    def letter(self, value):
        if value != None:
            self.__root = utf8.get_letters(value,capsule=True)[0] 
        else:
            self.__root = None

    @property
    def capsule(self):
        return self.__root

    @capsule.setter
    def capsule(self, value):
        self.__root = value
        # TODO to change _root sting
 
    @property
    def is_voule(self):
        if self.kind == 'VOL':
            return True
        else:
            return False
        
    @property
    def is_constant(self):
        if self.kind == 'CON':
            return True
        else:
            return False
        
    @property
    def is_compound(self): 
        if self.kind == 'COM':
            return True
        else:
            return False
    
    @property
    def has_voule(self):
        if self.kind == "VOL" or self.kind == "COM":
            return True
        else:
            return False
        
    @property
    def has_constant(self):
        if self.kind == "TA_CON" or self.kind == "COM":
            return True
        else:
            return False
    
    @property
    def voule(self):
        if self.kind == "VOL":
            return self.letter
        elif self.kind == "COM":
            constant_ , voule_ = utf8.split_compound(self.letter)
            return voule_
        else:
            return None
        
    @property
    def constant(self):
        if self.kind == "CON":
            return self.letter
        elif self.kind == "COM":
            constant_ , voule_ = utf8.split_compound(self.letter)
            return constant_
        else:
            return None
          
    @property
    def compound(self):
        if self.kind == "COM":
            return self.letter
        else:
            return None
            
    @property
    def split_letter(self):
        return utf8.split_compound(self.letter)
    
    def contain(self, other):
        if len(other) > 2:
            raise ValueError("it does not look like a seperate letter")
        if not isinstance(other, Letter):
            other = Letter(other)
        if other.kind == self.kind:
            if other.letter == self.letter:
                return True
            else:
                return False
        elif (other.is_compound and not self.is_compound):
            return None
        elif (self.is_compound and not other.is_compound) :
            if other.letter in self.splitLetter:
                return True
            else:
                return False

    def get_match(self, other, output=False):
        if not isinstance(other,Letter):
            other = Letter(other)
        output_value = (False,None,None) 
        if self.letter == other.letter:
            output_value = (True,other.kind,"EXACT")
        elif (other.is_compound and not self.is_compound):
            if self.letter in other.split_letter[0]:
                output_value = (True,other.kind,"CONTAINS")
        elif (self.is_compound and not other.is_compound):
            if other.letter == self.split_letter[1]:
                output_value = (True,other.kind, "CONTAINS")
        if output:
            return output_value
        else:
            return output_value[0]


class String:       
    _instance = None  

    def __new__(cls, *args, **kwargs):
        singleton = kwargs.pop('singleton', False)
        if singleton:
            if cls._instance is None:
                cls._instance = super(String, cls).__new__(cls)
                cls._instance._initialized = True 
            return cls._instance
        else:
            return super(String, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        if not getattr(self, '_initialized', True):
            super(String, self).__init__(*args, **kwargs)
            self._initialized = True 
        if len(args) == 1:
            args1 = args[0]
            if isinstance(args1, str):
                args1 = str(args1)
            self.__root = args1
        else:
            self.__root = None
        self.output = kwargs.pop('obj', False)
        self.position = 0

    def __add__(self,other):
        if not isinstance(other,String):
            other = String(other)
        if self.singleton(-1).is_constant and other.singleton(0).is_voule:
            ret = String("".join(self.letters[:-1] + [ utf8.make_compound(self.letters[-1],
                other.letters[0])] + other.letters[1:] ) )
            return ret if self.output else ret.string
        else:
            ret = String("".join(self.letters + other.letters))
            return ret if self.output else ret.string
            
    def __sub__(self,other):
        if not isinstance(other, Letter):
            other = Letter(other)
        if isinstance(other, Letter):
            if self.singleton(-1).is_compound and ( other.is_voule or other.is_constant): 
                final_letter = self.singleton(-1).constant if other.kind == "VOL" else self.singleton(-1).voule
                ret =  String("".join( self.letters[:-1] ) + final_letter)
                return ret if self.output else ret.string
            else:
                raise ValueError("can only subract string endings with voule or constant")        
        else:
            raise ValueError("can only subract string endings with voule or constant")

    @property
    def letters(self):
        return [l[1] for l in self.capsules]

    @property
    def capsules(self):
        return utf8.get_letters(self.__root,capsule=True)

    @property
    def string(self):
        return self.__root

    @string.setter
    def string(self,value):
        self.__root = value
       
    def has_contain(self, substring,):
        if isinstance(substring, String):
            subString = substring
        else:
            subString = String(substring)    
        matchValue, all_matches = [] ,[]       
        matchCount,tracer = 0,0
        letter = Letter('ஆ',obj=True)
        print(self.string,subString.string) 
        for index , letter_ in enumerate(self.capsules):
            letter.capsule = letter_
            if matchCount == len(subString.letters):
                subString.position,matchCount= 0,0
                all_matches.append((True,matchValue)) 
                matchValue = []
                tracer = index
            checkMatch =  letter.get_match(subString[subString.position],output=True )
            if checkMatch[0]:
                if checkMatch[-1] == "EXACT": 
                    matchValue.append(letter_[1])
                    subString.position += 1 
                    matchCount += 1
                    
                if checkMatch[-1] == "CONTAINS": 
                    constant,voule = letter.split_letter
                    if checkMatch[1] == "VOL":                       
                        matchValue.append(voule)
                        if len(all_matches) != 0:
                            if all_matches[-1][0] == True:
                                all_matches.append((False,constant))
                            else:
                                all_matches[-1] = (False,all_matches[-1][0]+[constant])
                        subString.position += 1  
                        matchCount += 1
            else:
                if index == tracer:
                    all_matches.append( (False,[l for l in self.letters[tracer:index+1]]) )
                else:
                    all_matches[-1] = (False,[l for l in self.letters[tracer:index+1]])
            self.position = index
        return [(am[0],"".join(am[1]) ) for am in all_matches ]
         
    def index_obj(self,index):
        return Letter(self.letters[index])

    def singleton(self,index,singleton = False):
        return Letter(self.letters[index],singleton = True)
    
    def letter(self,index):
        return Letter(self.letters[index])
 
    def __getitem__(self, index):
        if isinstance(index, slice):
            if self.string:
                return "".join(self.letters[index.start:index.stop:index.step])
            else:
                return "".join(self.letters[index.start:index.stop:index.step])
        else:
            return self.letters[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start, stop, step =  index.indices(len(self.letters))   
            previous_value = self.letters
            if not isinstance(value, String):
                other = String(value,singleton = True)
            previous_value[start:stop:step] = other.letters
            self.string = "".join(previous_value)   
        else:
            previous_value = self.letters 
            previous_value[index] = value
            self.string = "".join(previous_value)   


    def __delattr__(self):
        del self

    def __iter__(self):
        return iter(self.letters)
    
    def __len__(self):
        return len(self.letters)

    def __contains__(self, other):        
        if not isinstance(other,str):
            other = str(other)
        if self.__root in other:
            return True
        else:
            return False


letter_singleton_source = Letter(singleton = True)   
letter_singleton_backup = None

def take_letter_backup(letter):
    if letter_singleton_source.letter != None:
        letter_singleton_backup = letter_singleton_source.letter 
    letter_singleton_source.letter = letter
    return letter_singleton_source
    
def restore_letter_backup():
    letter_singleton_source.letter = letter_singleton_backup


string_singleton_source = String(singleton = True)   
string_singleton_backup = None

def take_string_backup(sting):
    if string_singleton_source.string != None:
        string_singleton_backup = string_singleton_source.string 
    string_singleton_source.string = sting
    return string_singleton_source
    
def restore_string_backup():
    string_singleton_source.string = string_singleton_backup
