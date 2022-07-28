import rsa
from hashlib import sha256
import json
from datetime import datetime

class Transaction:
    def __init__(self, from_account, to_account, amount):
        # create initial data object and store time
        self.data = {"from": from_account, "to": to_account, "amount": amount}
        self.time = str(int(datetime.utcnow().timestamp()))
        self.signature = None # signature remains None until it is signed
    
    def sign_transaction(self, privateKey):
        # we need to add the time to the transaction object
        txn_object = self.data
        txn_object["time"] = self.time
        txn_string = json.dumps(txn_object, sort_keys=True) # convert object into string (easier to get bytes)
        raw_hash_hex = sha256(txn_string.encode()).hexdigest() # hash the object string
        padded_hex = f"{int(raw_hash_hex, 16):#0{66}x}"
        shortened_hex = padded_hex[:34] # shorten the hash since its too much data
        # use RSA sign and indicate that data was hashed using SHA-256
        raw_signature = rsa.sign(bytes(shortened_hex.encode()), privateKey, "SHA-256").hex()
        clean_signature = f"{int(raw_signature, 16):#0{130}x}" # pad the hex string to 130 ('0x' + 128 hex characters)
        self.signature = clean_signature
    
    def verify_transaction(self, publicKey):
        try:
            # repreat the same process for getting message as used in signing
            txn_object = self.data
            txn_object["time"] = self.time
            txn_string = json.dumps(txn_object, sort_keys=True)
            raw_hash_hex = sha256(txn_string.encode()).hexdigest()
            padded_hex = f"{int(raw_hash_hex, 16):#0{66}x}"
            shortened_hex = padded_hex[:34]
            # use in-built RSA verify method on the message/signature
            rsa.verify(bytes(shortened_hex.encode()), bytes.fromhex(self.signature[2:]), publicKey)
            # the function raises an exception if the publicKey doesnt match
            # if no exception, return True
            return True
        except:
            # if exception is raised by rsa.verify(), we return False
            return False
        
class BlockReward:
    def __init__(self, to_account, amount):
        self.data = {"to": to_account, "amount": amount} # there is no 'from' since the reward is from the network itself
        # there is also no "signature" since there is no sender