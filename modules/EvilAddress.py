# modules/EvilAddress.py

from modules.Account import Account
from modules.LaunchControlCenter import LaunchControlCenter
from modules.Dark import DarkToken
from modules.FuelCells import FuelCellsToken
from modules.JourneyPhaseManager import JourneyPhaseManager
import numpy as np

class EvilAddress(Account):
    TOTAL_JOURNEYS = 33

    def __init__(self, dark_token: DarkToken, fuel_cells_token: FuelCellsToken, lcc: LaunchControlCenter, journey_phase_manager: JourneyPhaseManager, starting_balance: int):
        super().__init__()
        self.dark_token = dark_token
        self.fuel_cells_token = fuel_cells_token
        self.lcc = lcc
        self.starting_balance = starting_balance
        self.jpm = journey_phase_manager
        self.b = 10.3136  # starting percentage of spend from the evil address
        self.r = 0.9
        self.total_spend = 0
        self.journey_spend = {journey: 0 for journey in range(1, self.TOTAL_JOURNEYS + 1)}

    def mint_fuel_cells(self):
        """Mints FuelCells NFTs using Dark tokens"""
        current_journey = self.jpm.get_current_journey()
        amount_to_mint = np.floor(self.starting_balance * self.b * (self.r ** (current_journey - 1)) / 100)
        
        if self.dark_token.balance_of(self) < amount_to_mint:
            raise ValueError("Insufficient Dark tokens to mint FuelCells NFTs")

        self.total_spend += amount_to_mint
        self.journey_spend[current_journey] += amount_to_mint

        # Calculate the number of NFTs to mint
        nfts_to_mint = int(amount_to_mint)

        self.lcc.mint_nft(self, nfts_to_mint)

    def get_total_spend(self):
        return self.total_spend

    def get_journey_spend(self, journey):
        return self.journey_spend.get(journey, 0)
