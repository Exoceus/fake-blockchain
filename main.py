from account import create_account
from chain_of_blocks import Blockchain
from transactions import Transaction

blockchain = Blockchain()

public_address1, rsaPublicKey1, rsaPrivateKey1 = create_account()
public_address2, rsaPublicKey2, rsaPrivateKey2 = create_account()

# A hacky way to get some balance to start off with
transaction1 = Transaction(public_address1, public_address2, "0")
transaction2 = Transaction(public_address1, public_address2, "0")

transaction1.sign_transaction(rsaPrivateKey1)
transaction2.sign_transaction(rsaPrivateKey1)

blockchain.emit_new_transaction(transaction1)
blockchain.emit_new_transaction(transaction2)
blockchain.new_block(public_address1)

print("Balance of", public_address1, blockchain.get_current_balance(public_address1))
print("Balance of", public_address2, blockchain.get_current_balance(public_address2))

# Do some acctual transfers

transaction3 = Transaction(public_address1, public_address2, "1")
transaction4 = Transaction(public_address1, public_address2, "3")

transaction3.sign_transaction(rsaPrivateKey1)
transaction4.sign_transaction(rsaPrivateKey1)

blockchain.emit_new_transaction(transaction3)
blockchain.emit_new_transaction(transaction4)
blockchain.new_block(public_address2)

print("Balance of", public_address1, blockchain.get_current_balance(public_address1))
print("Balance of", public_address2, blockchain.get_current_balance(public_address2))