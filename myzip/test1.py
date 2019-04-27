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
        return lz1

    def test_A(self):
        lz = self.template("ABCDE")
        lz.write_enc_bin("kuki.zz")
        lz.read_enc_bin("kuki.zz")

    def test_B(self):
        self.template(''.join([random.choice(string.ascii_uppercase+string.digits) for s in range(10)]))

    def test_C(self):
        self.template(''.join([random.choice(string.ascii_uppercase+string.digits) for s in range(1000000)]))

    def test_F(self):
        lz = self.template(open('TextFile1.txt','r').read())
        lz.write_enc_bin("kuki.zz")
        print("encoded :",lz._e)
        lz.read_enc_bin("kuki.zz")

    def test_G(self):
        self.template(open('TextFile2.txt','r').read())

    def test_H(self):
        self.template(open('TextFile3.txt','r').read())

    def test_I(self):
        lz = self.template(open('TextFile4.txt','r').read())
        lz.write_enc_bin("kuki.zz")
        lz.read_enc_bin("kuki.zz")

if __name__ == '__main__':
    unittest.main()
