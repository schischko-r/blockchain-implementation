from Block import Block
from Wallet import Wallet
import random
import datetime
import BeatyPrint


class Blockchain:

    _chain: list
    # _DIFFICULTY  is the number of zeros at the beginning of the hash
    _DIFFICULTY = 3

    def __init__(self, users) -> None:
        # Create genesis block
        self.chain = [Block()]
        self.chain[0].mine(self._DIFFICULTY)
        # Create wallets
        self.wallets = [Wallet(*user, self) for user in users]

        # Giving money to all users
        for i in range(len(self.wallets)):
            self.add_block(data=datetime.datetime.now(), sender_public_key='MONEY FROM GOD',
                           recipient_public_key=self.wallets[i].public_key, value=150)

    def set_user_data(self, data) -> None:
        # Set user data
        self.user_data.update(data)

    def get_last_block(self) -> Block:
        # Get last block in the blockchain
        return self.chain[-1]

    def add_block(self, data, sender_public_key=None, recipient_public_key=None, value=100) -> None:
        # Add block to the blockchain
        if sender_public_key == recipient_public_key:
            # If the sender and the recipient are the same
            BeatyPrint.Error("You can't send money to yourself")
            return None

        if recipient_public_key is None:
            # If the recipient is not specified
            BeatyPrint.Error("You must specify the recipient")
            return None

        # Create block and add it to the blockchain
        block = Block(self.get_last_block(), data,
                      spk=sender_public_key, rpk=recipient_public_key, v=value)
        block.mine(self._DIFFICULTY)
        self.chain.append(block)

    def get_chain(self) -> list:
        # Get blockchain
        return self.chain

    def __str__(self) -> str:
        # Print blockchain data to console
        return '\n\n'.join([str(block) for block in self.chain]) + "\n\n" + "\n".join([f'{"="*10}\t{wallet.public_name} balance: {wallet.get_balance()}\t{"="*10}' for wallet in self.wallets])

    def change_block_data(self, block_number: int, data) -> None:
        # Change block data
        self.chain[block_number].set_data(data)
