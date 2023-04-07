    
import time
import numpy as np


#Parameters of S box
S_Box = np.array([6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11],dtype=np.uint16)

#Parameters of P box
P_Box = np.array([1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16],dtype=np.uint16)
KP_Box =np.array( [1, 2, 3, 4, 9, 10, 11, 12, 5, 6, 7, 8, 13, 14, 15, 16],dtype=np.uint16)

tmp_arr = np.array([0,4,8,12],dtype = np.uint16)
def bytes_(integer):
    return divmod(integer, 0x100)

def gen_K_list(K):
    Ks = np.arange(5,dtype=np.uint16)
    Ks[0] = K
    for i in range(1,5):
        high, low = bytes_(Ks[i-1])
        #circular shift on high 8 bits and on low 8bits
        tmp_high = high>>6
        tmp_low = low>>6
        high =  (high << 2 & 0xff) + tmp_high
        low = (low << 2 & 0xff) + tmp_low
        num=(high<<8)|(low)
        #permutate
        if(i==4):
            Ks[i]=(num)
        else: 
            Ks[i]=(pi_p(KP_Box,num))   
    return Ks


def pi_s(s_box, ur):
    
    vr = 0
    
    for i in range(4):
        uri = ur % (16)
        vri = s_box[uri]
        vr = vr + (vri << tmp_arr[i])
        ur = ur >> 4
    return vr


def pi_p(p_box, vr):
    
    wr = 0
    for i in range(15, -1, -1):
        vri = vr % 2
        vr = vr >> 1
        wr = wr + (vri << (16 - p_box[i]))
    return wr


def reverse_Sbox(s_box):
    
    re_box = np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],dtype=np.uint16)
    for i in range(16):
        re_box[s_box[i]] = i
    return re_box


def reverse_Pbox(p_box):
   
    re_box = np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],dtype=np.uint16)
    for i in range(16):
        re_box[p_box[i] - 1] = i + 1
    return re_box


def do_SPN(x, s_box, p_box, Ks):
    
    wr = x
    for r in range(3):
        Ur = wr ^ Ks [r] #XOR operation
        vr = pi_s (s_box, Ur) # packet substitution
        wr = pi_p (p_box, vr)  #single bit permutation

    ur = wr ^ Ks[3]
    vr = pi_s(s_box, ur)
    y = vr ^ Ks[4]
    return y


def encrypt(Ks,x):
    
    return do_SPN(x, S_Box, P_Box, Ks)


def decrypt(Ks, S_rbox, P_rbox,y):
    
    
    return do_SPN(y, S_rbox, P_rbox, Ks)

if __name__ == '__main__':
    #f = open("number.txt", "r")
    s = "abcd"
    s = bytes(s, 'utf-8')
    s = bytearray(s)
    print(len(s))
    s = s[0:1_000_000]
    
    text = np.arange(np.ceil(len(s))/2,dtype=np.uint16)
    text1 = np.arange(np.ceil(len(s))/2,dtype=np.uint16)
    text2 =np.arange(np.ceil(len(s))/2,dtype=np.uint16)
    K = gen_K_list(0xa1e9)
    print("Key list:",end=" ")
    for i in K:
        print(hex(i),end=" ")
    start = time.perf_counter()
    for i in range(0,len(s),2) :
        if i < len(s)-1:
            x = (s[i]<<8)|s[i+1]
        else:
           x = s[i]
        text[int(i/2)] = x

        
    end = time.perf_counter()
    print("")
    print(end-start)
    print("Encryption Starting...")
    start = time.perf_counter()
    for i,num in enumerate(text):
        text1[i] = encrypt (K,num)
    end = time.perf_counter()
    print("Encryption Ended:...")
    print(end-start)
   
    
    
    K = list(K)
    K.reverse()
    print("Reverse key list:",end=" ")
    for i in K:
        print(hex(i),end=" ")
    K = np.array(K,dtype=np.uint16)
    
    # Secret key replacement
    K[1] = pi_p(P_Box, K[1])
    K[2] = pi_p(P_Box, K[2])
    K[3] = pi_p(P_Box, K[3])

    S_rbox = reverse_Sbox (S_Box) # S-box inversion
    
    P_rbox = reverse_Pbox (P_Box) # P-box inversion
    print("\nDecryption Starting...")
    start = time.perf_counter()
    for i,num in enumerate(text1):
        text2[i] = decrypt (K,S_rbox,P_rbox,num)
    end = time.perf_counter()
    print("Decryption Ended:...")
    print(end-start)
    for i in range(len(text1)):
        print(hex(text[i]),hex(text1[i]),hex(text2[i]))



    file1 = open("First_File.txt", "w")
    key = gen_K_list(0x0)
    for i in range(0xffff+1):
        j = encrypt(key,i)
        file1.write("("+str(hex(i))+","+str(hex(j))+") ")
    file2 = open("Second_File.txt", "w")
    for i in range(0xffff+1):
        j = encrypt(gen_K_list(i),0x0)
        file2.write("("+str(hex(i))+","+str(hex(j))+") ")


