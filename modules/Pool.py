# modules/Pool.py

from modules.Dark import DarkToken
from modules.DAIStableCoin import DAIStableCoin
from modules.Account import Account

class Pool(Account):
    def __init__(self, dark_token: DarkToken, dai_token: DAIStableCoin, fee: float = 0.003):
        super().__init__()
        self.dark_token = dark_token
        self.dai_token = dai_token
        self.fee = fee
        self.dark_reserve = 0
        self.dai_reserve = 0
        self.total_volume = 0  # Track total trading volume

    def add_liquidity(self, provider: Account, dark_amount: int, dai_amount: int):
        assert self.dai_token.balance_of(provider) >= dai_amount, 'Insufficient DAI balance'
        assert self.dark_token.balance_of(provider) >= dark_amount, 'Insufficient Dark token balance'

        self.dai_token.transfer(provider, self, dai_amount)
        self.dark_token.transfer(provider, self, dark_amount)

        self.dark_reserve += dark_amount
        self.dai_reserve += dai_amount

    def update_fee(self, new_fee: float):
        self.fee = new_fee

    def get_price(self) -> float:
        return self.dai_reserve / self.dark_reserve

    def buy(self, buyer: Account, dai_amount: int):
        amount_with_fee = dai_amount * (1 - self.fee)
        dark_amount = amount_with_fee * self.dark_reserve / self.dai_reserve

        assert self.dai_token.balance_of(buyer) >= dai_amount, 'Insufficient DAI balance'
        assert self.dark_reserve >= dark_amount, 'Insufficient Dark tokens in reserve'

        self.dai_token.transfer(buyer, self, dai_amount)
        self.dark_token.transfer(self, buyer, dark_amount)

        self.dai_reserve += dai_amount
        self.dark_reserve -= dark_amount

        self.total_volume += dai_amount  # Update total volume

    def sell(self, seller: Account, dark_amount: int):
        amount_with_fee = dark_amount * (1 - self.fee)
        dai_amount = amount_with_fee * self.dai_reserve / self.dark_reserve

        assert self.dark_token.balance_of(seller) >= dark_amount, 'Insufficient Dark token balance'
        assert self.dai_reserve >= dai_amount, 'Insufficient DAI tokens in reserve'

        self.dark_token.transfer(seller, self, dark_amount)
        self.dai_token.transfer(self, seller, dai_amount)

        self.dark_reserve += dark_amount
        self.dai_reserve -= dai_amount

        self.total_volume += dai_amount  # Update total volume

    def __str__(self):
        return f'Pool: Dark reserve = {self.dark_reserve}, DAI reserve = {self.dai_reserve}, Fee = {self.fee}, Total volume = {self.total_volume}'

    __repr__ = __str__
