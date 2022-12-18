
import random

def gen_weak_prime():
    init_base = random.getrandbits(512)
    p = 4
    q = 4
    while not isPrime(p):
        p = (init_base << 512) ^ random.getrandbits(512)
    #print('p', p)
    while not isPrime(q):
        q = (init_base << 512) ^ random.getrandbits(512)
    #print('q', q)
    n = p*q
    #print("DIFF", p-q)
    print("n", n)
    return n


def cryptanalysis(infile_with_key, outfile):
    # with open(infile_with_key, 'r') as file:
    #     content = file.read().split(":")
    # exponent, n = content[0], content[1]
    n = gen_weak_prime()
    #CRAZY BIG n = 5261933844650100908430030083398098838688018147149529533465444719385566864605781576487305356717074882505882701585297765789323726258356035692769897420620858774763694117634408028918270394852404169072671551096321238430993811080749636806153881798472848720411673994908247486124703888115308603904735959457057925225503197625820670522050494196703154086316062123787934777520599894745147260327060174336101658295022275013051816321617046927321006322752178354002696596328204277122466231388232487691224076847557856202947748540263791767128195927179588238799470987669558119422552470505956858217654904628177286026365989987106877656917
    init_guess = isqrt(n) + 1
    while True:
        chck = init_guess**2 - n
        if is_perfect_square(chck):
            b = isqrt(chck)
            break
        init_guess += 1
    p = init_guess - b
    q = init_guess + b
    print("diff", p-q)
    return p, q


def is_perfect_square(a):
    b = isqrt(a)
    return b*b == a


def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def isPrime(n, k=128):

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    for _ in range(k):
        test = random.randint(2, n - 1)
        res = pwrfast(test, n-1, n)
        if res != 1:
            return False
    return True


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


print(cryptanalysis(1, 2))
