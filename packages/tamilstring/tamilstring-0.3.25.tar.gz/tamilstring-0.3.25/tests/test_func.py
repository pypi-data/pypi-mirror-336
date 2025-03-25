import unittest
from tamilstring.func import get_english,capsule_letter,constant,\
    get_compounds,get_constants,get_sanskrit,get_tamil,get_tamil_numerals, \
    get_tamil_symbols,get_vowels,hard_constant,is_aytham,is_compound, \
    is_constant,is_english,is_english_num,is_sanskrit,is_tamil, \
    is_tamil_char,is_tamil_num,is_vowel,soft_constant,vowel

class TestBaseWord(unittest.TestCase):

    def test_is_english(self):
        self.assertTrue(is_english("a"))
        self.assertTrue(is_english("3"))
        self.assertTrue(is_english("S"))
        self.assertTrue(is_english("!"))
        self.assertTrue(is_english("."))
        self.assertTrue(is_english(" "))
        self.assertTrue(is_english("F"))
        self.assertTrue(is_english(":"))
        self.assertFalse(is_english("இ"))
        self.assertFalse(is_english("ஃ"))
        self.assertFalse(is_english("க்"))
        self.assertFalse(is_english("௳"))

    def testis_tamil(self):
        self.assertTrue(is_tamil("இ"))
        self.assertTrue(is_tamil("ஃ"))
        self.assertTrue(is_tamil("க்"))
        self.assertTrue(is_tamil("௳"))
        self.assertTrue(is_tamil("௶"))
        self.assertTrue(is_tamil("௹"))
        self.assertTrue(is_tamil("கௌ"))
        self.assertTrue(is_tamil("பூ"))
        self.assertFalse(is_tamil("."))
        self.assertFalse(is_tamil(" "))
        self.assertFalse(is_tamil("F"))
        self.assertFalse(is_tamil(":"))

    def test_is_sanskrit(self):
        self.assertTrue(is_sanskrit("ஜ்"))
        self.assertTrue(is_sanskrit("ஷூ"))
        self.assertTrue(is_sanskrit("க்ஷோ"))
        self.assertTrue(is_sanskrit("ஸ்"))
        self.assertTrue(is_sanskrit("ஶா"))
        self.assertTrue(is_sanskrit("க்ஷ்"))
        self.assertTrue(is_sanskrit("ஸோ"))
        self.assertTrue(is_sanskrit("க்ஷா"))
        self.assertFalse(is_tamil("ஶா"))
        self.assertFalse(is_tamil("க்ஷ்"))
        self.assertFalse(is_tamil("F"))
        self.assertFalse(is_tamil(":"))        

    def test_is_tamil_num(self):
        self.assertTrue(is_tamil_num("௦"))
        self.assertTrue(is_tamil_num("௩"))
        self.assertTrue(is_tamil_num("௫"))
        self.assertTrue(is_tamil_num("௮"))
        self.assertFalse(is_tamil_num("1"))
        self.assertFalse(is_tamil_num("க்ஷ்"))
        self.assertFalse(is_tamil_num("F"))
        self.assertFalse(is_tamil_num(":"))        

    def test_is_english_num(self):
        self.assertTrue(is_english_num("1"))
        self.assertTrue(is_english_num("0"))
        self.assertTrue(is_english_num("4"))
        self.assertTrue(is_english_num("7"))
        self.assertFalse(is_english_num("a"))
        self.assertFalse(is_english_num("க்ஷ்"))
        self.assertFalse(is_english_num("௩"))
        self.assertFalse(is_english_num("௫"))     

    def test_is_tamil_char(self):
        self.assertTrue(is_tamil_char("௹"))
        self.assertTrue(is_tamil_char("௵"))
        self.assertTrue(is_tamil_char("௴"))
        self.assertTrue(is_tamil_char("௱"))
        self.assertFalse(is_tamil_char("a"))
        self.assertFalse(is_tamil_char("க்ஷ்"))
        self.assertFalse(is_tamil_char("௩"))
        self.assertFalse(is_tamil_char("௫"))     
 

    def test_is_vowel(self):
        self.assertTrue(is_vowel("அ"))
        self.assertTrue(is_vowel("ஔ"))
        self.assertTrue(is_vowel("ஓ"))
        self.assertTrue(is_vowel("இ"))
        self.assertFalse(is_vowel("a"))
        self.assertFalse(is_vowel("க்ஷ்"))
        self.assertFalse(is_vowel("௩"))
        self.assertFalse(is_vowel("௫"))
        self.assertNotEqual(True,is_vowel("ஃ"))
        self.assertNotEqual(True,is_vowel("க"))
        self.assertNotEqual(True,is_vowel("க்"))
        self.assertEqual(True,is_vowel("உ"))
        self.assertEqual(True,is_vowel("இ"))
           
 
    def test_is_constant(self):
        self.assertTrue(is_constant("க்"))
        self.assertTrue(is_constant("ழ்"))
        self.assertTrue(is_constant("க்ஷ்"))
        self.assertTrue(is_constant("ஞ்"))
        self.assertFalse(is_constant("a"))
        self.assertFalse(is_constant("ஷி"))
        self.assertFalse(is_constant("௩"))
        self.assertFalse(is_constant("௫")) 
        self.assertNotEqual(True,is_constant("ஃ"))
        self.assertNotEqual(True,is_constant("அ"))
        self.assertEqual(True,is_constant("க்"))
        self.assertEqual(True,is_constant("ப்"))
            
   
    def test_is_compound(self):
        self.assertTrue(is_compound("க"))
        self.assertTrue(is_compound("ழ"))
        self.assertTrue(is_compound("க்ஷ"))
        self.assertTrue(is_compound("க்ஷூ"))
        self.assertFalse(is_compound("a"))
        self.assertFalse(is_compound("ஶ்"))
        self.assertFalse(is_compound("௩"))
        self.assertFalse(is_compound("௫"))
        self.assertNotEqual(True,is_compound("ஃ"))
        self.assertNotEqual(True,is_compound("அ"))
        self.assertEqual(True,is_compound("க"))
        self.assertEqual(True,is_compound("மா"))

    def test_is_aytham(self):
        self.assertTrue(is_aytham("ஃ")) 
        self.assertFalse(is_aytham("a"))
        self.assertFalse(is_aytham("ஶ்"))
        self.assertFalse(is_aytham("௩"))
        self.assertFalse(is_aytham("௫"))
        self.assertEqual(True,is_aytham("ஃ"))
        self.assertNotEqual(True,is_aytham("அ"))
     
 
    def test_constant(self): 
        self.assertEqual("ற்",constant("றூ"))
        self.assertEqual("க்ஷ்",constant("க்ஷூ"))
        self.assertEqual("ஷ்",constant("ஷௌ"))
        self.assertEqual("ய்",constant("யொ"))  
        self.assertEqual("ஶ்",constant("ஶ்"))  
        self.assertEqual(None,constant("a")) 
        self.assertEqual(None,constant("௩"))
        self.assertEqual(None,constant("௫"))     

    def test_vowel(self): 
        self.assertEqual("ஊ",vowel("றூ"))
        self.assertEqual("ஊ",vowel("க்ஷூ"))
        self.assertEqual("ஔ",vowel("ஷௌ"))
        self.assertEqual("ஒ",vowel("யொ"))  
        self.assertEqual("அ",vowel("ஶ"))  
        self.assertEqual(None,vowel("a")) 
        self.assertEqual(None,vowel("௩"))
        self.assertEqual(None,vowel("௫"))     

    def test_hard_constant(self):
        hard_constant("ங்")

    def test_soft_constant(self):
        soft_constant("ங்")

    def get_constants(self):  
        self.assertEqual([],get_constants("ஃ"))
        self.assertEqual(['ள்', 'ற்'],get_constants("கொள்வதற்கு"))
        self.assertEqual('க்',get_constants("க்"))
        self.assertEqual(['ட்', 'க்', 'க்'],get_constants("ஆட்சிக்களமாகக்"))
        self.assertEqual(['ல்', 'த்', 'ன்', 'ள்'],get_constants("சுல்த்தான்கள்"))
        self.assertEqual(['ய்', 'ள்', 'க்', 'ப்'],get_constants("ஆய்வாளர்களுக்குப்"))
        self.assertEqual('ல்',get_constants("ஏடுகளில்"))

    def test_get_vowels(self):
        self.assertEqual([],get_vowels("ஃ"))
        self.assertEqual([],get_vowels("கொள்வதற்கு"))
        self.assertEqual([],get_vowels("சரியாக"))
        self.assertEqual(['ஆ'],get_vowels("ஆட்சிக்களமாகக்"))
        self.assertEqual(['இ'],get_vowels("இன்றியமையாதவை"))
        self.assertEqual(['ஒ'],get_vowels("ஒரு"))
        self.assertEqual(['ஏ'],get_vowels("ஏடுகளில்"))    

    def test_get_vowels(self):
        self.assertEqual([],get_compounds("ஃ"))
        self.assertEqual(['கொ', 'வ', 'த', 'கு'],get_compounds("கொள்வதற்கு"))
        self.assertEqual(['ச', 'ரி', 'யா', 'க'],get_compounds("சரியாக"))
        self.assertEqual(['சி', 'க', 'ள', 'மா', 'க'],get_compounds("ஆட்சிக்களமாகக்"))
        self.assertEqual(['றி', 'ய', 'மை', 'யா', 'த', 'வை'],get_compounds("இன்றியமையாதவை"))
        self.assertEqual(['ரு'],get_compounds("ஒரு"))
        self.assertEqual(['டு', 'க', 'ளி'],get_compounds("ஏடுகளில்")) 

    def test_capsule_letter(self):
        self.assertEqual('க்',capsule_letter(("ta","க்","CON")))
        self.assertEqual('ஓ',capsule_letter(("ta","ஓ","VOL")))
        self.assertEqual('ஃ',capsule_letter(("ta","ஃ","AUT")))
        self.assertEqual('௵',capsule_letter(("ta","௵","CAR")))
        self.assertEqual('௩',capsule_letter(("ta","௩","NUM")))
        self.assertEqual('A',capsule_letter(("en","A","UPP")))
        self.assertEqual('ஶ்ரீ',capsule_letter(("sa","ஶ்ரீ","UPP")))


    def test_get_tamil(self):
        documentation = "தமிழ் tamil"
        self.assertEqual(['த','மி','ழ்'],get_tamil(documentation))

    def test_get_english(self):
        documentation = "தமிழ் tamil"
        self.assertEqual([' ','t','a','m','i','l'],get_english(documentation))

    def test_get_sanskrit(self):
        name = "ஶ்ரீனி"
        self.assertEqual(['ஶ்ரீ'],get_sanskrit(name))

    def test_get_tamil_numerals(self):
        text = '''
        ௧ பை
        ௨ கைப்பேசி
        ௩ ஆடை
        '''
        self.assertEqual(['௧','௨','௩'],get_tamil_numerals(text))

    def test_get_tamil_symbols(self):
        text = ' ௵ ௧ பை ௨ கைப்பேசி ௩ ஆடை'
        self.assertEqual(['௵'],get_tamil_symbols(text))

