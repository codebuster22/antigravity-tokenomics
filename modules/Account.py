# modules/Account.py

import random
import string

class Account:
    def __init__(self, address=None):
        self.address = address or self._generate_address()

    def _generate_address(self):
        return '0x' + ''.join(random.choices(string.hexdigits[:16], k=40))

    def get_address(self):
        return self.address
