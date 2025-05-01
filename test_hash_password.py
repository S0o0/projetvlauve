import hashlib

mdp = "1234"
salt = "beb7d85faece5b68657a0b222ffe731a"
hash_attendu = hashlib.sha256((mdp + salt).encode()).hexdigest()
print(hash_attendu)