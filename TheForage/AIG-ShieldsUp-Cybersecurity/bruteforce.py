'''
Forage AIG Cybersecurity Program
Bruteforce starter template
'''

from zipfile import ZipFile

# Use a method to attempt to extract the zip file with a given password
def attempt_extract(zf, password):

    # Open the zip file in read mode
    try :
        
        zf.extractall(pwd=password)
        return True
        
         
    except RuntimeError:
        zf.close()
        
        return False
          

     
#
#

def main():
    print("[+] Beginning bruteforce ")

    with ZipFile('enc.zip') as zf:
        with open('rockyou.txt', 'rb') as f:
            for line in f:
                # Iterate through password entries in rockyou.txt
                password = line.strip()
             
            # Attempt to extract the zip file using each password
                if attempt_extract(zf, password):
                    print(f"Extraction successful for the password {password}")
                    break

                else:
                    print(f"Extraction failed for the password {password}")
                    # reopen after failed attempt since extractall may have
                    # left the file in a bad state
                    zf = ZipFile('enc.zip', 'r')


    

if __name__ == "__main__":
    main()