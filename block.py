from hashlib import sha256
from datetime import datetime
import json
from transactions import BlockReward

def create_block_hash(transactions, previous_hash, timestamp, nonce):
    transaction_strings = []
    for transaction in transactions:
        transaction_strings += json.dumps(transaction.__dict__, sort_keys=True).encode('utf-8')
    raw_hash_hex = sha256(bytes(previous_hash.encode('utf-8')) + bytes(nonce) + bytes(transaction_strings) +  bytes(timestamp.encode('utf-8'))).hexdigest()
    decimal_hash = int(raw_hash_hex, 16)
    padded_hex = f"{decimal_hash:#0{66}x}"
    return padded_hex

def calculate_nonce(transactions, previous_hash, timestamp):
    nonce = 0
    block_hash = create_block_hash(transactions, previous_hash, timestamp, nonce)
    while(block_hash[2:6] != "0000"):
        nonce += 1
        block_hash = create_block_hash(transactions, previous_hash, timestamp, nonce)
    return nonce


class Block:
    def __init__(self, previous_block_hash, transactions):
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.timestamp = str(int(datetime.utcnow().timestamp()))
    
    def mine_block(self,miner_public_address):
        self.transactions = [BlockReward(miner_public_address, "10")] + self.transactions
        self.nonce = calculate_nonce(self.transactions, self.previous_block_hash, self.timestamp)
        self.block_hash = create_block_hash(self.transactions, self.previous_block_hash, self.timestamp, self.nonce)