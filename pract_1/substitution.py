import regex as re

def substitution(algo, outfile, source_string):
    if algo == "enc":
        encrypt(source_string, outfile)
    elif algo == "dec":
        decrypt(source_string, outfile)
    return 0


def encrypt(source_string,outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()

    alphabet, len_alphabet = count_unique_symbols(source_string)
    key = input(f"Enter the key, in which symbols correspond to symbols of the alphabet, of the length same as alphabet of length {len_alphabet}:\n{' '.join(alphabet)}\n").split(' ')
    key_dict = dict(zip(alphabet, key))
    out_string = ''.join([source_string[i] if not source_string[i] in key_dict else key_dict[source_string[i]] for i in range(len(source_string))])
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)
    
    return 0


def decrypt(source_string,outfile):
    
    if source_string[1] == 1:
        source_string = source_string[0]
    else:
        with open(source_string[0], 'r') as fl:
            source_string = fl.read()
    source_string = source_string.lower()
    
    alphabet, len_alphabet = count_unique_symbols(source_string)
    key = input(f"Enter the key, in which symbols correspond to symbols of the alphabet, of the length same as alphabet of length {len_alphabet}:\n{' '.join(alphabet)}\n").split(' ')
    key_dict = dict(zip(alphabet, key))
    out_string = ''.join([source_string[i] if not source_string[i] in key_dict else key_dict[source_string[i]] for i in range(len(source_string))])

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(out_string)
    else:
        print(out_string)

    return 0


def count_unique_symbols(s):
    s = re.sub(r'[^a-zA-Z]',"",s)
    s = sorted(list(set(s)))
    return s,len(s)
