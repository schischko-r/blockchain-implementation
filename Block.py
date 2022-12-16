from dataclasses import dataclass
import datetime
from hashlib import md5
import string
import random
import os


@dataclass(frozen=True, order=True, kw_only=True)
class Block:

    def __init__(self, prev=None, data=None, nonce=0, spk=None, rpk=None, v=None) -> None:
        if prev is None:
            # If the previous block is not specified
            object.__setattr__(self, '_number', 0)
        else:
            # If the previous block is specified
            object.__setattr__(self, '_number', prev.get_number() + 1)

        # Set block data
        object.__setattr__(self, '_ver', 1)
        object.__setattr__(self, '_time', datetime.datetime.now())
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_spk', spk)
        object.__setattr__(self, '_rpk', rpk)
        object.__setattr__(self, '_value', v)
        object.__setattr__(self, '_previous', prev)
        object.__setattr__(self, '_nonce', nonce)
        object.__setattr__(self, '_charline', '')

    def get_previouis_hash(self) -> str:
        # Get previous block hash
        if self._previous is None:
            return '0' * 32
        else:
            return self._previous.get_hash()

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
        return self.calc_hash(self._number, self.get_previouis_hash(), self._data, self._nonce, self._ver, self._time, self._value, self._spk, self._rpk)

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

    def get_data(self) -> dict:
        # Get data of the block
        return self._data

    def get_nonce(self) -> int:
        # Get nonce of the block
        return self._nonce

    def mine(self, num_zeroes: int) -> None:
        # Mine block with specified number of zeroes in the beginning of the hash
        while (self.get_hash()[0:num_zeroes] != '0' * num_zeroes) or self.get_hash()[-1] != '1':
            object.__setattr__(self, '_nonce', self._nonce + 1)

    def set_data(self, data) -> None:
        # Set data of the block
        object.__setattr__(self, '_data', data)

    def __str__(self) -> str:
        # Print block data to console
        return f'Block {self.get_number()}\nSPK: {self.get_sender_public_key()}\nRPK: {self.get_reciever_public_key()}\nValue: {self.get_value()}'

    def calc_hash(*args):
        # Calculate hash of the block
        # TODO: Change mathod of calculating hash

        h = md5()
        block_string = ""
        for arg in args:
            block_string += str(arg)
        h.update(block_string.encode('utf-8'))
        return h.hexdigest()
