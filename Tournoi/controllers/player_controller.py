from models.player import Player
from models.database import Database
from views.player_view import PlayerView
class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()
        self.player = Player
        self.database = Database()

    def create_player(self, last_name, first_name, date_of_birth, national_id):
        try:
            new_player = self.player(last_name, first_name, date_of_birth, national_id)
            players = self.database.load_players()
            players.append(new_player)
            self.database.save_players(players)
        except Exception as e:
            print("Erreur lors de la création d'un joueur")
            #self.view.display_error(f"Erreur lors de la création du joueur : {e}")

    def select_player(self, players):
        #players = self.database.load_players()
        #self.player_view.display_players(players)
        selected_player = None
        while not selected_player:
            choice = self.player_view.select_player_input()
            if choice is not None and 1 <= choice <= len(players):
                selected_player = players[choice - 1]
            else:
                self.player_view.display_selected_player(None)

        self.player_view.display_selected_player(selected_player)
        return selected_player

    #def select_player(self):
        '''players = load_players()
        self.view.display_players(players)
        while True:
            try:
                choice = int(input("Entrez le numéro du joueur que vous souhaitez sélectionner : "))
                if 1 <= choice <= len(players):
                    selected_player = players[choice - 1]
                    print(
                        f"Vous avez sélectionné le joueur : {selected_player.last_name} {selected_player.first_name}")
                    return selected_player  # Retourne le joueur sélectionné
                else:
                    print(f"Veuillez entrer un numéro entre 1 et {len(players)}.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")'''