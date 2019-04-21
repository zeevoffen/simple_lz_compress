import unittest
import myzip

class Test_myzip(unittest.TestCase):
    def test_A(self):
        lz1 = myzip.lz("A"*10)

    def test_B(self):
        lz1 = myzip.lz("ABABA"*100000)

    def test_C(self):
        lz1 = myzip.lz("BABAB"*10124)

if __name__ == '__main__':
    unittest.main()
