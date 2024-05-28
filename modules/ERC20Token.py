# modules/ERC20.py

from modules.Account import Account

class ERC20Token(Account):
    """Basic ERC-20 token class with balances and totalSupply"""

    name = None

    def __init__(self):
        super().__init__()

        self.balances = {}
        self.total_supply = 0

    def balance_of(self, holder: Account) -> int:
        """Returns tokens balance of account"""

        return self.balances.get(holder.get_address(), 0)

    def mint(self, to: Account, tokens: int):
        """Mints (creates new amount of) tokens for the given account"""

        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0

        self.balances[to.get_address()] += tokens
        self.total_supply += tokens

    def transfer(self, frm: Account, to: Account, tokens: int):
        """ERC-20 transfer sends tokens from one account to another"""

        assert self.balances[frm.get_address()] >= tokens, 'Insufficient tokens for transfer'

        self.balances[frm.get_address()] -= tokens

        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0

        self.balances[to.get_address()] += tokens

    def __str__(self):
        return f'Token {self.name} ({self.address})'

    __repr__ = __str__
