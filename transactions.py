import rsa
from hashlib import sha256
import json
from datetime import datetime

class Transaction:
    def __init__(self, from_account, to_account, amount):
        self.data = {"from": from_account, "to": to_account, "amount": amount}
        self.time = str(int(datetime.utcnow().timestamp()))
        self.signature = None
    
    def sign_transaction(self, privateKey):
        txn_object = self.data
        txn_object["time"] = self.time
        txn_string = json.dumps(txn_object, sort_keys=True)
        raw_hash_hex = sha256(txn_string.encode()).hexdigest()
        padded_hex = f"{int(raw_hash_hex, 16):#0{66}x}"
        shortened_hex = padded_hex[:34] # shorten the hash since its too much data
        raw_signature = rsa.sign(bytes(shortened_hex.encode()), privateKey, "SHA-256").hex()
        clean_signature = f"{int(raw_signature, 16):#0{130}x}"
        self.signature = clean_signature
    
    def verify_transaction(self, publicKey):
        try:
            txn_object = self.data
            txn_object["time"] = self.time
            txn_string = json.dumps(txn_object, sort_keys=True)
            raw_hash_hex = sha256(txn_string.encode()).hexdigest()
            padded_hex = f"{int(raw_hash_hex, 16):#0{66}x}"
            shortened_hex = padded_hex[:34]
            rsa.verify(bytes(shortened_hex.encode()), bytes.fromhex(self.signature[2:]), publicKey)
            return True
        except:
            return False
        
class BlockReward:
    def __init__(self, to_account, amount):
        self.data = {"to": to_account, "amount": amount}