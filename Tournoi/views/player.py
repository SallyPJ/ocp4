from models.database import load_players


def display_players():
    try:
        players = load_players()
        if not players:
            print("Aucun joueur trouvé.")
            return
        print("Liste des joueurs :")
        for i, player in enumerate(players, start=1):
            print(f"{i}. Nom de famille: Nom de famille: {player.last_name}, Prénom: {player.first_name}, Date de naissance: {player.date_of_birth}, Identifiant: {player.national_id}")
    except FileNotFoundError:
        print("Liste des joueurs non trouvé")

def display_selected_players(self):
    print("Joueurs sélectionnés :")
    for i, player in enumerate(self.selected_players, start=1):
        print(f"{i}. {player.last_name} {player.first_name}")

