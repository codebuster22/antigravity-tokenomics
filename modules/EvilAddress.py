# modules/EvilAddress.py

from modules.Account import Account
from modules.LaunchControlCenter import LaunchControlCenter
from modules.Dark import DarkToken
from modules.FuelCells import FuelCellsToken

class EvilAddress(Account):
    def __init__(self, dark_token: DarkToken, fuel_cells_token: FuelCellsToken, lcc: LaunchControlCenter):
        super().__init__()
        self.dark_token = dark_token
        self.fuel_cells_token = fuel_cells_token
        self.lcc = lcc

    def mint_fuel_cells(self, amount: int):
        """Mints FuelCells NFTs using Dark tokens"""
        self.lcc.mint_nft(self, amount)
