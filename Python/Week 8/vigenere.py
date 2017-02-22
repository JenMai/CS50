#-----------------------------
# Ciphers a text according to a key (Vigenere)
#-----------------------------

import cs50
import sys

def main():
    #-----------------------------
    # Ensures proper usage.
    #-----------------------------
    
    if (len(sys.argv) > 2) or (len(sys.argv) == 1):
        print("Usage: ./vigenere k")
        return 1
    
    k = sys.argv[1]
    
    if k.isalpha() == False:
        print("Usage: ./vigenere k")
        return 2

    k = k.lower()                                       # all lower cases to make the process easier
    
    #-----------------------------
    # Prompts user for a plaintext.
    #-----------------------------
        
    print("plaintext: ", end="")
    p = cs50.get_string()
    print("ciphertext: ", end="")
    
    #-----------------------------
    # Cipher one character at a time per Vigenere's rules.
    #-----------------------------
    j = 0                                               # char index in key
    A = ord("A")
    a = ord("a")
    
    for i in p:
        if i.isalpha():                                 # only process when alpha char
            if i.isupper():
                i = ((ord(i)-A) + (ord(k[j])-a)) % 26   # convert to Unicode and alphabetical value
                i = chr(i + A)                          # back to char
                print("{}".format(i), end="")
                j += 1
            
            elif i.islower():
                i = ((ord(i)-a) + (ord(k[j])-a)) % 26 
                i = chr(i + a)
                print("{}".format(i), end="")
                j += 1 
                
            if j % len(k) == 0:                         # reset index if key is shorter than plaintext
                j = 0
        
        else:
            print("{}".format(i), end="")
            
    print()

if __name__ == "__main__" :
    main()