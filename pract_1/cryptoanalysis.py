import json
import regex as re
from math import log10
import random as rnd
import math

def cryptanalysis(outfile, infile_name):
    choice = int(input("You can choose which cipher to cryptanalyze:\n1. Substitution\n2. Affine cipher\n3. Affine recurrent cipher\n- "))
    if choice == 1:
        cryptanalysis_substitution(outfile, infile_name[0])
    elif choice == 2:
        cryptanalysis_affine(outfile, infile_name[0])
    elif choice == 3:
        cryptanalysis_affine_recur(outfile, infile_name[0])
    else:
        print("Wrong choice. Aborting.")
    return 0


def cryptanalysis_substitution(outfile, infile_name):
    
    with open(f"{infile_name}", 'r') as encrypted_fl:
        ciphertext = encrypted_fl.read().lower()
    #loading perfected values 
    n_gram = int(input("Choose which n-gram to use when decrypting\n1 - monograms\n2 - bigrams\n3 - trigrams\n4 - quadgrams\n- "))
    if n_gram == 1:
        NPERFECT = 4916299
        ngrams_file_name = "my_monograms.yml"
    elif n_gram == 2:
        NPERFECT = 4916301
        ngrams_file_name = "my_bigrams.yml"
    elif n_gram == 3:
        NPERFECT = 4916300
        ngrams_file_name = "my_trigrams.yml"
    elif n_gram == 4:
        NPERFECT = 4916299
        ngrams_file_name = "my_quadgrams.yml"
    else:
        print("Sth went wrong. Aborting.")
        return 0
    with open(ngrams_file_name, 'r') as fl:
        perf_ngrams = json.load(fl)
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
        oldscore = score_text(ciphertext, perf_ngrams, NPERFECT, n_gram) 
        count = 0
        while count < 1000:
            rand_a = rnd.randint(0,25)
            rand_b = rnd.randint(0,25)
            newkey = [i for i in oldkey]
            newkey[rand_a], newkey[rand_b] = newkey[rand_b], newkey[rand_a]
            decrypted = try_decrypt_substitution(base_alpha, newkey, ciphertext)
            newscore = score_text(decrypted,perf_ngrams, NPERFECT, n_gram)
            if newscore > oldscore:
                oldscore = newscore
                oldkey = newkey
                count = 0
            count += 1
        if oldscore > bestscore:
            bestscore = oldscore
            bestkey = oldkey
            print(f"at iteration |||{iter_num}||| with key {''.join(oldkey)} the best key {''.join(bestkey)} scored {bestscore}")
            plaintext = try_decrypt_substitution(base_alpha, bestkey, ciphertext)
    
    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(plaintext)
    else:
        print(plaintext)

    return 0


def cryptanalysis_affine(outfile, infile_name):
    
    with open(f"{infile_name}", 'r') as encrypted_fl:
        ciphertext = encrypted_fl.read().lower()
    #loading perfected values 
    n_gram = int(input("Choose which n-gram to use when decrypting\n1 - monograms\n2 - bigrams\n3 - trigrams\n4 - quadgrams\n- "))
    if n_gram == 1:
        NPERFECT = 4916299
        ngrams_file_name = "my_monograms.yml"
    elif n_gram == 2:
        NPERFECT = 4916301
        ngrams_file_name = "my_bigrams.yml"
    elif n_gram == 3:
        NPERFECT = 4916300
        ngrams_file_name = "my_trigrams.yml"
    elif n_gram == 4:
        NPERFECT = 4916299
        ngrams_file_name = "my_quadgrams.yml"
    else:
        print("Sth went wrong. Aborting.")
        return 0
    with open(ngrams_file_name, 'r') as fl:
        perf_ngrams = json.load(fl)
    
    ZM_RING = 26
    alpha_revs = [(rev_broad_euclidean(ZM_RING, i) + 26) % 26 for i in range(ZM_RING) if is_coprime(i, ZM_RING)]
    print(alpha_revs)
    betas = [i for i in range(ZM_RING)]

    best_score = -99e9
    best_keypair = (0,0)

    for alpha_rev in alpha_revs:
        for beta in betas:
            cur_keypair = (alpha_rev, beta)
            decrypted = try_decrypt_affine(cur_keypair, ciphertext, ZM_RING)
            cur_score = score_text(decrypted, perf_ngrams, NPERFECT, n_gram)
            if cur_score > best_score:
                best_score = cur_score
                best_keypair = (alpha_rev, beta)
                print(f"Current best pair of keys is {(rev_broad_euclidean(ZM_RING, best_keypair[0]) + 26) % 26},{best_keypair[1]}, resulting in score {best_score}\n")
    
    plaintext = try_decrypt_affine(best_keypair,ciphertext, ZM_RING)

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(plaintext)
    else:
        print(plaintext)

    return 0


