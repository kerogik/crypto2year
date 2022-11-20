import regex as re
import math
import galois

def affine(algo, outfile, source_string):
    field_or_ring = int(input("Choose whether you want to encode/decode something over residue class ring (1) or Galois field (2)\n- "))
    if field_or_ring != 1 and field_or_ring != 2:
        print("Wrong number provided. Aborting.")
        return 0
    if algo == "enc":
        if field_or_ring == 1:
            encrypt_ring(source_string, outfile)
        else:
            encrypt_galois(source_string, outfile)
    elif algo == "dec":
        if field_or_ring == 1:
            decrypt_ring(source_string, outfile)
        else:
            decrypt_galois(source_string, outfile)
    return 0


def encrypt_ring(source_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    ZM_RING = 26
    
    alpha = int(input("Pick alpha that belongs to multiplicative group of residue class ring (such that alpha is coprime with 26)\n- "))
    if not is_coprime(alpha, ZM_RING) or alpha > ZM_RING-1:
        print("That is not an appropriate alpha")
        return 0
    if alpha < 0:
        alpha = ZM_RING + alpha
    beta = int(input("Pick beta that belongs to residue class ring\n- "))
    if beta > ZM_RING:
        print("That is not an appropriate beta")
        return 0
    if beta < 0:
        beta = ZM_RING + beta

    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z]', source_string[i]):
            out_string += source_string[i]
        else:
            new_letter = chr((alpha*(ord(source_string[i]) - 97) + beta) % ZM_RING + 97)
            out_string += new_letter

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
    
    alpha = int(input("Pick alpha that belongs to multiplicative group of residue class ring (such that alpha is coprime with 26)\n- "))
    if not is_coprime(alpha, ZM_RING) or alpha > ZM_RING-1:
        print("That is not an appropriate alpha")
        return 0
    if alpha < 0:
        alpha = ZM_RING + alpha
    beta = int(input("Pick beta that belongs to residue class ring\n- "))
    if beta > ZM_RING:
        print("That is not an appropriate beta")
        return 0
    if beta < 0:
        beta = ZM_RING + beta
    
    alpha_rev = rev_broad_euclidean(ZM_RING, alpha)
    
    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z]', source_string[i]):
            out_string += source_string[i]
        else:
            new_letter = chr((ord(source_string[i]) - 97 - beta)*alpha_rev % ZM_RING + 97)
            out_string += new_letter
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)
    
    return 0


def encrypt_galois(source_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    print("Wait while the program generates the Galois field...\n")
    irreducible_poly = galois.irreducible_poly(3,3)
    GF = galois.GF(3**3,irreducible_poly)
    print(f"The program conducts arithmetics over Galua field 3**3, with the irreducible polynomial {irreducible_poly}\n")
    alphabet = [chr(i) for i in range(97,123)]
    alphabet.append(' ')
    alphabet_dict = dict(zip(alphabet, [i for i in range(27)]))

    alpha = int(input("Pick alpha that belongs to Galois field 3**3\n- "))
    if alpha == 0:
        print("That is not an appropriate alpha")
        return 0
    
    beta = int(input("Pick beta that belongs to Galois field 3**3\n- "))
    
    alpha = GF(alpha)
    beta = GF(beta)
    
    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z ]', source_string[i]):
            out_string += source_string[i]
        else:
            ltrnum = alphabet_dict[source_string[i]]
            ltrnum = GF(ltrnum)
            k = int(alpha*(ltrnum) + beta)
            new_letter = alphabet[k]
            out_string += new_letter

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def decrypt_galois(source_string, outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    print("Wait while the program generates the Galois field...\n")
    irreducible_poly = galois.irreducible_poly(3,3)
    GF = galois.GF(3**3,irreducible_poly)
    print(f"The program conducts arithmetics over Galua field 3**3, with the irreducible polynomial {irreducible_poly}\n")

    alphabet = [chr(i) for i in range(97,123)]
    alphabet.append(' ')
    alphabet_dict = dict(zip(alphabet, [i for i in range(27)]))

    alpha = int(input("Pick alpha that belongs to Galois field 3**3\n- "))
    if alpha == 0:
        print("That is not an appropriate alpha")
        return 0
    
    beta = int(input("Pick beta that belongs to Galois field 3**3\n- "))
 
    beta = GF(beta)
    alpha = GF(alpha)

    out_string = ''
    for i in range(len(source_string)):
        if not re.match(r'[a-zA-Z ]', source_string[i]):
            out_string += source_string[i]
        else:
            ltrnum = alphabet_dict[source_string[i]]
            ltrnum = GF(ltrnum)
            k = int((ltrnum - beta)/alpha)
            new_letter = alphabet[k]
            out_string += new_letter

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
    