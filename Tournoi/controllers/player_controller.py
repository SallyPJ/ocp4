from models.database import Database
from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    def __init__(self):
        # Initialize view and database
        self.player_view = PlayerView()
        self.database = Database()

    def create_player(self, last_name, first_name, date_of_birth, national_id):
        # Create a new player and save to the database
        new_player = Player(last_name, first_name, date_of_birth, national_id)
        players = self.database.load_players()
        players.append(new_player)
        self.database.save_players(players)





