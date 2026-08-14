import hashlib

hashes = {
    "admin": "2365bfe9e7e5331dd2daf29d50bb0903",
    "dev": "18a7763dbf76f40177acbfda65e84214"
}

wordlist = [
    "admin",
    "password",
    "123456",
    "admin123",
    "dev",
    "letmein",
    "qwerty",
    "welcome",
    "test",
    "password123"
]

for user, target in hashes.items():
    for word in wordlist:
        h = hashlib.md5(word.encode()).hexdigest()
        if h == target:
            print(f"{user} password =", word)