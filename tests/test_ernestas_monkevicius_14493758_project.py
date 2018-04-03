'''
Created on 3 Apr 2018

@author: ernest
'''
import unittest
from ernestas_monkevicius_14493758_project import data_structures

#EXAMPLE TESTING
class Test(unittest.TestCase):
        
    #def test_invalid1(self):
    #    t = Triangle(1, 2, 4)
    #    self.assertTrue(t.classify() == "INVALID")
        
    def test_Currency(self):
        currency = data_structures.Currency()
        #Logic here...
        self.assertTrue(True, "Success!!")
        
        
if __name__ == '__main__':
    unittest.main()
