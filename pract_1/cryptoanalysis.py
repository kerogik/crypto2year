import json
import regex as re
from math import log10
import random as rnd

def cryptanalysis(outfile, infile_name):
    choice = int(input("You can choose which cipher to cryptanalyze:\n1. Substitution\n- "))
    if choice == 1:
        cryptanalysis_substitution(outfile, infile_name[0])
    return 0

def cryptanalysis_substitution(outfile, infile_name):
    
    with open(f"{infile_name}", 'r') as encrypted_fl:
        ciphertext = encrypted_fl.read().lower()
    #loading perfected values 
    NPERFECT = 389373
    with open('english_quadgrams.yml', 'r') as fl:
        perf_quadgrams = json.load(fl)
    base_alpha = [chr(i) for i in range(97, 123)]
    #
    total_iter_tries = int(input("Choose how many iterations you want to conduct\n- "))
    oldkey = [chr(i) for i in range(97, 123)]
    bestkey = oldkey
    bestscore = -99e9
    #starting to iterate with random first keys
    iter_num = 0
    while iter_num < total_iter_tries:
        iter_num += 1
        rnd.shuffle(oldkey)
        oldscore = score_text(ciphertext, perf_quadgrams, NPERFECT) 
        count = 0
        while count < 1000:
            rand_a = rnd.randint(0,25)
            rand_b = rnd.randint(0,25)
            newkey = [i for i in oldkey]
            newkey[rand_a], newkey[rand_b] = newkey[rand_b], newkey[rand_a]
            decrypted = try_decrypt(base_alpha, newkey, ciphertext)
            newscore = score_text(decrypted,perf_quadgrams, NPERFECT)
            if newscore > oldscore:
                oldscore = newscore
                oldkey = newkey
                count = 0
            count += 1
        if oldscore > bestscore:
            bestscore = oldscore
            bestkey = oldkey
            print(f"at iteration |||{iter_num}||| with key {''.join(oldkey)} the best key {''.join(bestkey)} scored {bestscore}")
            plaintext = try_decrypt(base_alpha, bestkey, ciphertext)
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(plaintext)
    else:
        print(plaintext)

    return 0

def score_text(source_string, perf_quadgrams, NPERFECT):
    
    clean_string = re.sub(r'[^a-z]','',source_string)
    quadgrams = []
    for i in range(len(clean_string)-3):
        quadgrams.append(clean_string[i:i+4].upper())
    
    score_text = 0
    for i in range(len(quadgrams)):
        if quadgrams[i] in perf_quadgrams:
            score_text += log10(float(perf_quadgrams[quadgrams[i]])/NPERFECT)
        else:
            score_text += log10(0.01/NPERFECT)
    return score_text


def try_decrypt(alphabet, key, source_string):
    key_dict = dict(zip(alphabet, key))
    out_string = ''.join([source_string[i] if not source_string[i] in key_dict else key_dict[source_string[i]] for i in range(len(source_string))])
    return out_string
