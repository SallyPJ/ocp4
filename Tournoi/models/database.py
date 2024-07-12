import json
import os
from models.player import Player
from models.tournament import Tournament

class Database:
    PLAYERS_FILE = "players.json"
    TOURNAMENTS_FILE = "tournaments.json"

    @classmethod
    def load_players(cls):
        if not os.path.exists(cls.PLAYERS_FILE):
            # Create the file with an empty list if it does not exist
            with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []
        else:
            with open(cls.PLAYERS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Player.from_dict(player) for player in data]# Ajout message d'erreur json empty ?

    @classmethod
    def save_players(cls, players):
        with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
            json.dump([player.to_dict() for player in players], file, ensure_ascii=False, indent=4)
    @classmethod
    def load_tournaments(cls):
        tournaments = []
        try:
            with open(cls.TOURNAMENTS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                tournaments = [Tournament.from_dict(tournament_data) for tournament_data in data]
        except FileNotFoundError:
            print("Fichier de tournois non trouvé.")
        except json.JSONDecodeError:
            print("Erreur de décodage JSON.")
        return tournaments

    @classmethod
    def save_tournament(cls, tournaments):
        with open(cls.TOURNAMENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump([tournament.to_dict() for tournament in tournaments], file, ensure_ascii=False, indent=4)