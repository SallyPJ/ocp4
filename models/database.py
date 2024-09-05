import json
import os

from models.player import Player
from models.tournament import Tournament


class Database:
    """
    The Database class provides methods for persisting and
    retrieving data related to players and tournaments.
    It uses JSON files to store the data and provides an interface
    for loading and saving data in these files.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PLAYERS_FILE = os.path.join(BASE_DIR, "data", "players.json")
    TOURNAMENTS_FILE = os.path.join(BASE_DIR, "data", "tournaments.json")

    @classmethod
    def check_for_data_directory(cls):
        if not os.path.exists(os.path.dirname(cls.PLAYERS_FILE)):
            os.makedirs(os.path.dirname(cls.PLAYERS_FILE))

    @classmethod
    def load_players(cls):
        """
        Load players from the JSON file.

        If the data repertory does not exist, it creates it.
        If the players file does not exist, it initializes an
        empty file and returns an empty list.
        Otherwise, it reads the data from the file, converts it into Player objects,
        and returns a list of these players.

        Returns:
            list[Player]: A list of Player objects.
       """
        cls.check_for_data_directory()
        if not os.path.exists(cls.PLAYERS_FILE):
            with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []
        with open(cls.PLAYERS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Player.from_dict(player) for player in data]

    @classmethod
    def save_players(cls, players):
        """
        Save a list of players to the JSON file.

        The method converts the Player objects into dictionaries
        and writes them to the file in JSON format.

        Args:
            players (list[Player]): A list of Player objects to save.
        """
        with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
            json.dump([player.to_dict() for player in players],
                      file, ensure_ascii=False, indent=4)

    @classmethod
    def load_tournaments(cls):
        """
        Load tournaments from the JSON file.

        If the data repertory does not exist, it creates it.
        This method reads the tournament data from the file, converts it into
        Tournament objects, and returns a list of these tournaments.
        If the file does not exist or if there's an error during the loading process,
        it returns an empty list.

        Returns:
            list[Tournament]: A list of Tournament objects.
        """
        cls.check_for_data_directory()
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
        """
        Save a list of tournaments to the JSON file.

        The method converts the Tournament objects into dictionaries
        and writes them to the file in JSON format.

        Args:
            tournaments (list[Tournament]): A list of Tournament objects to save.
        """
        cls.check_for_data_directory()
        with open(cls.TOURNAMENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump([tournament.to_dict() for tournament in tournaments],
                      file, ensure_ascii=False, indent=4)

    @classmethod
    def save_tournament_update(cls, tournament):
        """
        Update an existing tournament in the JSON file.

        The method loads all tournaments, finds the one with the matching reference,
        updates it, and saves the updated list back to the file.
        If the tournament is not found, a ValueError is raised.

        Args:
            tournament (Tournament): The Tournament object to update.

        Raises:
            ValueError: If the tournament with the specified reference is not found.
            """
        tournaments = cls.load_tournaments()
        for i, existing_tournament in enumerate(tournaments):
            if existing_tournament.reference == tournament.reference:
                tournaments[i] = tournament
                cls.save_tournament(tournaments)
                return
        raise ValueError(
            f"Le tournoi avec la référence {tournament.reference} "
            f"n'a pas été trouvé et donc pas mis à jour.")
