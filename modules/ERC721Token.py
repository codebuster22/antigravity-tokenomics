# modules/ERC721.py

from modules.Account import Account

class ERC721Token(Account):
    """Basic ERC-721 token class with token ownerships"""

    name = None

    def __init__(self):
        super().__init__()

        self.token_owners = {}
        self.balances = {}
        self.current_token_id = 0

    def balance_of(self, holder: Account) -> int:
        """Returns token count of account"""

        return self.balances.get(holder.get_address(), 0)

    def owner_of(self, token_id: int) -> str:
        """Returns the owner of the specified token ID"""

        return self.token_owners.get(token_id, None)

    def mint(self, to: Account, amount: int):
        """Mints (creates new) tokens for the given account"""

        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0

        for _ in range(amount):
            self.token_owners[self.current_token_id] = to.get_address()
            self.balances[to.get_address()] += 1
            self.current_token_id += 1

    def transfer(self, frm: Account, to: Account, token_id: int):
        """ERC-721 transfer sends token from one account to another"""

        assert self.token_owners.get(token_id) == frm.get_address(), 'Transfer not authorized by owner'

        self.token_owners[token_id] = to.get_address()

        self.balances[frm.get_address()] -= 1
        if to.get_address() not in self.balances:
            self.balances[to.get_address()] = 0
        self.balances[to.get_address()] += 1

    def __str__(self):
        return f'Token {self.name} ({self.address})'

    __repr__ = __str__
