import math
import regex as re

def affine_recurrent(algo, outfile, source_string):
    field_or_ring = int(input("Choose whether you want to encode/decode something over residue class ring (1) or Galois field (2)\n- "))
    if field_or_ring != 1 and field_or_ring != 2:
        print("Wrong number provided. Aborting.")
        return 0
    if algo == "enc":
        if field_or_ring == 1:
            encrypt_ring(source_string, outfile)
        else:
            pass
    elif algo == "dec":
        if field_or_ring == 1:
            decrypt_ring(source_string, outfile)
        else:
            pass
    return 0


def encrypt_ring(source_string, outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    ZM_RING = 26

    alpha_1 = int(input("Pick alpha_1 that belongs to multiplicative group of residue class ring (such that alpha_1 is coprime with 26)\n- "))
    if not is_coprime(alpha_1, ZM_RING) or alpha_1 > ZM_RING-1:
        print("That is not an appropriate alpha_1")
        return 0
    if alpha_1 < 0:
        alpha_1 = ZM_RING + alpha_1
    beta_1 = int(input("Pick beta_1 that belongs to residue class ring\n- "))
    if beta_1 > ZM_RING:
        print("That is not an appropriate beta_1")
        return 0
    if beta_1 < 0:
        beta_1 = ZM_RING + beta_1

    alpha_2 = int(input("Pick alpha_2 that belongs to multiplicative group of residue class ring (such that alpha_2 is coprime with 26)\n- "))
    if not is_coprime(alpha_2, ZM_RING) or alpha_2 > ZM_RING-1:
        print("That is not an appropriate alpha_2")
        return 0
    if alpha_2 < 0:
        alpha_2 = ZM_RING + alpha_2
    beta_2 = int(input("Pick beta_2 that belongs to residue class ring\n- "))
    if beta_2 > ZM_RING:
        print("That is not an appropriate beta_2")
        return 0
    if beta_2 < 0:
        beta_2 = ZM_RING + beta_2
    
    decoded_letters= ''
    clean_string = re.sub(r'[^a-zA-Z]',"",source_string)
    decoded_letters += chr((alpha_1*(ord(clean_string[0]) - 97) + beta_1) % ZM_RING + 97)
    decoded_letters += chr((alpha_2*(ord(clean_string[1]) - 97) + beta_2) % ZM_RING + 97)
    for i in range(2, len(clean_string)):
        alpha_cur = alpha_1*alpha_2 % ZM_RING
        alpha_1 = alpha_2
        alpha_2 = alpha_cur
        beta_cur = (beta_1 + beta_2) % ZM_RING
        beta_1 = beta_2
        beta_2 = beta_cur
        decoded_letters += chr((alpha_cur*(ord(clean_string[i]) - 97) + beta_cur) % ZM_RING + 97)

    count_non_alpha = 0
    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z]', source_string[i]):
            out_string += source_string[i]
            count_non_alpha +=1
        else:
            out_string += decoded_letters[i-count_non_alpha]
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def decrypt_ring(source_string, outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    ZM_RING = 26
    
    alpha_1 = int(input("Pick alpha_1 that belongs to multiplicative group of residue class ring (such that alpha_1 is coprime with 26)\n- "))
    if not is_coprime(alpha_1, ZM_RING) or alpha_1 > ZM_RING-1:
        print("That is not an appropriate alpha_1")
        return 0
    if alpha_1 < 0:
        alpha_1 = ZM_RING + alpha_1
    beta_1 = int(input("Pick beta_1 that belongs to residue class ring\n- "))
    if beta_1 > ZM_RING:
        print("That is not an appropriate beta_1")
        return 0
    if beta_1 < 0:
        beta_1 = ZM_RING + beta_1

    alpha_2 = int(input("Pick alpha_2 that belongs to multiplicative group of residue class ring (such that alpha_2 is coprime with 26)\n- "))
    if not is_coprime(alpha_2, ZM_RING) or alpha_2 > ZM_RING-1:
        print("That is not an appropriate alpha_2")
        return 0
    if alpha_2 < 0:
        alpha_2 = ZM_RING + alpha_2
    beta_2 = int(input("Pick beta_2 that belongs to residue class ring\n- "))
    if beta_2 > ZM_RING:
        print("That is not an appropriate beta_2")
        return 0
    if beta_2 < 0:
        beta_2 = ZM_RING + beta_2

    decoded_letters= ''
    clean_string = re.sub(r'[^a-zA-Z]',"",source_string)
    rev_alpha_1 = rev_broad_euclidean(ZM_RING, alpha_1)
    decoded_letters += chr((ord(clean_string[0]) - 97 - beta_1)*rev_alpha_1 % ZM_RING + 97)
    rev_alpha_2 = rev_broad_euclidean(ZM_RING, alpha_2)
    decoded_letters += chr((ord(clean_string[1]) - 97 - beta_2)*rev_alpha_2 % ZM_RING + 97)
    for i in range(2, len(clean_string)):
        rev_alpha_cur = rev_alpha_1*rev_alpha_2 % ZM_RING
        rev_alpha_1 = rev_alpha_2
        rev_alpha_2 = rev_alpha_cur
        beta_cur = (beta_1 + beta_2) % ZM_RING
        beta_1 = beta_2
        beta_2 = beta_cur
        decoded_letters += chr((ord(clean_string[i]) - 97 - beta_2)*rev_alpha_2 % ZM_RING + 97)

    count_non_alpha = 0
    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z]', source_string[i]):
            out_string += source_string[i]
            count_non_alpha +=1
        else:
            out_string += decoded_letters[i-count_non_alpha]
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def is_coprime(a, b):
    return math.gcd(a,b) == 1


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