def cryptanalysis_affine_recur(outfile, infile_name):
    
    with open(f"{infile_name}", 'r') as encrypted_fl:
        ciphertext = encrypted_fl.read().lower()
    #loading perfected values 
    n_gram = int(input("Choose which n-gram to use when decrypting\n1 - monograms\n2 - bigrams\n3 - trigrams\n4 - quadgrams\n- "))
    if n_gram == 1:
        NPERFECT = 4916299
        ngrams_file_name = "my_monograms.yml"
    elif n_gram == 2:
        NPERFECT = 4916301
        ngrams_file_name = "my_bigrams.yml"
    elif n_gram == 3:
        NPERFECT = 4916300
        ngrams_file_name = "my_trigrams.yml"
    elif n_gram == 4:
        NPERFECT = 4916299
        ngrams_file_name = "my_quadgrams.yml"
    else:
        print("Sth went wrong. Aborting.")
        return 0
    with open(ngrams_file_name, 'r') as fl:
        perf_ngrams = json.load(fl)
    
    ZM_RING = 26
    alpha_revs = [(rev_broad_euclidean(ZM_RING, i) + 26) % 26 for i in range(ZM_RING) if is_coprime(i, ZM_RING)]
    betas = [i for i in range(ZM_RING)]

    best_score = -99e9
    best_keypair = ((0,0),(0,0))

    
    for alpha_1 in alpha_revs:
        try:
            for beta_1 in betas:
                for alpha_2 in alpha_revs:
                    for beta_2 in betas:
                        cur_keypair = ((alpha_1, beta_1),(alpha_2, beta_2))
                        decrypted = try_decrypt_affine_recur(cur_keypair, ciphertext, ZM_RING)
                        cur_score = score_text(decrypted, perf_ngrams, NPERFECT, n_gram)
                        
                        if cur_score > best_score:
                            best_score = cur_score
                            best_keypair = ((alpha_1, beta_1),(alpha_2, beta_2))
                            print(f"Current best pair of keys is {(rev_broad_euclidean(ZM_RING, best_keypair[0][0]) + 26) % 26, best_keypair[0][1]},{(rev_broad_euclidean(ZM_RING, best_keypair[1][0]) + 26) % 26, best_keypair[1][1]}, resulting in score {best_score}\n[Press Ctrl+C if you wish to try and see the corresponding results, or wait until all keys are tried]\n")
        except:
            print("Stopping the iterations...\n")
            break                
    
    plaintext = try_decrypt_affine_recur(best_keypair,ciphertext, ZM_RING)

    if outfile != 0:
        with open(outfile, 'w') as outfile:
            outfile.write(plaintext)
    else:
        print(plaintext)

    return 0


def score_text(source_string, perf_ngrams, NPERFECT, n_gram):
    
    clean_string = re.sub(r'[^a-z]','',source_string)
    ngrams = []
    for i in range(len(clean_string)- n_gram + 1):
        ngrams.append(clean_string[i:i+n_gram])
    
    score_text = 0
    for i in range(len(ngrams)):
        if ngrams[i] in perf_ngrams:
            score_text += log10(float(perf_ngrams[ngrams[i]])/NPERFECT)
        else:
            score_text += log10(0.01/NPERFECT)
    return score_text / n_gram


def try_decrypt_substitution(alphabet, key, source_string):
    key_dict = dict(zip(alphabet, key))
    out_string = ''.join([source_string[i] if not source_string[i] in key_dict else key_dict[source_string[i]] for i in range(len(source_string))])
    return out_string


def try_decrypt_affine(keypair, ciphertext, ZM_RING):
    alpha_rev = keypair[0]
    beta = keypair[1]
    out_string = ''
    for i in range(len(ciphertext)):
        if not re.match(r'[a-zA-Z]', ciphertext[i]):
            out_string += ciphertext[i]
        else:
            new_letter = chr((ord(ciphertext[i]) - 97 - beta)*alpha_rev % ZM_RING + 97)
            out_string += new_letter
    return out_string


def try_decrypt_affine_recur(keypairs, ciphertext, ZM_RING):
    alpha_1 = keypairs[0][0]
    beta_1 = keypairs[0][1]
    alpha_2 = keypairs[1][0]
    beta_2 = keypairs[1][1]

    decoded_letters= ''
    clean_string = re.sub(r'[^a-zA-Z]',"",ciphertext)
    rev_alpha_1 = alpha_1
    decoded_letters += chr((ord(clean_string[0]) - 97 - beta_1)*rev_alpha_1 % ZM_RING + 97)
    rev_alpha_2 = alpha_2
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
    for i in range(len(ciphertext)):
        if not re.match(r'[a-zA-Z]', ciphertext[i]):
            out_string += ciphertext[i]
            count_non_alpha +=1
        else:
            out_string += decoded_letters[i-count_non_alpha]
    return out_string


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