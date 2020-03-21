from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import base64
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding


def hashMessage(msg):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(msg)
    return digest.finalize()   
    

def generatePasswordsKeyPairsCertificates():
    

    #CA KeyPair generate

    CA_KeyPair = generateKeyPair() 
    CA_PublicKey = CA_KeyPair.public_key()
    saveKeyPair("./KeyPairs/CA_KeyPair",CA_KeyPair)
    savePublicKey("./KeyPairs/CA_PublicKey",CA_PublicKey)
    #ChatServer generate

    ChatServerKeyPair = generateKeyPair()
    saveKeyPair("./KeyPairs/ChatServer_KeyPair",ChatServerKeyPair)
    ChatServerPublicKey = getPublicKey(ChatServerKeyPair)
    ChatServerCertificate = generateCertificate(ChatServerPublicKey,CA_KeyPair)
    saveCertificate("./Certificates/ChatServer_Certificate",ChatServerCertificate)

    savePublicKey("./Certificates/CA_PublicKey",ChatServerPublicKey)
    readCertificate("./Certificates/ChatServer_Certificate")

    NumberOfClient = int(input("Enter number of Clients :"))

    for i in range (NumberOfClient):
        userName = input("Enter Client Name : ")
        password = input("Enter Client Password :")
        HashPassword = hashMessage(bytes(password,"utf8"))
        file = open("./Passwords/"+userName+"_Password","wb") 
        file.write(HashPassword)
        file.close()

        clientKeyPair = generateKeyPair()
        saveKeyPair("./KeyPairs/"+userName+"_KeyPair",clientKeyPair)
        ClientPublicKey = getPublicKey(clientKeyPair)
        ClientCertificate = generateCertificate(ClientPublicKey,CA_KeyPair)
        saveCertificate("./Certificates/"+userName+"_Certificate",ClientCertificate)
        

def generateKeyPair():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

def getPublicKey(keyPair):
    
    return keyPair.public_key()


def savePublicKey(path,pubKey):
    # Write our key to disk for safe keeping
    with open(path, "wb") as f:
        f.write(pubKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,))


def saveKeyPair(path,keyPair):
    with open(path, "wb") as f:
        f.write(keyPair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),))
   
def getKeyPairFromFile(path):
    with open(path) as key_file:
        return serialization.load_pem_private_key(
        key_file.read().encode(),
        password=b"passphrase",
        backend=default_backend()
    )

def getPublicKeyFromFile(path):
    with open(path) as key_file:
        return load_pem_public_key(key_file.read().encode(), backend=default_backend())

def generateCertificate(PubKey,CAPrivateKey):
    # Various details about who we are. For a self-signed certificate the
    # subject and issuer are always the same.
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"TR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Ankara"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Cankaya"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"TOBB"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    return x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        PubKey #Client Public Key
    ).serial_number(
        2
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    # Sign our certificate with our private key
    ).sign(CAPrivateKey, hashes.SHA256(), default_backend())
    # Write our certificate out to disk.

def saveCertificate(path,certificate):
    with open(path, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

def readCertificate(path):
    with open(path, "r") as f:
        pem_data = f.read()
        cert = x509.load_pem_x509_certificate(pem_data.encode(), default_backend())

def verifyCertificate(CA_PublicKey,certificate):
    try:
        CA_PublicKey.verify(
             certificate.signature,
             certificate.tbs_certificate_bytes,
             # Depends on the algorithm used to create the certificate
             padding.PKCS1v15(),
             certificate.signature_hash_algorithm,
        )
        return
    except expression as identifier:
        return False
        
        

generatePasswordsKeyPairsCertificates()




