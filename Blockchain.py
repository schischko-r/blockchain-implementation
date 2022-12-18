from Block import Block
from Wallet import Wallet
from Interface import InterfaceHandler
from ellipticcurve.ecdsa import Ecdsa


class Blockchain:

    _chain: list
    # _DIFFICULTY  is the number of zeros at the beginning of the hash
    _DIFFICULTY = 0

    def __init__(self, users) -> None:
        # Create genesis block
        self.chain = [Block()]
        self.chain[0].mine(self._DIFFICULTY)
        # Create wallets
        self.wallets = [Wallet(public_name=user[0], blockchain=self)
                        for user in users]

        # Giving money to all users
        for i in range(len(self.wallets)):
            self.add_block(sender_wallet=Wallet(public_name="God", blockchain=self),
                           recipient_wallet=self.wallets[i], value=150)

    def get_last_block(self) -> Block:
        # Get last block in the blockchain
        return self.chain[-1]

    def add_block(self, sender_wallet=None, recipient_wallet=None, value=100, ) -> None:
        # Add block to the blockchain

        if recipient_wallet is None:
            # If the recipient is not specified
            InterfaceHandler.Error("You must specify the recipient")
            return None

        if sender_wallet.public_key == recipient_wallet.public_key:
            # If the sender and the recipient are the same
            InterfaceHandler.Error("You can't send money to yourself")
            return None

        # Create block and add it to the blockchain
        block = Block(self.get_last_block(),
                      sender_wallet=sender_wallet, recipient_wallet=recipient_wallet, v=value)

        if Ecdsa.verify(block.get_hash(),
                        block.get_signature_object(), sender_wallet.public_key):
            block.mine(self._DIFFICULTY)
            self.chain.append(block)
        else:
            pass

    def get_chain(self) -> list:
        # Get blockchain
        return self.chain

    def __str__(self) -> str:
        # Print blockchain data to console
        return '\n\n'.join([block.get_block_info() for block in self.chain]) + "\n\n"
