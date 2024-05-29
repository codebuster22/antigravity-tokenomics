# modules/ERC721.py

from modules.Account import Account

class ERC721Token(Account):
    """Basic ERC-721 token class with token balances"""

    name = None

    def __init__(self):
        super().__init__()
        self.balances = {}
        self.total_supply = 0

    def balance_of(self, holder: Account) -> int:
        """Returns token count of account"""
        return self.balances.get(holder.get_address(), 0)

    def total_supply(self) -> int:
        """Returns the total supply of tokens"""
        return self.total_supply

    def mint(self, to: Account, amount: int):
        """Mints (creates new) tokens for the given account"""
        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0
        self.balances[to.get_address()] += amount
        self.total_supply += amount

    def transfer(self, frm: Account, to: Account, amount: int):
        """ERC-721 transfer sends tokens from one account to another"""
        assert self.balances.get(frm.get_address(), 0) >= amount, 'Transfer not authorized by owner'
        self.balances[frm.get_address()] -= amount
        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0
        self.balances[to.get_address()] += amount

    def burn(self, owner: Account, amount: int):
        """Burns (destroys) the specified amount of tokens"""
        assert self.balances.get(owner.get_address(), 0) >= amount, 'Burn not authorized by owner'
        self.balances[owner.get_address()] -= amount
        self.total_supply -= amount

    def __str__(self):
        return f'Token {self.name} ({self.address})'

    __repr__ = __str__
