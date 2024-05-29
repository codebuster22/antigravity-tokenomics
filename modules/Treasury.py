# modules/Treasury.py

from modules.Account import Account
from modules.FuelCells import FuelCellsToken
from modules.JourneyPhaseManager import JourneyPhaseManager

class Treasury:
    def __init__(self, account: Account):
        self.account = account
        self.yield_formula_a = 3
        self.yield_formula_r = 0.9
        self.journey_yields = {journey: 0 for journey in range(1, 34)}

    def calculate_yield(self, journey: int) -> float:
        return self.yield_formula_a * (self.yield_formula_r ** (journey - 1))

    def distribute_yield(self, journey_phase_manager: JourneyPhaseManager):
        treasury_balance = self.account.get_balance()
        for journey in range(1, journey_phase_manager.TOTAL_JOURNEYS + 1):
            yield_percentage = self.calculate_yield(journey)
            yield_value = yield_percentage * treasury_balance / 100
            self.journey_yields[journey] += yield_value

    def get_total_yield_for_journey(self, journey: int) -> float:
        return self.journey_yields[journey]

    def get_nft_yield(self, journey: int, nft_count: int) -> float:
        if nft_count > 0:
            return self.journey_yields[journey] / nft_count
        return 0

    def burn_nft(self, owner: Account, journey: int, nft_id: int, fuel_cells_token: FuelCellsToken, journey_phase_manager: JourneyPhaseManager):
        nft_count = journey_phase_manager.get_nft_count(journey)
        if nft_count > 0:
            nft_yield = self.get_nft_yield(journey, nft_count)
            self.journey_yields[journey] -= nft_yield
            journey_phase_manager.decrement_nft_count(journey)
            fuel_cells_token.burn(owner, nft_id)
            self.account.transfer(owner, nft_yield)
