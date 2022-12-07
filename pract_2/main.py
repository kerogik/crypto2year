import sys
from aes import *

def help():
    print("""
    Options:
    [+] -h  || --help                    Display help 
    [+] -s  || --string                  String to decode/encode
    [+] -f  || --file                    File from which the program reads contents
    [+] -ks || --keystring               Key (password) used to decode/encode
    [+] -kf || --keyfile                 File from which the program reads key (password)
    [+] -e  || --encode                  Use this flag to encode a string/file contents
    [+] -d  || --decode                  Use this flag to decode a string/file contents
    [+] -o  || --outfile                 Write the results of encryption/decryption to a file (specify relative or full path)
    """)


def check_args():
    if not ("-ks" in sys.argv or "--keystring" in sys.argv or "-kf" in sys.argv or "--keyfile" in sys.argv):
        print("You need to specify a keyfile or the key itself!")
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
    
    if "-h" in sys.argv or "--help" in sys.argv:
        help()
        return 0

    if "-e" in sys.argv or "--encode" in sys.argv:
        algo_cipher = "enc"
    elif "-d" in sys.argv or "--decode" in sys.argv:
        algo_cipher = "dec"
    
    if "-s" in sys.argv:
        source_string = [sys.argv[sys.argv.index("-s") + 1], 1]
    elif "--string" in sys.argv:
        source_string = [sys.argv[sys.argv.index("--string") + 1], 1]
    elif "-f" in sys.argv:
        source_string = [sys.argv[sys.argv.index("-f") + 1], 0]
    elif "--file" in sys.argv:
        source_string = [sys.argv[sys.argv.index("--file") + 1], 0]

    if "-ks" in sys.argv:
        key_string = [sys.argv[sys.argv.index("-ks") + 1], 1]
    elif "--keystring" in sys.argv:
        key_string = [sys.argv[sys.argv.index("--keystring") + 1], 1]
    elif "-kf" in sys.argv:
        key_string = [sys.argv[sys.argv.index("-kf") + 1], 0]
    elif "--keyfile" in sys.argv:
        key_string = [sys.argv[sys.argv.index("--keyfile") + 1], 0]

    outfile = 0
    if "-o" in sys.argv:
        outfile = sys.argv[sys.argv.index("-o") + 1]
    elif "--outfile" in sys.argv:
        outfile = sys.argv[sys.argv.index("--outfile") + 1]
    
    aes(algo=algo_cipher, outfile=outfile, source_string=source_string, key_string=key_string)
    
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
    main()
