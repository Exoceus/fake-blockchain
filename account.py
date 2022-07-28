import rsa

def create_account():
    rsaPublicKey, rsaPrivateKey = rsa.newkeys(512)
    public_address = hex(rsaPublicKey.n)
    return public_address, rsaPublicKey, rsaPrivateKey