# modules/Team.py

from modules.Account import Account

class Team(Account):
    def __init__(self):
        super().__init__()

# Example usage
if __name__ == "__main__":
    team_account = Team()
    print(f"Created team account with address: {team_account.get_address()}")
