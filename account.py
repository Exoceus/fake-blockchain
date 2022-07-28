import rsa

def create_account():
    rsaPublicKey, rsaPrivateKey = rsa.newkeys(512) # get random RSA key pair
    public_address = hex(rsaPublicKey.n) # convert public key to hex string
    return public_address, rsaPublicKey, rsaPrivateKey