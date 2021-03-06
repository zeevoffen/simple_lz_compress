
import struct
import pickle
import math

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
        return tb + len(self._e)*8

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

    def write_p_enc_bin(self,file_name):
        pickle_out = open(file_name,"wb")
        pickle.dump(self._e, pickle_out)
        pickle_out.close()

    def read_p_enc_bin(self,file_name):
        pickle_in = open(file_name,"rb")
        p_enc = pickle.load(pickle_in)
        assert(p_enc==self._e)
                           
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

    def write_n_enc_bin(self,file_name):
        binary_file = open(file_name, "wb")
        print(self._e)
        for i in range(0,len(self._e)):
            tkn=self._e[i]
            #num=self._e[i][1]
            num=tkn[1]
            sym=self._e[i][0]
            sym_frmt=''
            sym_bin=bytes(sym,encoding= 'utf-8')
            sym_l = len(sym_bin)
            for i in range(sym_l) :
                sym_frmt+='c'
            if num<=0xff :
                n_frmt="B"
                num_l=1
            elif num<=0xffff:
                n_frmt="H"
                num_l=2
            else :
                n_frmt+="I"
                num_l=4
            len_byte=(num_l<<4)+sym_l
            final_frmt="B"+n_frmt+sym_frmt
            if sym_l != 0 :
                binary_data = struct.pack(final_frmt,len_byte,num,sym_bin)
            else : 
                binary_data = struct.pack(final_frmt,num,len_byte)
            binary_file.write(binary_data)
            assert(len(binary_data)==(num_l+sym_l+1))
        binary_file.close()

    def write_s_enc_bin(self,file_name):
        binary_file = open(file_name, "wb")
        print(self._e)
        pos=0
        for i in range(0,len(self._e)):
            num=self._e[i][1]
            sym=self._e[i][0]
            sym_bin=bytes(sym,encoding= 'utf-8')
            sym_l = len(sym_bin)
            num_l = math.ceil(num.bit_length()/8)
            num_bin=num.to_bytes(num_l,'big')
            len_byte=(num_l<<4)+sym_l
            len_byte_bin = len_byte.to_bytes(1,'big')
            #binary_data = bytearray([len_byte,num])
            #binary_data += sym_bin
            print(num_l,sym_l)
            binary_data=len_byte_bin+num_bin+sym_bin
            binary_file.write(binary_data)
            pos+=len(binary_data)
            binary_file.seek(pos)
            assert(len(binary_data)==(num_l+sym_l+1))
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






