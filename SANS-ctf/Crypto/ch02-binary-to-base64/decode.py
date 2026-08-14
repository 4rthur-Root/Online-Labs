import base64
import re

def binary_to_text():
    chemin = "code.txt"
    with open(chemin, "r") as c:
        contenu = c.read().strip()
        liste_bits = contenu.split()
    decoded_chars = [chr(int(b, 2)) for b in liste_bits]
    ascii_message = "".join(decoded_chars)
    return ascii_message

def clean_base64(s):
    # Supprimer tous les '=' (ils seront remis correctement à la fin)
    s = s.replace('=', '')
    # Supprimer tout caractère non valide (normalement il n'y en a pas)
    s = re.sub(r'[^A-Za-z0-9+/]', '', s)
    # Ajouter le padding nécessaire pour que la longueur soit multiple de 4
    while len(s) % 4 != 0:
        s += '='
    return s

if __name__ == "__main__":
    message = binary_to_text()
    print("Message ASCII brut :", message)

    try:
        clean_msg = clean_base64(message)
        print("Message corrigé :", clean_msg)
        message_final = base64.b64decode(clean_msg).decode("utf-8", errors="ignore")
        print("Message final décodé :", message_final)
    except Exception as e:
        print("Impossible de décoder en Base64 :", e)
        
