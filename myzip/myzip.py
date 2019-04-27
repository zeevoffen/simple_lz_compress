
#s = "ABABBBAA" # A B AB BB AA
#s = "ABABABB" # A B AB ABB
#s = "AABABBBABAABABBBABBABB"
#A AB ABB B ABA ABAB BB ABBA BB
#∅A 1B 2B ∅B 2A 5B 4B 3A 7
#s = "AB AB AB   " #A B " " AB " "
#s = "ABZABZABZZZ" #A B " " AB " "
#s = "ABAB"*1024
#s= "ABABABAB" * 100

import struct


class lz():
    null=""
    NUM_BYTES_PER_ENC_ENTRY = 5

    def get_compression_ratio(self):
        #orig_string_len = len(self._s) 
        #enc_string_len = len(self._e) * self.NUM_BYTES_PER_ENC_ENTRY
        self._compression_ratio = (self.calc_num_bits_needed()/self.calc_num_bits_orig())*100

    def calc_num_bits_orig(self):
        return (len(self._s)*8)

    def calc_num_bits_needed(self):
        tb=0
        nb=1
        for i in range(0,len(self._e)+1):
            if i>(2**nb) :
                nb+=1
            tb+=(nb+8)
        return tb

    def get_dic_size(self):
        return (len(self._d_dic))


    def get_dic(self,s):
        if s in self._dic :
            return self._dic[s]
        else :
            return self.null

    def update_dic(self,s,sym) :
        self._dic[s] = sym

    def update_tok(self,t) :
        self._t.append(t)

    def update_enc(self,str,t):
         self._e.append([str,t])

    def tokens(self):
        p1=p2=0
        last_t=t=0
        while p2<len(self._s) :
            str = self._s[p1:p2+1]
            d = self.get_dic(str)
            if d==self.null :
                self.update_dic(str,t)
                self.update_tok(str)
                if last_t=='' :
                    u_t=t
                else :
                    u_t=last_t
                self.update_enc(self._s[p2:p2+1],u_t)
                p1=p2+1
                p2=p1
                t+=1
                last_t=''
            else :
                last_t = d
                if p2==(len(self._s)-1) :
                    self.update_tok(str)
                    self.update_enc('',d)
                p2+=1

    def dec(self) :
        for i in range(len(self._e)):
            num=self._e[i][1]
            sym=self._e[i][0]
            if num in self._d_dic:
                s = self._d_dic[num]+sym
                self._d_dic[i]=s
                self._d.append(s)
            else :
                self._d.append(sym)
                self._d_dic[num]=sym

    def read_enc_bin(self,file_name):
        #binary_file = open(file_name, "rb")
        #content = binary_file.read()
        f = open(file_name, "rb")
        nb=1
        bc=0
        while True : 
            if bc > 2**nb :
                nb+=1
            if nb<=8 :
                n_byte_to_read = 2
                frmt = "Bc"
            elif nb<=16 :
                n_byte_to_read = 3
                frmt = "Hc"
            elif nb<=32 :
                n_byte_to_read = 5
                frmt = "Ic"
            bin_data = f.read(n_byte_to_read)
            if bin_data == b"":
                break
            else : 
                size = len(bin_data)
                if size < n_byte_to_read:
                    if size==1 :
                        frmt="B"
                    elif size==2 :
                        frmt="H"
                    else :
                        frmt="I"
                data_tpl = struct.unpack(frmt,bin_data)
            indx= data_tpl[0]
            e_indx= self._e[bc][1]
            if len(data_tpl)==2:
                char= data_tpl[1].decode()
            else :
                char = ''
            e_char= self._e[bc][0]
            assert(indx==e_indx)
            assert(char==e_char)
            bc+=1
            #print('tpl:',data_tpl)
           
    def write_enc_bin(self,file_name):
        binary_file = open(file_name, "wb")
        tb=0
        nb=1
        for i in range(0,len(self._e)):
            num=self._e[i][1]
            sym=self._e[i][0]
            sym_bin=bytes(sym,encoding= 'utf-8')
            if i>(2**nb) :
                nb+=1
            if nb<=8 :
                format = "B"
            elif nb<=16 :
                format = "H"
            else :
                format = "I"
            if sym=='' :
                binary_data = struct.pack(format, num)
            else :
                format+='c'
                binary_data = struct.pack(format, num, sym_bin)
            binary_file.write(binary_data)
        binary_file.close()

    def __init__(self,s):
        self._dic = {}
        self._d_dic = {}
        self._s = ""
        self._t = []
        self._e=  []
        self._d = []
        self._s = s
        self.tokens()
        self.dec()
        assert(self._d==self._t),"decoded {} != original {}".format(self._d,self._t)
        self.get_compression_ratio()

    def __repr__(self) :
        return "original string :"+ str(self._s) + "\ntokens : "+str(self._t)\
            +"\ndictionary : "+str(self._dic)+"\nencoded : "+str(self._e)\
            +"\ndecoded : "+str(self._d)+"\ndec dictionary : "+str(self._d_dic)\
            +"\ncompression ratio: "+str(self._compression_ratio)+"%"



#lz1 = lz("A")

#print(lz1)




