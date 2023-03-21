from Block import Block
from Wallet import Wallet
from Interface import InterfaceHandler
from ellipticcurve.ecdsa import Ecdsa
import json

from ECDSA import ecdsa
from ECDSA import elliptic_curves as ec


class Blockchain:

    _chain: list
    # _DIFFICULTY  is the number of zeros at the beginning of the hash
    _DIFFICULTY = 3
    _BRAIN_CELLS_COST = 1E-5
    _TRANSACTION_COST = 1E-2

    _P = 233970423115425145524320034830162017933
    _G = ec.ECPoint(182, 85518893674295321206118380980485522083)
    _N = 29246302889428143187362802287225875743
    _curve = ec.EllipticCurve(-95051, 11279326, _P)
    _dsa = ecdsa.EllipticCurveDSA(_curve, _G, _N)

    def __init__(self, users) -> None:
        # Create genesis block
        self.interface = InterfaceHandler()
        self.chain = [Block()]
        self.interface.Debug("Genesis block created")
        self.chain[0].mine(self._DIFFICULTY)
        self.interface.Debug("Genesis block mined")

        self.admin_wallet = Wallet(
            public_name="Admin", blockchain=self, dsa=self._dsa)
        # Create wallets
        self.wallets = [Wallet(public_name=user, blockchain=self, dsa=self._dsa)
                        for user in users]
        self.interface.Debug(f"{len(self.wallets)} wallets created\n")

        self.interface.Debug(f"Giving users neurocoins ...\n")
        # Giving money to all users
        for i in range(len(self.wallets)):
            self.add_block(sender_wallet=self.admin_wallet,
                           recipient_wallet=self.wallets[i], value=150)

    def get_last_block(self) -> Block:
        # Get last block in the blockchain
        return self.chain[-1]

    def add_block(self, sender_wallet=None, recipient_wallet=None, value=100) -> None:
        # Add block to the blockchain

        if recipient_wallet is None and sender_wallet.public_name != "Admin" and recipient_wallet.public_name != "Admin":
            # If the recipient is not specified
            InterfaceHandler.Error("You must specify the recipient")
            return None
        if sender_wallet.public_name != "Admin" and recipient_wallet.public_name != "Admin":
            if sender_wallet.public_key == recipient_wallet.public_key:
                # If the sender and the recipient are the same
                InterfaceHandler.Error("You can't send money to yourself")
                return None

        # Create block and add it to the blockchain
        block = Block(self.get_last_block(), sender_wallet=sender_wallet,
                      recipient_wallet=recipient_wallet, v=value, dsa=self._dsa)

        # if Ecdsa.verify(block.get_hash(),
        #               block.get_signature_object(), sender_wallet.public_key):
        if self._dsa:
            if self._dsa.Verify(block.get_signature(), sender_wallet.key, block.get_hash()):
                if sender_wallet.public_name != "Admin" and recipient_wallet.public_name != "Admin":
                    choice = int(
                        input("\nDo you want to send message to recipient? (1 - yes, 2 - no): "))
                    if choice == 1:
                        block.add_message()

        block.mine(self._DIFFICULTY)
        self.interface.Debug(f"Block {len(self.chain)} mined")

        if sender_wallet.public_name != "Admin" and recipient_wallet.public_name != "Admin":
            block.set_brain_cells(
                block.get_nonce() * self._BRAIN_CELLS_COST)

            block.set_transacttion_cost(self._TRANSACTION_COST *
                                        block.get_value() + block.get_brain_cells())

        block.sign()
        self.interface.Debug(f"Block {len(self.chain)} signed")

        self.chain.append(block)
        self.interface.Debug(
            f"Block {len(self.chain) - 1} successfully added to the blockchain\n")

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
