# modules/Treasury.py

from modules.Account import Account
from modules.FuelCells import FuelCellsToken
from modules.JourneyPhaseManager import JourneyPhaseManager
from modules.Dark import DarkToken

class Treasury:
    def __init__(self, account: Account, dark_token: DarkToken):
        self.account = account
        self.dark_token = dark_token
        self.yield_formula_a = 3
        self.yield_formula_r = 0.9
        self.journey_yields = {journey: 0 for journey in range(1, 34)}
        self.total_yield_distributed = 0
        self.remaining_balance = 0

    def calculate_yield(self, journey: int) -> float:
        return self.yield_formula_a * (self.yield_formula_r ** (journey - 1))

    def total_yield_percentage(self, journey: int) -> float:
        return self.yield_formula_a * (self.yield_formula_r ** journey - 1) / (self.yield_formula_r - 1)

    def distribute_yield(self, journey_phase_manager: JourneyPhaseManager):
        treasury_balance = self.dark_token.balance_of(self.account) - self.total_yield_distributed
        total_yield_percentage = self.total_yield_percentage(journey_phase_manager.get_current_journey())
        total_yield_value = total_yield_percentage * treasury_balance / 100
        self.remaining_balance = treasury_balance - total_yield_value
        for journey in range(1, min(journey_phase_manager.get_current_journey() + 1, 33)):
            yield_percentage = self.calculate_yield(journey)
            yield_value = yield_percentage * treasury_balance / 100
            self.journey_yields[journey] += yield_value
            self.total_yield_distributed += yield_value

    def get_total_yield_for_journey(self, journey: int) -> float:
        return self.journey_yields[journey]

    def get_nft_yield(self, journey: int, nft_count: int) -> float:
        if nft_count > 0:
            return self.journey_yields[journey] / nft_count
        return 0

    def burn_nfts(self, owner: Account, journey: int, nft_count: int, fuel_cells_token: FuelCellsToken, journey_phase_manager: JourneyPhaseManager):
        current_nft_count = journey_phase_manager.get_nft_count(journey)
        owner_balance = journey_phase_manager.get_account_nft_balance(journey, owner)
        if current_nft_count > 0 and nft_count <= owner_balance:
            nft_yield = self.get_nft_yield(journey, current_nft_count)
            total_yield = nft_yield * nft_count
            self.journey_yields[journey] -= total_yield
            journey_phase_manager.decrement_nft_count(journey, owner, nft_count)
            fuel_cells_token.burn(owner, nft_count)
            self.dark_token.transfer(self.account, owner, total_yield)
