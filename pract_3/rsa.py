import math
import random
import binascii

def rsa(algo, outfile, source_string, key_string):
    if algo == "gen":
        genkeypair()
    elif algo == "enc":
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
    source_string = source_string.hex()
    #print('start hex', source_string, len(source_string))
    with open(f"{key_string[0]}", 'r') as file:
        ksfl = file.read().split(':')
        e, n = int(ksfl[0]), int(ksfl[1])


    hex_str_len = len(source_string)
    #print(hex_str_len)
    bin_str = bin(int(source_string, 16))[2:].zfill(((hex_str_len + 1) // 2) * 8)
    #print('start bin', bin_str)
    bin_blocks = []
    ##test
    # n = 26745475138272326665571528269272188086186709795747103505080525569912375504296909718120540410009324249310934073066414405543088621232185553897148743964010006913207564430655901997367299362802551320676155053237899167694027545908671893829442952075518510518154361518202424126502309316440638573529190495603308306197330660740827488303010883475390605821329712793997286532800168152497399881402064215295895138014153568451044493036618741016712150389513859781367191579427518672705453957782259245727268547063177911172691057600334333273778663577217285520232067866634027743156366389661049321144194653577114283389021364074743528572273
    # e = 47
    ##test

    lenbl1 = math.floor(math.log2(n))
    #print(lenbl1)
    left_zeros = len(bin_str) % lenbl1
    bin_str = '0'*(lenbl1-left_zeros) + bin_str
    #print(bin_str)
    #print(bin_str)
    for i in range(len(bin_str)//lenbl1):
        bin_blocks.append(bin_str[i*lenbl1:lenbl1+i*lenbl1])
    #print([(i, len(i)) for i in bin_blocks])
    #print([int(i,2) for i in bin_blocks], len(bin_blocks))

    powers_nums = [pwrfast(int(i, 2), e, n) for i in bin_blocks]
    #print([(bin(i)[2:], len(bin(i)[2:])) for i in powers_nums], len(powers_nums))
    lenbl2 = math.floor(math.log2(n))+1
    bin_encr = ''.join([bin(i)[2:].zfill(lenbl2) for i in powers_nums])
    #print('encr bin', bin_encr, len(bin_encr), lenbl2)
    hex_encr = hex(int(bin_encr,2))
    #print('encr hex', hex_encr, len(hex_encr))
    if len(hex_encr) % 2 != 0:
        hex_encr = hex_encr[:2]+'0'+hex_encr[2:]
    hex_encr_bytes = bytes.fromhex(hex_encr[2:])
    #print(hex_encr_bytes)
    
    out_string = ''
    if outfile != 0:
        with open(outfile, 'wb') as outfile:
            outfile.write(hex_encr_bytes)
    else:
        print(out_string)

    return 0

def decrypt(source_string, key_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'rb') as fl:
            source_string = fl.read()
    source_string = source_string.hex()
    with open(f"{key_string[0]}", 'r') as file:
        ksfl = file.read().split(':')
        d, n = int(ksfl[0]), int(ksfl[1])

    lenbl2 = math.floor(math.log2(n)) + 1
    int_src_str = int(source_string, 16)
    hex_str_len = len(source_string)

    bin_src_str = bin(int_src_str)[2:].zfill(((hex_str_len + 1) // 2) * 8).zfill(lenbl2)
    
    bin_blocks = []
    for i in range(len(bin_src_str)//lenbl2):
        bin_blocks.append(bin_src_str[i*lenbl2:lenbl2+i*lenbl2])
    
    lenbl1 = math.floor(math.log2(n))
    powers_blocks = [pwrfast(int(i, 2), d, n) for i in bin_blocks]
    bin_str = ''.join([bin(i)[2:].zfill(lenbl1) for i in powers_blocks])
    
    int_str = int(bin_str, 2)
    hex_str_len = len(hex(int_str)[2:])
    if hex_str_len % 2 != 0:
        hex_str = '0' + hex(int_str)[2:]
    else:
        hex_str = hex(int_str)[2:]
    bytes_hex = bytes.fromhex(hex_str)


    out_string = ''
    if outfile != 0:
        with open(outfile, 'wb') as outfile:
            outfile.write(bytes_hex)
    else:
        print(out_string)

    return 0


def genkeypair():
    e, p, q = genpublickey()
    euler_val = (p-1)*(q-1)
    n = p*q
    with open('public_key.rsakey', 'w') as fl:
        fl.write(str(e)+':'+str(n))
        print('Public key: ', e, n)
    d = genprivatekey(n, euler_val, e)
    with open('private_key.rsakey', 'w') as fl:
        fl.write(str(d)+':'+str(n))
        print('Private key:', d, n)
    
    test_correctness = pwrfast(pwrfast(111111, e ,n), d, n)
    if test_correctness != 111111:
        print('Warning: Failed attempt, the keys are bad, retrying...')
        genkeypair()
    
    
    return 0


def genpublickey():
    length = int(input("enter the bit length of n\n")) // 2
    p, q = rsa_primepair(length)
    encr_exponent = 13#int(input("enter encryption exponent\n")) ###//TODO: change exponent to be the chosen value
    euler_val = (p-1)*(q-1)
    while not is_coprime(euler_val, encr_exponent):
        p, q = rsa_primepair()
        encr_exponent = 13 ###//TODO: change exponent to be the chosen value
        euler_val = (p-1)*(q-1)
    return encr_exponent, p, q


def genprivatekey(n, euler_val, encr_exponent):
    
    res_eucl = rev_broad_euclidean(euler_val, encr_exponent) 
    decr_exponent = res_eucl + n * (res_eucl < 0)

    return decr_exponent


def rsa_primepair(len):
    p, q = genPrime(len), genPrime(len)
    return p, q


def genPrimeMaybe(len):
    bts = random.getrandbits(len)
    bts |= (1 << len - 1) | 1 #//TEST //TEST TEST
    return bts


def isPrime(n, k=128):

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # 
    # Miller-Rabin algorithm
    # 

    # s = 0
    # r = n - 1
    # while r & 1 == 0:
    #     s += 1
    #     r //= 2
    # for _ in range(k):
    #     a = random.randrange(2, n-1)
    #     x = pow(a, r, n)
    #     if x != 1 and x != n - 1:
    #         j = 1
    #         while j < s and x != n-1:
    #             x = pow(x, 2, n)
    #             if x == 1:
    #                 return False
    #             j += 1
    #         if x != n - 1:
    #             return False

    #
    # Fermat primality test
    #

    for _ in range(k):
        test = random.randint(2, n - 1)
        res = pwrfast(test, n-1, n)
        if res != 1:
            return False
    return True


def genPrime(len = 1024):
    val = 4
    while not isPrime(val, 128):
        val = genPrimeMaybe(len)
        #print(val, '\nNOT VALID')
    return val


def rev_broad_euclidean(a, b):
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while b != 0:
        q = a // b
        r = a % b
        x = x2 - q*x1
        y = y2- q*y1
        a = b
        b = r
        x2 = x1
        y2 = y1
        x1 = x
        y1 = y
    return y2


def is_coprime(a, b):
    return math.gcd(a,b) == 1

def pwrfast(a, n, m):
    power = n
    outer_number = 1
    while power != 1:
        if power % 2 == 1:
            outer_number *= a
            outer_number %= m
            power -= 1
        a **= 2
        a %= m
        power //=2
        #print(f"{outer_number}*({int_src_str})**{power}")
    int_plaintext = outer_number * a % m
    return int_plaintext


