from models.player import Player
from models.database import load_players, save_players


def create_player(last_name, first_name, date_of_birth, national_id):
    players = load_players()
    new_player = Player(last_name, first_name, date_of_birth, national_id)
    players.append(new_player)
    save_players(players)

# Fonction pour obtenir les informations du joueur depuis la console
def get_player_info():
    last_name = input("Nom de famille : ")
    first_name = input("Prénom : ")
    date_of_birth = input("Date de naissance (AAAA-MM-JJ) : ")
    national_id = input("Identifiant : ")
    return last_name, first_name, date_of_birth, national_id

def select_player(players):
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
            print("Veuillez entrer un numéro valide.")