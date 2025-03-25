import unittest
from tamilstring import Letter


class TestTamil(unittest.TestCase):

    def test_without_letter(self):
        none_letter = Letter()

    def test_singelton(self):
        l1 = Letter("க்",singleton = True)
        l2 = Letter("வா",singleton = True)
        self.assertEqual(id(l1),id(l2))

    def test(self):
        volue = Letter('ஆ')
        constant = Letter('வ்')
        compound = Letter('வா')
        self.assertEqual( "வா",constant+volue )

        self.assertEqual( "வா",constant+"ஆ")
        self.assertEqual( "ஆவ்",volue+constant)
        self.assertEqual( "ஆவ்",volue+"வ்")

        tha = Letter("த")
        self.assertEqual( "தமிழ்", tha+"மிழ்" )
        ith = Letter("த்")
        self.assertEqual( "தமிழ்", ith+"அமிழ்")
        self.assertNotEqual( "தமிழ்", tha+"த்மிழ்")
        self.assertEqual("வ்",compound-volue)
        self.assertEqual("வ்",compound-"ஆ") 
        self.assertEqual("ஆ",compound-constant)
        self.assertEqual("ஆ",compound-"வ்") 

        volue = Letter('ஆ',obj=True)
        constant = Letter('வ்',obj=True)
        compound = Letter('வா',obj=True)

        self.assertEqual( "வா", (constant+volue).letter )
        self.assertEqual( "வா", (constant+"ஆ" ).letter )
        self.assertEqual( "ஆவ்", (volue+constant).string )
        self.assertEqual( "ஆவ்", (volue+"வ்").string )
        
        self.assertEqual( "தமிழ்", (Letter("த",obj=True)+"மிழ்").string )
        self.assertEqual( "தமிழ்", (Letter("த்",obj=True)+"அமிழ்").string )
        self.assertNotEqual( "தமிழ்", (Letter("த",obj=True)+"த்மிழ்").string )

        with self.assertRaises(ValueError) as context:
            compound - Letter("ஃ") 
        self.assertEqual(str(context.exception),"voule or constant can subract only from compound" )
        with self.assertRaises(ValueError) as context:
            volue - compound
        self.assertEqual(str(context.exception),"non compound kind can not subractable" )

 
    def test_get_match(self):
        volue = Letter('ஆ')
        constant = Letter('வ்')
        compound = Letter('வா')
        self.assertTrue( constant.get_match("வ்") )
        self.assertFalse( volue.get_match("வ்") )
        self.assertFalse( constant.get_match("ஆ") )
        self.assertTrue( volue.get_match("ஆ") )
        self.assertTrue( compound.get_match("ஆ") ) 
        self.assertTrue( constant.get_match('வா') )
        self.assertFalse( volue.get_match('வா') )
        self.assertTrue( compound.get_match('வா') )

    def test_kind(self):
        volue = Letter('ஆ')
        constant = Letter('வ்')
        compound = Letter('வா')
        self.assertEqual( volue.kind, 'VOL')
        self.assertNotEqual( volue.kind, 'CON')
        self.assertNotEqual( volue.kind, 'COM')
        
        self.assertNotEqual( constant.kind, 'VOL')
        self.assertEqual( constant.kind, 'CON')
        self.assertNotEqual( constant.kind, 'COM')
        
        self.assertNotEqual( compound.kind, 'VOL')
        self.assertNotEqual( compound.kind, 'CON')
        self.assertEqual( compound.kind, 'COM')


    def test_letter_kind(self):
        volue = Letter('ஆ')
        constant = Letter('வ்')
        compound = Letter('வா')

        self.assertTrue( volue.is_voule )
        self.assertFalse( volue.is_constant)
        self.assertFalse( volue.is_compound)

        self.assertFalse( constant.is_voule )
        self.assertTrue( constant.is_constant)
        self.assertFalse( constant.is_compound)

        self.assertFalse( compound.is_voule )
        self.assertFalse( compound.is_constant)
        self.assertTrue( compound.is_compound)
        
