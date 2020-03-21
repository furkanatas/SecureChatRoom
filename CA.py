from Crypto.Hash import SHA512
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes



def hashMessage(msg):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(msg)
    return digest.finalize()
    

def generatePasswordsFile():
    NumberOfClient = int(input("Enter How many Client : "))

    for i in range (NumberOfClient):
        userName = input("Enter Client Name : ")
        password = input("Enter Client Password :")
        HashPassword = hashMessage(bytes(password,"utf8"))
        file = open(userName+".txt","w") 
        file.write(userName +" " + HashPassword)
        file.close()

def generateCertificate():    
    # Generate CA key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Write our key to disk for safe keeping
    with open("path/to/store/key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))


generatePasswordsFile()
