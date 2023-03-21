from dataclasses import dataclass
import datetime
from hashlib import md5

from Interface import InterfaceHandler


@dataclass(frozen=True, order=True, kw_only=True)
class Block:

    def __init__(self, prev=None, nonce=0, sender_wallet=None, recipient_wallet=None, v=None, dsa=None, key=None) -> None:
        if prev is None:
            # If the previous block is not specified
            object.__setattr__(self, '_number', 0)
        else:
            # If the previous block is specified
            object.__setattr__(self, '_number', prev.get_number() + 1)
        object.__setattr__(self, 'interface', InterfaceHandler())
        # Set block data
        object.__setattr__(self, '_ver', 1)
        object.__setattr__(self, '_time', datetime.datetime.now())
        object.__setattr__(
            self, '_spk', sender_wallet.public_key_compressed if sender_wallet is not None else None)
        object.__setattr__(
            self, '_rpk', recipient_wallet.public_key_compressed if recipient_wallet is not None else None)
        object.__setattr__(self, '_value', v)
        object.__setattr__(self, '_transaction_cost', 0)
        object.__setattr__(self, '_brain_cells', 0)

        object.__setattr__(self, '_previous', prev)
        object.__setattr__(self, '_nonce', nonce)
        object.__setattr__(self, '_charline', '')
        object.__setattr__(self, '_signature', None)

        if dsa:
            object.__setattr__(self, '_signature', dsa.Sign(
                sender_wallet.key, self.get_hash()) if sender_wallet is not None else None)
        else:
            if sender_wallet is not None:
                sender_wallet.blockchain.interface.Debug(
                    "No DSA! Signature is None")
        object.__setattr__(self, '_signature_verified', False)

    def add_message(self):
        # Add message to the block
        object.__setattr__(self, '_charline', input("Enter message: "))
        self.interface.Debug("Message added")

    def get_message(self):
        # Get message from the block
        return self._charline

    def is_valid(self) -> bool:
        # Check if the block is valid
        if self._signature_verified:
            return True
        else:
            return False

    def sign(self):
        object.__setattr__(self, '_signature_verified', True)

    def unsign(self):
        object.__setattr__(self, '_signature_verified', False)

    def set_brain_cells(self, value):
        object.__setattr__(self, '_brain_cells', value)

    def get_brain_cells(self):
        return self._brain_cells

    def set_transacttion_cost(self, value):
        object.__setattr__(self, '_transaction_cost', value)

    def get_transaction_cost(self):
        return self._transaction_cost

    def get_previouis_hash(self) -> str:
        # Get previous block hash
        if self._previous is None:
            return '0' * 32
        else:
            return self._previous.get_hash()

    def get_signature_object(self) -> str:
        # Get signature of the block
        return self._signature

    def get_signature(self) -> str:
        # Get signature of the block
        if self._signature:
            return self._signature
        return None

    def get_balance(self, public_key):
        # Get balance of the user
        if self._spk is None:
            return 0
        elif public_key == self._spk:
            return -self._value
        elif public_key == self._rpk:
            return self._value
        return 0

    def get_hash(self):
        # Get block hash
        return self.calc_hash(self._number, self.get_previouis_hash(), self._nonce, self._ver, self._time, self._value, self._spk, self._rpk)

    def get_number(self) -> int:
        # Get block number
        return self._number

    def get_reciever_public_key(self) -> str:
        # Get reciever public key
        return self._rpk

    def get_sender_public_key(self) -> str:
        # Get sender public key
        return self._spk

    def get_value(self) -> int:
        # Get value of the block
        return self._value

    def get_nonce(self) -> int:
        # Get nonce of the block
        return self._nonce

    def mine(self, num_zeroes: int) -> None:
        # Mine block with specified number of zeroes in the beginning of the hash
        if num_zeroes:
            while (self.get_hash()[0:num_zeroes] != '0' * num_zeroes) or self.get_hash()[-1] != '1':
                object.__setattr__(self, '_nonce', self._nonce + 1)

    def get_time(self) -> datetime.datetime:
        # Get time of the block
        return self._time

    def get_block_info(self):
        # Print block data to console

        self.interface.Block(block=self)

    def calc_hash(*args):
        # Calculate hash of the block
        # TODO: Change method of calculating hash

        h = md5()
        block_string = ""
        for arg in args:
            block_string += str(arg)
        h.update(block_string.encode('utf-8'))
        return h.hexdigest()
