import binascii
import hashlib

def aes(algo, outfile, source_string, key_string):
    if algo == "enc":
        encrypt(source_string, key_string, outfile)
    elif algo == "dec":
        decrypt(source_string, key_string, outfile)
    return 0


def encrypt(source_string, key_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'rb') as fl:
            source_string = fl.read()
    print(source_string)
    if key_string[1] == 1:
        key_string = key_string[0]
    else:
        with open(key_string[0], 'r') as fl:
            key_string = fl.read()
    key_string = int(hashlib.md5(key_string.encode('utf-8')).hexdigest(), 16)

    source_string = binascii.hexlify(source_string)
    blocks = [int((source_string[32*i:32*i+32]), 16) for i in range(len(source_string)//32+1)]
    
    #print([hex(i) for i in blocks])
    
    blocks[-1] = hex(blocks[-1])
    len_last = len(blocks[-1])
    cnt = 0
    
    while len_last < 34:
        blocks[-1] += '0'
        cnt += 1
        print(cnt)
        len_last = len(blocks[-1])
        print(len_last, blocks[-1])
    blocks[-1] = int(blocks[-1], 16)
    print(hex(blocks[-1]))
    blocks.append(cnt)
    print(blocks)
    NUMROUNDS = 10
    roundKeys = []
    blocks_ans = []

    roundKeys = keyExpansion(key_string)

    for block in blocks:
        #1 round
        #print(hex(roundKeys[0]), hex(block))
        block = addRoundKey(roundKeys[0],block)
        #print(hex(block))
        #rounds 2-9
        for i in range(1, NUMROUNDS):
            #print(hex(block))
            block = subBytes(block)
            #print(hex(block))
            block = shiftRows(block)
            #print(hex(block))
            block = mixColumns(block)
            #print(hex(block))
            block = addRoundKey(roundKeys[i],block)
            #print(hex(block))
        #last round
        block = subBytes(block)
        #print(hex(block))
        block = shiftRows(block)
        #print(hex(block))
        ##adjusting bytes
        block = adjust_last_round(block)
        #print(hex(block))
        block = addRoundKey(roundKeys[NUMROUNDS], block)
        #print(hex(block))
        blocks_ans.append(block)
    
    print([hex(i) for i in blocks_ans])
    # print(len(blocks), len(blocks_ans))
    out_string = ''
    if outfile != 0:
        with open(outfile, 'wb') as outfile:
            for i in blocks_ans:
                outfile.write(i.to_bytes(16, 'big'))
    else:
        print(out_string)

    return 0


def decrypt(source_string, key_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    
    if key_string[1] == 1:
        key_string = key_string[0]
    else:
        with open(key_string[0], 'r') as fl:
            key_string = fl.read()

    #
    out_string = ''
    #

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def bit_count(value):
    return bin(value).count('1')


def sbox(byte):
    if byte == 0:
        inv_a = 0
    else:
        inv_a = inv(0x11B, byte)
    res = 0
    mat = [
        0b11110001,
        0b11100011,
        0b11000111,
        0b10001111,
        0b00011111,
        0b00111110,
        0b01111100,
        0b11111000,
    ]
    for i in range(8):
        res ^= (bit_count(mat[i] & inv_a) % 2) << i
    res ^= 0x63
    return res


def subBytes(block):
    words = []
    for i in range(0,4):
        st = 2**32-1
        g = (block << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    wordbytes = []
    for j in range(4):
        for i in range(4):
            st = 2**8-1
            g = (words[j] << i*8)
            g = (g >> 8*3) & st
            wordbytes.append(g)
    for i in range(len(wordbytes)):
        wordbytes[i] = sbox(wordbytes[i])
    block = 0
    chck = 0
    for i in range(16):
        shft = wordbytes[i] << (120 - 8*i)
        chck = chck ^ shft
        block ^= wordbytes[i] << (120 - 8*i)
    return block


def shiftRows(block):
    words = []
    wordbytes = []
    for i in range(0,4):
        st = 2**32-1
        g = (block << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    for j in range(4):
        for i in range(4):
            st = 2**8-1
            g = (words[j] << i*8) 
            g = (g >> 8*3) & st
            wordbytes.append(g)
    #print([hex(i) for i in wordbytes])
    wordbytes_new = []
    for i in range(4):
        for j in range(4):
            wordbytes_new.append(wordbytes[i+j*4])
    for i in range(4):
        words[i] = 0
        for j in range(4):
            words[i] <<= 8
            words[i] ^= wordbytes_new[4*i+j]
        
    #print([hex(i) for i in wordbytes_new])    
    for i in range(4):
        for j in range(i):
            words[i] = rotate(words[i])
    #print([hex(i) for i in words])
    block = 0
    for i in range(4):
        block ^= words[i] << 96 - 32*i
    return block


def mixColumns(block):
    words = []
    reswords = []
    for i in range(0,4):
        st = 2**32-1
        g = (block << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    tmp = []
    for j in range(4):
        for i in range(4):
            st = 2**8-1
            g = (words[j] << i*8) 
            g = (g >> 8*3) & st
            tmp.append(g)
        words[j] = [i for i in tmp]
        tmp = []
    for i in range(4):
        reswords_tmp = []
        reswords_tmp.append(gal_mul_2(words[0][i]) ^ gal_mul_3(words[1][i]) ^ words[2][i] ^ words[3][i])
        reswords_tmp.append(words[0][i] ^ gal_mul_2(words[1][i]) ^ gal_mul_3(words[2][i]) ^ words[3][i])
        reswords_tmp.append(words[0][i] ^ words[1][i] ^ gal_mul_2(words[2][i]) ^ gal_mul_3(words[3][i]))
        reswords_tmp.append(gal_mul_3(words[0][i]) ^ words[1][i] ^ words[2][i] ^ gal_mul_2(words[3][i]))
        reswords.append(reswords_tmp)
    #print(reswords)
    block = subblock = 0
    for i in range(4):
        for j in range(4):
            subblock ^= reswords[i][j] << 24 - 8*j
        block ^= subblock << 96 - 32*i
        subblock = 0
    #print(hex(block))
    return block


def addRoundKey(roundKey, block):
    return roundKey ^ block


def gal_multiply(a , b):

    p = 0x00
    
    for i in range(8):
        if b & 1 != 0:
            p = p ^ a

        check = a & 0x80 != 0

        a = a << 1

        if check:
            a = a ^ 0x11B
        
        b = b >> 1
    return p


def gal_mul_2(a):
    h = a & 0x80
    b = a << 1
    if h == 0x80:
        b ^= 0x11b
    return b


def gal_mul_3(a):
    return gal_mul_2(a) ^ a


def rotate(a):
    b = a << 8 & 2**32-1
    c = ((a << 8) >> 32)
    return b^c


def rcon(val):
    c = 1
    if (val == 0):
        return 0
    while val != 1:
        c = gal_multiply(c,2)
        val -= 1
    return c << 24


def gal_degree(a):
    res = 0
    a >>= 1
    while a != 0:
        a >>= 1
        res += 1
    return res


def inv(m, a):
    
    y2 = 0
    y1 = 1
    shft = gal_degree(a) - 8
    
    while a != 1:
        
        if shft < 0:
            m, a = a, m
            y2, y1 = y1, y2
            shft = -shft
        
        a = a ^ (m << shft)
        y1 = y1 ^ (y2 << shft)
        
        shft = gal_degree(a) - gal_degree(m)

    return y1


def subWord(word):
    wordbytes = []
    for i in range(4):
        st = 2**8-1
        g = (word << i*8) 
        g = (g >> 8*3) & st
        wordbytes.append(g)
    res = 0
    for i in range(4):
        wordbytes[i] = sbox(wordbytes[i])
    for i in range(4):
        res ^= wordbytes[i] << (3-i)*8
    return res


def keyExpansion(key):
    R = 10
    N = 4
    words = []
    for i in range(0,4):
        st = 2**32-1
        g = (key << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    for i in range(N, N*(R+1)):
        if i % N == 0:
            sbwrd = subWord(rotate(words[i-1]))
            rcn = rcon(i // N)
            words.append(words[i-N] ^ sbwrd ^ rcn)
        else:
            words.append(words[i-N] ^ words[i-1])
    ans = []
    subans = 0
    for j in range(0,len(words), 4):
        for i in range(0,4):
            subans = (subans << 32) ^ words[j+i] 
        ans.append(subans)
        subans = 0
    return ans


def adjust_last_round(block):
    words = []
    wordbytes = []
    for i in range(0,4):
        st = 2**32-1
        g = (block << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    for j in range(4):
        for i in range(4):
            st = 2**8-1
            g = (words[j] << i*8) 
            g = (g >> 8*3) & st
            wordbytes.append(g)
    #print([hex(i) for i in wordbytes])
    wordbytes_new = []
    for i in range(4):
        for j in range(4):
            wordbytes_new.append(wordbytes[i+j*4])
    for i in range(4):
        words[i] = 0
        for j in range(4):
            words[i] <<= 8
            words[i] ^= wordbytes_new[4*i+j]
    block = 0
    for i in range(4):
        block <<= 32
        block ^= words[i]
    return block