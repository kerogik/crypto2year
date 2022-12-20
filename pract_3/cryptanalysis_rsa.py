
import random

def gen_weak_prime():
    lng = 1024
    init_base = random.getrandbits(lng)
    p = 4
    q = 4
    while not isPrime(p):
        p = (init_base << lng) ^ random.getrandbits(lng)
    print('p', p)
    while not isPrime(q):
        q = (init_base << lng) ^ random.getrandbits(lng)
    print('q', q)
    n = p*q
    #print("DIFF", p-q)
    print("n", n)
    return n


def cryptanalysis(infile_with_key, outfile):
    n = gen_weak_prime()
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
