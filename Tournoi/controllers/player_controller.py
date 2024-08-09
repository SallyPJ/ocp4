from models.player import Player
from models.database import Database
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

    def load_players(self):
        # Load players from the database
        return self.database.load_players()




    def select_players(self, expected_player_count):
        while True:
            self.player_view.display_players(self.players)
            player_choices = self.view.select_players_input()
            selected_players = self.process_player_choices(player_choices)

            if len(selected_players) != expected_player_count:
                self.view.display_message(
                    f"Erreur : Vous devez sélectionner exactement {expected_player_count} joueurs.")
            else:
                self.view.display_selected_players(selected_players)
                confirmation = self.view.confirm_selection()
                if confirmation.lower() == 'o':
                    self.view.display_message("Tous les joueurs ont été sélectionnés.")
                    break
                else:
                    self.view.display_message("Réinitialisation de la sélection des joueurs.")

