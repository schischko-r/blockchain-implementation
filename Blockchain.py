from Block import Block
from Wallet import Wallet
from Interface import InterfaceHandler
from ellipticcurve.ecdsa import Ecdsa
import json


class Blockchain:

    _chain: list
    # _DIFFICULTY  is the number of zeros at the beginning of the hash
    _DIFFICULTY = 3
    _BRAIN_CELLS_COST = 1E-6
    _TRANSACTION_COST = 1E-2

    def __init__(self, users) -> None:
        # Create genesis block
        self.chain = [Block()]
        self.chain[0].mine(self._DIFFICULTY)
        # Create wallets
        self.wallets = [Wallet(public_name=user[0], blockchain=self)
                        for user in users]
        self.interface = InterfaceHandler()
        # Giving money to all users
        for i in range(len(self.wallets)):
            self.add_block(sender_wallet=Wallet(public_name="God", blockchain=self),
                           recipient_wallet=self.wallets[i], value=150)

    def get_last_block(self) -> Block:
        # Get last block in the blockchain
        return self.chain[-1]

    def add_block(self, sender_wallet=None, recipient_wallet=None, value=100, commission=False) -> None:
        # Add block to the blockchain

        if recipient_wallet is None and not commission:
            # If the recipient is not specified
            InterfaceHandler.Error("You must specify the recipient")
            return None
        if not commission:
            if sender_wallet.public_key == recipient_wallet.public_key:
                # If the sender and the recipient are the same
                InterfaceHandler.Error("You can't send money to yourself")
                return None

        # Create block and add it to the blockchain
        block = Block(self.get_last_block(),
                      sender_wallet=sender_wallet, recipient_wallet=recipient_wallet, v=value)

        if Ecdsa.verify(block.get_hash(),
                        block.get_signature_object(), sender_wallet.public_key):
            block.sign()
            block.mine(self._DIFFICULTY)
            if not commission:
                block.set_brain_cells(
                    block.get_nonce() * self._BRAIN_CELLS_COST)

                block.set_transacttion_cost(self._TRANSACTION_COST *
                                            block.get_value() + block.get_brain_cells())
            self.chain.append(block)

        else:
            pass

    def get_chain(self) -> list:
        # Get blockchain
        return self.chain

    def print_blockchain_info(self):
        # Print blockchain data to console
        for block in self.chain:
            block.get_block_info()
        return None

    def write_to_json(self):
        # Write blockchain data to json file

        with open('blockchain.json', 'w') as f:
            json.dump(self.chain, f, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)
        return None

    def read_from_json(self):
        # Read blockchain data from json file

        with open('blockchain.json', 'r') as f:
            self.chain = json.load(f, object_hook=lambda d: Block(**d))
        return None
