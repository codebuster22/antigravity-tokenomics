# modules/JourneyPhaseManager.py

from modules.Account import Account

class JourneyPhaseManager:
    PHASE_DURATIONS = [15, 90, 1]  # Durations for Phase 1, Phase 2, and Phase 3
    TOTAL_JOURNEYS = 33

    def __init__(self):
        self.current_journey = 1
        self.current_phase = 1
        self.journey_nft_counts = {journey: 0 for journey in range(1, self.TOTAL_JOURNEYS + 1)}
        self.journey_balances = {journey: {} for journey in range(1, self.TOTAL_JOURNEYS + 1)}

    def increment_phase(self):
        if self.current_phase < 3:
            self.current_phase += 1
        else:
            self.current_phase = 1
            if self.current_journey < self.TOTAL_JOURNEYS:
                self.current_journey += 1

    def get_current_phase(self):
        return self.current_phase

    def get_current_journey(self):
        return self.current_journey

    def increment_nft_count(self, account: Account, amount: int):
        self.journey_nft_counts[self.current_journey] += amount
        if account.get_address() not in self.journey_balances[self.current_journey]:
            self.journey_balances[self.current_journey][account.get_address()] = 0
        self.journey_balances[self.current_journey][account.get_address()] += amount

    def decrement_nft_count(self, journey, account: Account, amount: int):
        if self.journey_nft_counts[journey] >= amount:
            self.journey_nft_counts[journey] -= amount
            self.journey_balances[journey][account.get_address()] -= amount

    def get_nft_count(self, journey):
        return self.journey_nft_counts.get(journey, 0)

    def get_account_nft_balance(self, journey, account: Account) -> int:
        return self.journey_balances[journey].get(account.get_address(), 0)
