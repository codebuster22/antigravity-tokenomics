# modules/Pool.py

from modules.Dark import DarkToken
from modules.DAIStableCoin import DAIStableCoin
from modules.Account import Account

class Pool:
    def __init__(self, dark_token: DarkToken, dai_token: DAIStableCoin, fee: float = 0.003):
        self.dark_token = dark_token
        self.dai_token = dai_token
        self.fee = fee
        self.dark_reserve = 0
        self.dai_reserve = 0

    def add_liquidity(self, dark_amount: int, dai_amount: int):
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

    def sell(self, seller: Account, dark_amount: int):
        amount_with_fee = dark_amount * (1 - self.fee)
        dai_amount = amount_with_fee * self.dai_reserve / self.dark_reserve

        assert self.dark_token.balance_of(seller) >= dark_amount, 'Insufficient Dark token balance'
        assert self.dai_reserve >= dai_amount, 'Insufficient DAI tokens in reserve'

        self.dark_token.transfer(seller, self, dark_amount)
        self.dai_token.transfer(self, seller, dai_amount)

        self.dark_reserve += dark_amount
        self.dai_reserve -= dai_amount

    def __str__(self):
        return f'Pool: Dark reserve = {self.dark_reserve}, DAI reserve = {self.dai_reserve}, Fee = {self.fee}'

    __repr__ = __str__

# Example usage
if __name__ == "__main__":
    dark_token = DarkToken()
    dai_token = DAIStableCoin()
    user_account = Account()
    pool_account = Account()

    # Mint some tokens for the user and the pool
    dark_token.mint(user_account, 1000)
    dai_token.mint(user_account, 5000)
    dark_token.mint(pool_account, 10000)
    dai_token.mint(pool_account, 50000)

    # Initialize the Pool
    pool = Pool(dark_token, dai_token)

    # Add liquidity to the pool
    pool.add_liquidity(10000, 50000)

    # User buys Dark tokens
    pool.buy(user_account, 1000)

    # User sells Dark tokens
    pool.sell(user_account, 50)

    print(pool)

    print("User Balances:")
    print(f"Dark: {dark_token.balance_of(user_account)}")
    print(f"DAI: {dai_token.balance_of(user_account)}")
