from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, hmac

def loadPrivateKeyPair(path):
    with open( path, "rb") as key_file: 
        return serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend() )

def generateRandomKey():
    return Fernet.generate_key()

def encryptWithSymKey(key,message):
    f = Fernet(key)
    return f.encrypt(message)

def decryptWithSymKey(key,ciphertext):
    f = Fernet(key)
    return f.decrypt(ciphertext)

def hashMessage(msg):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(msg)
    return digest.finalize()    

def getPublicKeyFromkeyPair(keyPair):
    return  keyPair.public_key()

def generateRSAKeyPair():
    return rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())

def getMACofMessage(message):
    h = hmac.HMAC(base64.urlsafe_b64encode(b'MACkey'), hashes.SHA256(), backend=default_backend())
    h.update(message)
    return h.finalize()

def encryptWithRSA_PublicKey(pubKey,msg):
    return pubKey.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decryptWithRSA_PrivateKey(keyPair,ciphertext):
    return keyPair.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )      


def signWithRSA_PrivateKey(keyPair,msg):
    return private_key.sign(
     msg,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
 )


def verifyWithRSA_PublicKey(pubKey,signature):
    return pubKey.verify(
    signature,
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )



