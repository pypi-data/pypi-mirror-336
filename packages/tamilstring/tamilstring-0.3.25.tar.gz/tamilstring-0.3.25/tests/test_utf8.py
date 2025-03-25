import unittest
from tamilstring.utf8 import get_letters, split_compound, make_compound


class TestBaseWord(unittest.TestCase):
    def test_get_letters(self):
        self.assertEqual(['த','மி','ழ்'],get_letters("தமிழ்"))
        self.assertNotEqual(['த','மி','ழ'],get_letters("தமிழ்"))
        self.assertEqual(['க்ஷி','க்ஷு'],get_letters("க்ஷிக்ஷு"))
        self.assertEqual(['௵'],get_letters("௵"))
        self.assertEqual(['ஶ்ரீ'],get_letters("ஶ்ரீ")) 
        self.assertEqual(['ஶ்ரீ','னி'],get_letters("ஶ்ரீனி")) 
    
    def remove_wrong_unicode(self):
        self.assertEqual(['த','மி','ழ்'],get_letters("தமிழ்்"))
        self.assertEqual([],get_letters("்ா")) 
        self.assertEqual(['க்ஷி','க்ஷு'],get_letters("க்ஷி்ாக்ஷு"))

    def test_split_letter(self):
        self.assertEqual(('ம்','ஆ'),split_compound("மா"))
        self.assertEqual(('க்','ஓ'),split_compound("கோ"))
        self.assertEqual(('ண்','ஐ'),split_compound("ணை"))
        self.assertEqual(None,split_compound("ழ்"))
        self.assertEqual(None,split_compound("ஃ"))
        self.assertEqual(None,split_compound("௵"))
        self.assertEqual(("க்ஷ்","இ"),split_compound("க்ஷி")) 
        self.assertEqual(('ஶ்', 'அ'),split_compound("ஶ"))
        self.assertEqual(('க்ஷ்', 'ஐ'),split_compound("க்ஷை"))

    def test_make_compound(self):
        self.assertEqual('ழௌ',make_compound("ழ்","ஔ"))
        self.assertEqual('பூ',make_compound("ப்","ஊ"))
        self.assertEqual('கை',make_compound("க்","ஐ"))
        self.assertEqual('மூ',make_compound("ம்","ஊ"))
        self.assertEqual('சா',make_compound("ச்","ஆ"))
        with self.assertRaises(ValueError) as context:
            make_compound("ப்ப","ப்")
        self.assertEqual(str(context.exception),"more then two letter in any one parameter")
        
        with self.assertRaises(ValueError) as context:
            make_compound("ச","ஆ")
        self.assertEqual(str(context.exception),"unjoinable letter types")        
        with self.assertRaises(ValueError) as context:
            make_compound("ப்","ப")
        self.assertEqual(str(context.exception),"unjoinable letter types")
        with self.assertRaises(ValueError) as context:
            make_compound("ப்","ப்")
        self.assertEqual(str(context.exception),"unjoinable letter types")
        

        