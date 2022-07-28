from hashlib import sha256
from datetime import datetime
import json
from transactions import BlockReward

def create_block_hash(transactions, previous_hash, timestamp, nonce):
    # we want to convert json object into bytes
    transaction_strings = [] # we start with empty array
    for transaction in transactions:
        # then we convert json object to string and get its bytes
        transaction_strings += json.dumps(transaction.__dict__, sort_keys=True).encode('utf-8')
    # add up all the bytes and then get the SHA-256 hash
    raw_hash_hex = sha256(bytes(previous_hash.encode('utf-8')) + bytes(nonce) + bytes(transaction_strings) +  bytes(timestamp.encode('utf-8'))).hexdigest()
    # just get the hex number and convert to int and then convert it back to hex string with padding to make the string always have length of 66
    # this means '0x' + 64 hex characters
    decimal_hash = int(raw_hash_hex, 16)
    padded_hex = f"{decimal_hash:#0{66}x}"
    return padded_hex

def calculate_nonce(transactions, previous_hash, timestamp):
    nonce = 0 # start off with 0 since we only want positive integers
    block_hash = create_block_hash(transactions, previous_hash, timestamp, nonce)
    # at every nonce value, check if the hash begins with 4 zeroes
    while(block_hash[2:6] != "0000"):
        nonce += 1
        block_hash = create_block_hash(transactions, previous_hash, timestamp, nonce) # calculate new hash
    return nonce


class Block:
    def __init__(self, previous_block_hash, transactions):
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.timestamp = str(int(datetime.utcnow().timestamp())) # get current UTC datetime and convert it into string int
    
    # calculates the blockhash by using helper functions
    def mine_block(self,miner_public_address):
        # add BlockReward as first "transaction"
        self.transactions = [BlockReward(miner_public_address, "10")] + self.transactions
        self.nonce = calculate_nonce(self.transactions, self.previous_block_hash, self.timestamp)
        self.block_hash = create_block_hash(self.transactions, self.previous_block_hash, self.timestamp, self.nonce)