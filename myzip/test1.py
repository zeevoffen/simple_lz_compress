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
        #lz.write_enc_bin("kuki.zz")
        lz.write_n_enc_bin("kuki.zz")
        #lz.read_enc_bin("kuki.zz")

    def test_B(self):
        for n in range(100) :
            lz = self.template(''.join([random.choice(string.ascii_uppercase+string.digits) for s in range(10)]))
            lz.write_n_enc_bin("kuki.zz")


    def test_C(self):
        self.template(''.join([random.choice(string.ascii_uppercase+string.digits) for s in range(1000000)]))

    def test_F(self):
        lz = self.template(open('TextFile1.txt','r').read())
        lz.write_enc_bin("TextFile1.zz")
        lz.read_enc_bin("TextFile1.zz")
        lz.write_p_enc_bin("TextFile1.zzp")
        lz.read_p_enc_bin("TextFile1.zzp")
        print(lz)

    def test_G(self):
        lz=self.template(open('TextFile2.txt','r').read())
        lz.write_enc_bin("TextFile2.zz")
        lz.read_enc_bin("TextFile2.zz")


    def test_H(self):
        lz=self.template(open('TextFile3.txt','r').read())
        lz.write_enc_bin("TextFile3.zz")
        lz.read_enc_bin("TextFile3.zz")

    def test_I(self):
        lz = self.template(open('TextFile4.txt','r').read())
        lz.write_enc_bin("kuki.zz")
        lz.read_enc_bin("kuki.zz")

    def test_J(self):
        lz = self.template(open('TextFile1.txt','r').read())
        #lz.write_enc_bin("TextFile1.zz")
        #lz.read_enc_bin("TextFile1.zz")
        lz.write_s_enc_bin("TextFile1.zzn")
        #print(lz)

    def test_K(self):
        lz = self.template(open('TextFile3.txt','r').read())
        #lz.write_enc_bin("TextFile1.zz")
        #lz.read_enc_bin("TextFile1.zz")
        lz.write_s_enc_bin("TextFile3.zzn")
        #print(lz)

if __name__ == '__main__':
    unittest.main()
