from block import Block

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.pending_transactions = []
    
    def get_current_balance(self, public_address):
        balance = 0
        for block in self.blocks:
            for transaction in block.transactions:
                txn_data = transaction.data
                if 'to' in txn_data and public_address == txn_data['to']:
                    balance += int(txn_data['amount'])
                elif 'from' in txn_data and public_address == txn_data['from']:
                    balance -= int(txn_data['amount'])
        return balance
    
    def emit_new_transaction(self, transaction):
        current_balance = self.get_current_balance(transaction.__dict__['data']['from'])
        if int(transaction.__dict__['data']['amount']) > current_balance:
            raise Exception("Not enough balance to make transaction")
        if len(self.pending_transactions) >= 2:
            raise Exception("Too many transactions for one block. Block limit is 2 so please mine a block before ")
        self.pending_transactions.append(transaction)
    
    def new_block(self, miner_public_address):
        if len(self.blocks) == 0:
            previous_block_hash = f"{0:#0{66}x}"
        else:
            previous_block_hash = self.blocks[-1].block_hash
        new_block = Block(previous_block_hash, self.pending_transactions)
        new_block.mine_block(miner_public_address)
        self.blocks.append(new_block)
        self.pending_transactions = []
