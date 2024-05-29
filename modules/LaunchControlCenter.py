# modules/LaunchControlCenter.py

from modules.Dark import DarkToken
from modules.FuelCells import FuelCellsToken
from modules.Account import Account
from modules.JourneyPhaseManager import JourneyPhaseManager

class LaunchControlCenter:
    def __init__(self, dark_token: DarkToken, fuel_cells_token: FuelCellsToken, treasury: Account, magic_box: Account, team: Account, journey_phase_manager: JourneyPhaseManager):
        self.dark_token = dark_token
        self.fuel_cells_token = fuel_cells_token
        self.treasury = treasury
        self.magic_box = magic_box
        self.team = team
        self.journey_phase_manager = journey_phase_manager

    def mint_nft(self, from_account: Account, amount: int):
        """Mints NFTs in exchange for Dark tokens"""

        # Ensure the user has enough Dark tokens to mint NFTs
        if self.dark_token.balance_of(from_account) < amount:
            raise ValueError("Insufficient Dark tokens for minting NFTs")

        # Transfer Dark tokens to the LaunchControlCenter
        self.dark_token.transfer(from_account, self.treasury, amount * 0.77)
        self.dark_token.transfer(from_account, self.magic_box, amount * 0.20)
        self.dark_token.transfer(from_account, self.team, amount * 0.03)

        # Mint the NFTs and increment the NFT count in the JourneyPhaseManager
        self.fuel_cells_token.mint(from_account, amount)
        self.journey_phase_manager.increment_nft_count(amount)
