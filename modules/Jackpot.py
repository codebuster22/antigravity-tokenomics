# Jackpot contract is responsible for conducting lucky draws. Eligible participants are accounts who minted NFTs in the current journey. Jackpot will conduct 10 distinct lotteries.
# Each lottery will have different percentage of payout but the number of winners will be same.
# Let's say
# current journey = J
# total nfts minted in journey J = x
# total balance of Jackpot = y
# number of winners of lottery in current journey = round_down((x * 5) / 100) 
# number of winners of each lottery = (number of winners of lottery in current journey)/10
# number of lotteries in current journey = 10

# common ratio = c = 2
# starting lottery payout percentage = a1 = 0.09775

# hence the payouts for each lottery will be as follows:
# Payout percentage of Lottery 1 in Journey J = a1 * (c**(1-1))
# Payout percentage of Lottery 2 in journey J = a1 * (c**(2-1))
# Payout percentage of Lottery 3 in Journey J = a1 * (c**(3-1))
# Payout percentage of Lottery 4 in Journey J = a1 * (c**(4-1))
# .
# .
# .
# Payout percentage of Lottery 10 in Journey J = a1 * (c**(10-1))

# The formulae for payout percentage = a1 * (c**(n-1)) where n is the lottery number

# Now, the lottery will be given based on the starting balance of Jackpot in the journey.
# Let's say starting balance of Jackpot was 20,000 Dark tokens,
# Then the total payout will be:

# given, startingBalance_in_J = 20000
# then,
# payout of Lottery 1 = startingBalance_in_J * payout_percentage_lottery1 / 100
# payout of Lottery 2 = startingBalance_in_J * payout_percentage_lottery2 / 100
# payout of Lottery 3 = startingBalance_in_J * payout_percentage_lottery3 / 100
# .
# .
# .
# payout of Lottery 10 = startingBalance_in_J * payout_percentage_lottery10 / 100

# The payout in each journey is distributed among the number of winners of each lottery

# Here's how lottery will operate:

# Journey J starts:
# Minting phase over
# Lottery 1 winner selected and payout distributed
# Lottery 2 winner selected and payout distributed
# Lottery 3 winner selected and payout distributed
# Lottery 4 winner selected and payout distributed
# Lottery 5 winner selected and payout distributed
# Lottery 6 winner selected and payout distributed
# Lottery 7 winner selected and payout distributed
# Lottery 8 winner selected and payout distributed
# Lottery 9 winner selected and payout distributed
# Lottery 10 winner selected and payout distributed
# Treasury gives yield
# Start next journey J++ and repeat

# modules/Jackpot.py

from modules.Account import Account
from modules.Dark import DarkToken
from modules.JourneyPhaseManager import JourneyPhaseManager
from modules.FuelCells import FuelCellsToken
import numpy as np

class Jackpot:
    def __init__(self, account: Account, dark_token: DarkToken, journey_phase_manager: JourneyPhaseManager, fuel_cells_token: FuelCellsToken):
        self.account = account
        self.dark_token = dark_token
        self.journey_phase_manager = journey_phase_manager
        self.fuel_cells_token = fuel_cells_token
        self.common_ratio = 2
        self.starting_payout_percentage = 0.09775
        self.lotteries_per_journey = 10
        self.lottery_winnings = {}  # Dictionary to store total lottery winnings per account per journey

    def calculate_payout_percentage(self, lottery_number: int) -> float:
        """Calculate the payout percentage for a given lottery number"""
        return self.starting_payout_percentage * (self.common_ratio ** (lottery_number - 1))

    def calculate_payouts(self, journey: int, starting_balance: int) -> list:
        """Calculate the payouts for all lotteries in a journey"""
        payouts = []
        for i in range(1, self.lotteries_per_journey + 1):
            payout_percentage = self.calculate_payout_percentage(i)
            payout_amount = starting_balance * payout_percentage / 100
            payouts.append(payout_amount)
        return payouts

    def select_winners(self, participants: list, num_winners: int) -> list:
        """Select winners based on probability from the list of participants"""
        total_nfts = sum([self.journey_phase_manager.get_account_nft_balance(self.journey_phase_manager.get_current_journey(), account) for account in participants])
        probabilities = [self.journey_phase_manager.get_account_nft_balance(self.journey_phase_manager.get_current_journey(), account) / total_nfts for account in participants]
        winners = np.random.choice(participants, num_winners, p=probabilities, replace=True)
        return winners

    def conduct_lottery(self):
        """Conducts the lottery for the current journey"""
        current_journey = self.journey_phase_manager.get_current_journey()
        total_nfts_minted = self.journey_phase_manager.get_nft_count(current_journey)
        starting_balance = self.dark_token.balance_of(self.account)

        if total_nfts_minted == 0:
            return "No NFTs minted in the current journey, no lottery conducted."

        total_winners = max(1, total_nfts_minted * 5 // 100)  # Ensure at least one winner
        winners_per_lottery = max(1, total_winners // self.lotteries_per_journey)

        # Convert addresses (strings) to Account objects and ensure they are in the balances
        participants = []
        for address in self.journey_phase_manager.journey_balances[current_journey].keys():
            if self.journey_phase_manager.journey_balances[current_journey][address] > 0:
                account = Account(address)
                if address not in self.dark_token.balances:
                    self.dark_token.balances[address] = 0
                participants.append(account)

        payouts = self.calculate_payouts(current_journey, starting_balance)

        if current_journey not in self.lottery_winnings:
            self.lottery_winnings[current_journey] = {}

        for i in range(self.lotteries_per_journey):
            winners = self.select_winners(participants, winners_per_lottery)
            payout_amount = payouts[i] / winners_per_lottery
            for winner in winners:
                self.dark_token.transfer(self.account, winner, payout_amount)
                winner_address = winner.get_address()
                if winner_address not in self.lottery_winnings[current_journey]:
                    self.lottery_winnings[current_journey][winner_address] = 0
                self.lottery_winnings[current_journey][winner_address] += payout_amount

        return "Lottery conducted and payouts distributed."

    def get_lottery_winnings(self, journey: int, account: Account) -> int:
        """Get the total lottery winnings for an account in a specific journey"""
        return self.lottery_winnings.get(journey, {}).get(account.get_address(), 0)
