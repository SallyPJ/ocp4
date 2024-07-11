import json
import os
from models.player import Player
from models.tournament import Tournament

PLAYERS_FILE = "players.json"
TOURNAMENTS_FILE = "tournaments.json"

def load_players():
    if not os.path.exists(PLAYERS_FILE):
        # Create the file with an empty list if it does not exist
        with open(PLAYERS_FILE, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []
    else:
        with open(PLAYERS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Player.from_dict(player) for player in data]# Ajout message d'erreur json empty ?

# Fonction pour enregistrer la base de données des joueurs
def save_players(players):
    with open(PLAYERS_FILE, 'w', encoding='utf-8') as file:
        json.dump([player.to_dict() for player in players], file, ensure_ascii=False, indent=4)

def load_tournaments():
    tournaments = []
    try:
        with open(TOURNAMENTS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            tournaments = [Tournament.from_dict(tournament_data) for tournament_data in data]
    except FileNotFoundError:
        print("Fichier de tournois non trouvé.")
    except json.JSONDecodeError:
        print("Erreur de décodage JSON.")
    return tournaments


def save_tournament(tournaments):
    with open(TOURNAMENTS_FILE, 'w', encoding='utf-8') as file:
        json.dump([tournament.to_dict() for tournament in tournaments], file, ensure_ascii=False, indent=4)