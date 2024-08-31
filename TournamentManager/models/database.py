import json
import os

from models.player import Player
from models.tournament import Tournament


class Database:
    PLAYERS_FILE = "players.json"
    TOURNAMENTS_FILE = "tournaments.json"

    @classmethod
    def load_players(cls):
        # Load players from JSON file
        if not os.path.exists(cls.PLAYERS_FILE):
            with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []
        with open(cls.PLAYERS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Player.from_dict(player) for player in data]

    @classmethod
    def save_players(cls, players):
        # Save players to JSON file
        with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
            json.dump([player.to_dict() for player in players], file, ensure_ascii=False, indent=4)

    @classmethod
    def load_tournaments(cls):
        # Load tournaments from JSON file
        if not os.path.exists(cls.TOURNAMENTS_FILE):
            return []
        try:
            with open(cls.TOURNAMENTS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Tournament.from_dict(tournament) for tournament in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement des tournois : {e}")
            return []

    @classmethod
    def save_tournament(cls, tournaments):
        # Save tournaments to JSON file
        with open(cls.TOURNAMENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump([tournament.to_dict() for tournament in tournaments], file, ensure_ascii=False, indent=4)

    @classmethod
    def save_tournament_update(cls, tournament):
        tournaments = cls.load_tournaments()

        # Rechercher et mettre à jour le tournoi dans la liste
        for i, existing_tournament in enumerate(tournaments):
            if existing_tournament.reference == tournament.reference:
                tournaments[i] = tournament
                cls.save_tournament(tournaments)
                return

        # Si aucun tournoi n'a été trouvé, lever une exception
        raise ValueError(
            f"Le tournoi avec la référence {tournament.reference} n'a pas été trouvé et donc pas mis à jour.")

