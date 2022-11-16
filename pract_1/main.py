import sys
from substitution import *
from affine import *
from affine_recurrent import *


def help():
    print("""
    Options:
    [+] -h || --help                    Display help
    [+] -t || --type                    Cipher type. Use the option number after this argument
        Available ciphers are:
            (1) Simple Substitution
            (2) Affine
            (3) Recurrent Affine
    [+] -s || --string                  String to decode/encode
    [+] -f || --file                    File from which the program reads contents
    [+] -e || --encode                  Use this flag to encode a string/file contents
    [+] -d || --decode                  Use this flag to decode a string/file contents
    [+] -o || --outfile                 Write the results of encryption/decryption to a file (specify relative or full path)
    """)


def check_args():
    if not ("-t" in sys.argv or "--type" in sys.argv):
        print("You must specify cipher type!")
        return -1
    if not ("-e" in sys.argv or "-d" in sys.argv or "--encode" in sys.argv or "--decode" in sys.argv):
        print("You must specify whether you want to decode or encode something!")
        return -1
    if not ("-f" in sys.argv or "--file" in sys.argv or "-s" in sys.argv or "--string" in sys.argv):
        print("You must specify a source string or source file!")
        return -1
    if not ("-f" in sys.argv or "--file" in sys.argv or "-s" in sys.argv or "--string" in sys.argv):
        print("You must specify source string or source file, not both!")
        return -1


def main():
    
    if check_args() == -1:
        print("Problems with args")
        return 0
    
    if "-t" in sys.argv:
        type_index = sys.argv.index("-t")
    elif "--type" in sys.argv:
        type_index = sys.argv.index("--type")
    type_cipher = sys.argv[type_index + 1]

    if "-e" in sys.argv or "--encode" in sys.argv:
        algo_cipher = "enc"
    elif "-d" in sys.argv or "--decode" in sys.argv:
        algo_cipher = "dec"
    
    if "-s" in sys.argv:
        source_string = sys.argv[sys.argv.index("-s") + 1]
    elif "--string" in sys.argv:
        source_string = sys.argv[sys.argv.index("--string") + 1]
    elif "-f" in sys.argv:
        source_string = sys.argv[sys.argv.index("-f") + 1]
    elif "--file" in sys.argv:
        source_string = sys.argv[sys.argv.index("--file") + 1]

    outfile = 0
    if "-o" in sys.argv:
        outfile = sys.argv[sys.argv.index("-o") + 1]
    elif "--outfile" in sys.argv:
        outfile = sys.argv[sys.argv.index("--outfile") + 1]
    
    if type_cipher == 1:
        substitution(algo=algo_cipher, outfile=outfile, source_string=source_string)
    elif type_cipher == 2:
        affine(algo=algo_cipher, outfile=outfile, source_string=source_string)
    elif type_cipher == 3:
        affine_recurrent(algo=algo_cipher, outfile=outfile, source_string=source_string)
    else:
        print("Incorrect cipher chosen")
        return 0
    
    return 0


if __name__ == "__main__":
    banner = """
    $$\       $$\                                                                     $$\               
    \__|      $$ |                                                                    $$ |              
    $$\       $$ |$$\   $$\ $$\    $$\        $$$$$$$\  $$$$$$\  $$\   $$\  $$$$$$\ $$$$$$\    $$$$$$\  
    $$ |      $$ |$$ |  $$ |\$$\  $$  |      $$  _____|$$  __$$\ $$ |  $$ |$$  __$$\\_$$  _|  $$  __$$\ 
    $$ |      $$ |$$ |  $$ | \$$\$$  /       $$ /      $$ |  \__|$$ |  $$ |$$ /  $$ | $$ |    $$ /  $$ |
    $$ |      $$ |$$ |  $$ |  \$$$  /        $$ |      $$ |      $$ |  $$ |$$ |  $$ | $$ |$$\ $$ |  $$ |
    $$ |      $$ |\$$$$$$  |   \$  /         \$$$$$$$\ $$ |      \$$$$$$$ |$$$$$$$  | \$$$$  |\$$$$$$  |
    \__|      \__| \______/     \_/           \_______|\__|       \____$$ |$$  ____/   \____/  \______/ 
                                                                $$\   $$ |$$ |                         
                                                                \$$$$$$  |$$ |                         
                                                                \______/ \__|                         
    """
    print(banner)
    help()
    main()
