from block import Block

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.pending_transactions = []
    
    def get_current_balance(self, public_address):
        # set initial balance at 0 since it is the default balance
        balance = 0
        # iterate through each transaction in each block
        for block in self.blocks:
            for transaction in block.transactions:
                txn_data = transaction.data
                # if public address is 'to', then we increment the amount
                if 'to' in txn_data and public_address == txn_data['to']:
                    balance += int(txn_data['amount'])
                # if public address is in 'from', then we decrement the amount
                elif 'from' in txn_data and public_address == txn_data['from']:
                    balance -= int(txn_data['amount'])
        return balance
    
    def emit_new_transaction(self, transaction):
        # first we check if the sender has enough balance to make the transactions
        current_balance = self.get_current_balance(transaction.__dict__['data']['from'])
        if int(transaction.__dict__['data']['amount']) > current_balance:
            raise Exception("Not enough balance to make transaction")
        # We max out the amount of pending transactions at 2
        if len(self.pending_transactions) >= 2:
            raise Exception("Too many transactions for one block. Block limit is 2 so please mine a block before ")
        # if all checks pass, we add the transaction to pending transaction list
        self.pending_transactions.append(transaction)
    
    def new_block(self, miner_public_address):
        # if this is the first block, we let previous has be just 0x000...00
        if len(self.blocks) == 0:
            previous_block_hash = f"{0:#0{66}x}"
        else:
            previous_block_hash = self.blocks[-1].block_hash
        # create new block and mine it
        new_block = Block(previous_block_hash, self.pending_transactions)
        new_block.mine_block(miner_public_address)
        # once it is mined, we add the block to the list of confirmed blocks and clear out pending transactions
        self.blocks.append(new_block)
        self.pending_transactions = []
