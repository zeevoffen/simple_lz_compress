
#s = "ABABBBAA" # A B AB BB AA
#s = "ABABABB" # A B AB ABB
#s = "AABABBBABAABABBBABBABB"
#A AB ABB B ABA ABAB BB ABBA BB
#∅A 1B 2B ∅B 2A 5B 4B 3A 7
#s = "AB AB AB   " #A B " " AB " "
#s = "ABZABZABZZZ" #A B " " AB " "
class lz():
    null=""
    _dic = {}
    _d_dic = {}
    _s = ""
    _t = []
    _e=  []
    _d = []

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
            #last_tok = (i==(len(self._e)-1))
            if num in self._d_dic:
                #if last_tok :
                #    s = sym
                #else :
                s = self._d_dic[num]+sym
                self._d_dic[i]=s
                self._d.append(s)
            else :
                self._d.append(sym)
                self._d_dic[num]=sym
          

    def __init__(self,s):
        self._s = s
        self.tokens()
        self.dec()
        assert(self._d==self._t),"decoded != original"

    def __repr__(self) :
        return "original string :"+ str(self._s) + "\ntokens : "+str(self._t)\
            +"\ndictionary : "+str(self._dic)+"\nencoded : "+str(self._e)\
            +"\ndecoded : "+str(self._d)+"\ndec dictionary : "+str(self._d_dic)



lz1 = lz(s)

print(lz1)




