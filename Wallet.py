import datetime
from Interface import InterfaceHandler
from ellipticcurve.privateKey import PrivateKey


class Wallet:

    _TRANSACTION_FEE = 0.01

    def __init__(self, blockchain, public_name=None, dsa=None):
        # Blockchain of the wallet
        self.blockchain = blockchain
        self.interface = InterfaceHandler()
        self.blockchain.interface = self.interface
        if public_name is None:
            self.interface.new_user_welcoming_message(side_wallet=self)
        else:
            self.public_name = public_name
            # Public key of the wallet
        self.key = dsa.GeneratePair()
        self.private_key = self.key[0]  # Private key of the wallet
        self.public_key = self.key[1]
        self.public_key_compressed = "".join(
            [l for l in str(self.key[1]) if l in "0123456789abcdefABCDEF"])

        self._dsa = dsa

    def get_balance(self):
        # Get balance of the wallet
        return sum([block.get_balance(self.public_key_compressed)
                    for block in self.blockchain.chain])

    def send_money(self, recipient_public_key, value):
        # Send money to another wallet
        if self.get_balance() < value:
            # If the wallet doesn't have enough money
            InterfaceHandler.Error('Not enough neurocoins')
            return

        if value < 0:
            # If the value is negative
            InterfaceHandler.Error('Value must be positive')
            return
        # Add block with sending money to another user to the blockchain
        # find wallet with recipient public key
        self.blockchain.add_block(sender_wallet=self,
                                  recipient_wallet=self.blockchain.wallets[[wallet.public_key_compressed for wallet in self.blockchain.wallets].index(
                                      recipient_public_key)], value=value)

        # Transaction fee
        self.blockchain.add_block(
            sender_wallet=self, recipient_wallet=self.blockchain.admin_wallet, value=self.blockchain.chain[-1].get_transaction_cost())

    def login(self, public_name):
        if public_name in [self.blockchain.wallets[i].public_name for i in range(len(self.blockchain.wallets))]:
            return True
        else:
            return False
