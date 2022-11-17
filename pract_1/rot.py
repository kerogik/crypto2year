import regex as re

def rot(algo, outfile, source_string):
    if algo == "enc":
        encrypt(source_string, outfile)
    elif algo == "dec":
        decrypt(source_string, outfile)
    return 0


def encrypt(source_string, outfile):

    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()

    rot_number = int(input("Enter number by which you want to rotate your string. The true Caesar way is 13!\n"))
    out_string = ''.join([source_string[i] if not re.match(r'[a-zA-Z]', source_string[i]) else chr((ord(source_string[i]) - 97 + rot_number) % 26 + 97) for i in range(len(source_string))])

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def decrypt(source_string, outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()

    rot_number = int(input("Enter number by which you want your string was rotated\n"))
    out_string = ''.join([source_string[i] if not re.match(r'[a-zA-Z]', source_string[i]) else chr((ord(source_string[i]) - 97 - rot_number) % 26 + 97) for i in range(len(source_string))])

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0