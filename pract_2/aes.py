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
    #print(source_string)
    if key_string[1] == 1:
        key_string = key_string[0]
    else:
        with open(key_string[0], 'r') as fl:
            key_string = fl.read()
    key_string = int(hashlib.md5(key_string.encode('utf-8')).hexdigest(), 16)

    source_string = binascii.hexlify(source_string)
    blocks = [int((source_string[32*i:32*i+32]), 16) for i in range(len(source_string)//32+1)]
    
    blocks[-1] = hex(blocks[-1])
    len_last = len(blocks[-1])
    cnt = 0
    
    while len_last < 34:
        blocks[-1] += '0'
        cnt += 1
        len_last = len(blocks[-1])
    blocks[-1] = int(blocks[-1], 16)
    blocks.append(cnt)
    
    ###test###
    #blocks = [0x00112233445566778899aabbccddeeff]
    #key_string = 0x000102030405060708090a0b0c0d0e0f
    ###test###

    NUMROUNDS = 10
    roundKeys = []
    blocks_ans = []

    roundKeys = keyExpansion(key_string)

    for block in blocks:
        #1 round
        print(hex(roundKeys[0]), hex(block))
        block = addRoundKey(roundKeys[0],block)
        print(hex(block))
        #rounds 2-9
        for i in range(1, NUMROUNDS):
            print(hex(block))
            block = subBytes(block)
            print(hex(block))
            block = shiftRows(block)
            print(hex(block))
            block = mixColumns(block)
            print(hex(block))
            block = addRoundKey(roundKeys[i],block)
            print(hex(block))
        #last round
        block = subBytes(block)
        print(hex(block))
        block = shiftRows(block)
        print(hex(block))
        ##adjusting bytes
        block = adjust_last_round(block)
        print(hex(block))
        block = addRoundKey(roundKeys[NUMROUNDS], block)
        print(hex(block))
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
    print('this ',hex(block))
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
    for j in words:
        for i in j:
            tmp.append(hex(i))
        print(tmp)
        tmp = []
    for i in range(4):
        reswords_tmp = []
        reswords_tmp.append(gal_mul_2(words[0][i]) ^ gal_mul_3(words[1][i]) ^ words[2][i] ^ words[3][i])
        reswords_tmp.append(words[0][i] ^ gal_mul_2(words[1][i]) ^ gal_mul_3(words[2][i]) ^ words[3][i])
        reswords_tmp.append(words[0][i] ^ words[1][i] ^ gal_mul_2(words[2][i]) ^ gal_mul_3(words[3][i]))
        reswords_tmp.append(gal_mul_3(words[0][i]) ^ words[1][i] ^ words[2][i] ^ gal_mul_2(words[3][i]))
        reswords.append(reswords_tmp)
        print([hex(i) for i in reswords_tmp])
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






def invrotate(a):
    b = (a & 2**8-1) << 24
    #print(hex(b))
    c = (a >> 8)
    #print(hex(c))
    return b^c

def invShiftRows(block):
    words = []
    wordbytes = []
    for i in range(0,4):
        st = 2**32-1
        g = (block << i*32) 
        g = (g >> 32*3) & st
        words.append(g)
    #print([hex(i) for i in words])
    for j in range(4):
        for i in range(4):
            st = 2**8-1
            g = (words[j] << i*8) >> 24
            g = g & st 
            wordbytes.append(g)
            #print(words[j],g)
    
    #print([hex(i) for i in wordbytes])
    wordbytes_new = []
    for i in range(4):
        for j in range(4):
            wordbytes_new.append(wordbytes[i+j*4])
    #print('wordbytes new', [hex(i) for i in wordbytes_new])
    for i in range(4):
        words[i] = 0
        for j in range(4):
            words[i] <<= 8
            words[i] ^= wordbytes_new[4*i+j]
        
    #print([hex(i) for i in wordbytes_new])    
    for i in range(4):
        for j in range(i):
            #print([hex(i) for i in words])
            words[i] = invrotate(words[i])
            #print([hex(i) for i in words])
    #print([hex(i) for i in words])
    block = 0
    for i in range(4):
        block ^= words[i] << 96 - 32*i
    return block


def invsbox(byte):
    for i in range(256):
        test = sbox(i)
        if test == byte:
            res = i
    return res


def invSubBytes(block):
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
    #print([hex(i) for i in wordbytes])
    for i in range(len(wordbytes)):
        wordbytes[i] = invsbox(wordbytes[i])
    #print([hex(i) for i in wordbytes])
    block = 0
    chck = 0
    for i in range(16):
        shft = wordbytes[i] << (120 - 8*i)
        chck = chck ^ shft
        block ^= wordbytes[i] << (120 - 8*i)
    return block


def invMixColumns(block): 
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
    ########
    for j in words:
        for i in j:
            tmp.append(hex(i))
        print(tmp)
        tmp = []
    ########
    for i in range(4):
        reswords_tmp = []
        reswords_tmp.append(gal_multiply(0x0e, words[0][i]) ^ gal_multiply(0x0b, words[1][i]) ^ gal_multiply(0x0d,words[2][i]) ^ gal_multiply(0x09,words[3][i]))
        reswords_tmp.append(gal_multiply(0x09, words[0][i]) ^ gal_multiply(0x0e, words[1][i]) ^ gal_multiply(0x0b,words[2][i]) ^ gal_multiply(0x0d,words[3][i]))
        reswords_tmp.append(gal_multiply(0x0d, words[0][i]) ^ gal_multiply(0x09, words[1][i]) ^ gal_multiply(0x0e,words[2][i]) ^ gal_multiply(0x0b,words[3][i]))
        reswords_tmp.append(gal_multiply(0x0b, words[0][i]) ^ gal_multiply(0x0d, words[1][i]) ^ gal_multiply(0x09,words[2][i]) ^ gal_multiply(0x0e,words[3][i]))
        reswords.append(reswords_tmp)
    #print(reswords)
    block = subblock = 0
    for i in range(4):
        for j in range(4):
            subblock ^= reswords[i][j] << 24 - 8*j
        block ^= subblock << 96 - 32*i
        print(hex(subblock))
        subblock = 0
    #print(hex(block))
    return block


def decrypt(source_string, key_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'rb') as fl:
            source_string = fl.read()
    #print(source_string)
    if key_string[1] == 1:
        key_string = key_string[0]
    else:
        with open(key_string[0], 'r') as fl:
            key_string = fl.read()
    key_string = int(hashlib.md5(key_string.encode('utf-8')).hexdigest(), 16)
    
    #print(key_string)
    source_string = source_string.hex()#binascii.hexlify(source_string)
    #print(source_string, type(source_string))
    
    blocks = [int((source_string[32*i:32*i+32]), 16) for i in range(len(source_string)//32)]
    #print(blocks)
    
    
    ###test###
    #blocks = [0x69c4e0d86a7b0430d8cdb78070b4c55a]
    #key_string = 0x000102030405060708090a0b0c0d0e0f
    ###test###

    NUMROUNDS = 10
    roundKeys = []
    blocks_ans = []

    roundKeys = keyExpansion(key_string)
    print([hex(i) for i in roundKeys])
    print(hex(roundKeys[0]))
    for block in blocks:
        #1 round
        #print(hex(roundKeys[0]), hex(block))
        block = addRoundKey(roundKeys[-1],block)
        print(hex(block))
        #rounds 2-9
        for i in range(1, NUMROUNDS):
            print(hex(block), 'start?')
            block = invShiftRows(block)
            print(i, hex(block))

            block = invSubBytes(block)
            print(i, hex(block))

            block = adjust_last_round(block)

            block = addRoundKey(roundKeys[-1-i],block)
            print(i, hex(block), 'after addr')

            block = adjust_last_round(block)
            print(i, hex(block), 'try rotate')

            block = invMixColumns(block)
            print(i, hex(block))
            
        #last round
        block = invSubBytes(block)
        print('last r', hex(block))
        block = invShiftRows(block)
        print('last r', hex(block))
        ##adjusting bytes
        block = adjust_last_round(block)
        print('last r', hex(block))
        block = addRoundKey(roundKeys[0], block)
        print('last r', hex(block))
        blocks_ans.append(block)
    
    print([hex(i) for i in blocks_ans])
    # print(len(blocks), len(blocks_ans))
    shifted_zeroes = blocks_ans.pop(-1)
    print(shifted_zeroes)
    print([hex(i) for i in blocks_ans])
    blocks_ans[-1] = int(hex(blocks_ans[-1])[:-shifted_zeroes], 16)
    print([hex(i) for i in blocks_ans])
    out_string = ''
    if outfile != 0:
        with open(outfile, 'wb') as outfile:
            for i in blocks_ans:
                len_bytes = (len(hex(i)) - 2) // 2
                print(len_bytes, hex(i))
                outfile.write(i.to_bytes(len_bytes, 'big'))
    else:
        print(out_string)
        print("You need to specify outfiles!")

    return 0