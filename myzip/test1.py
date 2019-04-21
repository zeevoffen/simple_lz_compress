import unittest
import myzip
import random
import string

class Test_myzip(unittest.TestCase):
    def template(self,str) :
        lz1 = myzip.lz(str)
        print("compression ration : ",lz1._compression_ratio)
        #print(lz1._s)
        #print("encoded :",lz1._e)
        print("orig string num bits needed :",lz1.calc_num_bits_orig())
        print("compressed num bits needed : ",lz1.calc_num_bits_needed())

    def test_A(self):
        self.template("ABCDE")

    def test_B(self):
        self.template(''.join([random.choice(string.ascii_uppercase+string.digits) for s in range(10)]))

    def test_F(self):
        self.template(open('TextFile1.txt','r').read())

    def test_G(self):
        self.template(open('TextFile2.txt','r').read())

    def test_H(self):
        self.template(open('TextFile3.txt','r').read())

if __name__ == '__main__':
    unittest.main()
