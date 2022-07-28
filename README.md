# Jatin's Fake Blockchain

Contains competed code for the following: [funfirst.blog article](https://www.funfirst.blog/blockchain-without-the-hype/)

---

Make sure to download the required packages:

```
pip install rsa
```

---

Here is a rundown of all the files:

## `transactions.py`

Has the `Transaction` class and all logic for signing and verifying transactions. Also, includes the `BlockReward` class.

## `block.py`

Has the `Block` class which also implements logic for mining a block.

## `account.py`

Has logic for getting RSA public, private key pair and also a public address for each account.

## `chain_of_blocks.py`

Implements the core `Blockchain` class which combines other subclasses and is used to get the current balance of a public_address

## `main.py`

Optional file to highlight an example for the usage of the blockchain
