import uuid
import os
import json

from utils import date_utils
from models.round import Round
from models.player import Player


class Tournament:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TOURNAMENTS_FILE = os.path.join(BASE_DIR, "data", "tournaments.json")

    def __init__(self, name: str, location: str, start_date: str,
                 end_date: str, number_of_rounds: int,
                 number_of_players: int, description=None,
                 rounds_completed=False, in_progress=False):
        """
        Initializes a Tournament object with the given details.

        Args:
            name (str): The name of the tournament.
            location (str): The location where the tournament is held.
            start_date (str): The start date of the tournament.
            end_date (str): The end date of the tournament.
            number_of_rounds (int): The total number of rounds in the tournament.
            number_of_players (int): The number of players participating.
            description (str) A brief description of the tournament. Defaults to None.
            rounds_completed (bool, optional): Whether the tournament
            has finished. Defaults to False.
            in_progress (bool, optional): Whether the tournament is in progress.
            Defaults to False.

        Raises:
            ValueError: If number_of_rounds or number_of_players is negative.
        """
        self.reference = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.number_of_players = number_of_players
        self.description = description
        self.rounds_completed = rounds_completed
        self.in_progress = in_progress
        self.selected_players = []
        self.rounds = []

    def to_dict(self):
        """
        Converts the Tournament instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the tournament details,
            including players and rounds.
        """
        return {
            "reference": self.reference,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "number_of_players": self.number_of_players,
            "description": self.description,
            "rounds_completed": self.rounds_completed,
            "in_progress": self.in_progress,
            "selected_players": [player.to_dict() for player
                                 in self.selected_players],
            "rounds": [round.to_dict() for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Tournament object from a dictionary. This method also converts
        player and round data from dictionaries into their respective objects.

        Args:
            data (dict): A dictionary containing the tournament data.

        Returns:
            Tournament: A Tournament instance created from the provided dictionary.
        """
        tournament = cls(
            data.get("name", "Unknown"),
            data.get("location", "Unknown"),
            data.get("start_date", "Unknown"),
            data.get("end_date", "Unknown"),
            data.get("number_of_rounds", 0),
            data.get("number_of_players", 0),
            data.get("description", ""),
            data.get("rounds_completed", "False"),
            data.get("in_progress", "False")
        )
        tournament.reference = data.get("reference", str(uuid.uuid4()))
        tournament.selected_players = \
            [Player.from_dict(player_data) for player_data
             in data.get("selected_players", [])]
        tournament.rounds = [Round.from_dict(round_data, tournament)
                             for round_data in data.get("rounds", [])]
        return tournament

    @classmethod
    def create_tournament(cls, name, location, start_date, end_date,
                          number_of_rounds, number_of_players):
        """
        Creates a new Tournament instance.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date of the tournament.
            end_date (str): The end date of the tournament.
            number_of_rounds (int): Number of rounds.
            number_of_players (int): Number of players.

        Returns:
            Tournament: The created Tournament instance.
        """
        return cls(name, location, start_date, end_date, number_of_rounds,
                   number_of_players)

    @staticmethod
    def check_for_data_directory():
        """
        Ensures the data directory for storing tournaments exists.
        If the directory doesn't exist, it is created.
        """
        if not os.path.exists(os.path.dirname(Tournament.TOURNAMENTS_FILE)):
            os.makedirs(os.path.dirname(Tournament.TOURNAMENTS_FILE))

    @classmethod
    def load_tournaments(cls):
        """
        Loads the list of tournaments from the JSON file.

        Returns:
            list: A list of Tournament objects, or an empty list if no file is found.

        Exceptions:
            Handles FileNotFoundError and JSONDecodeError,
            returning an empty list on failure.
        """
        cls.check_for_data_directory()
        if not os.path.exists(cls.TOURNAMENTS_FILE):
            return []
        try:
            with open(cls.TOURNAMENTS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [cls.from_dict(tournament) for tournament in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement des tournois : {e}")
            return []

    @classmethod
    def save_tournament(cls, tournaments):
        """
        Saves the list of tournaments to the JSON file.

        Args:
            tournaments (list): A list of Tournament objects to be saved.

        The data directory is created if it does not exist.
        """
        cls.check_for_data_directory()
        with open(cls.TOURNAMENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump([tournament.to_dict() for tournament in tournaments], file,
                      ensure_ascii=False, indent=4)

    @classmethod
    def save_tournament_update(cls, updated_tournament):
        """
        Met à jour un tournoi existant dans le fichier JSON
        en fonction de la référence du tournoi.

        Args:
            updated_tournament (Tournament): Le tournoi à mettre à jour.

        Raises:
            ValueError: Si le tournoi avec la référence donnée n'est pas trouvé.
        """
        tournaments = cls.load_tournaments()
        for i, tournament in enumerate(tournaments):
            if tournament.reference == updated_tournament.reference:
                tournaments[i] = updated_tournament
                cls.save_tournament(tournaments)
                return
        raise ValueError(f"Le tournoi avec la référence "
                         f"{updated_tournament.reference} n'a pas été trouvé.")

    def assign_players(self, selected_players):
        """
        Adds the selected players to the tournament's list of participants.

        Args:
            selected_players (list): A list of Player objects to be added.
        """
        self.selected_players.extend(selected_players)

    def update_description(self, feedback):
        """
        Updates the tournament description with the user feedback.

        Args:
            feedback (str): The feedback to be added to the tournament description.
        """
        if feedback.strip():
            self.description = feedback

    def finalize_tournament(self):
        """
        Finalizes the tournament by marking it as no longer in progress.
        """
        self.in_progress = False

    def start_tournament(self):
        """
        Marks the tournament as in progress.
        """
        self.in_progress = True

    def create_round(self, round_number):
        """
        Creates and starts a new round for the tournament.

        Args:
            round_number (int): The round number to create.

        Returns:
            Round: The created round instance.
        """
        is_first_round = (round_number == 1)
        round_instance = Round(self, round_number=round_number,
                               is_first_round=is_first_round)
        round_instance.start_time = date_utils.get_current_datetime()
        self.rounds.append(round_instance)
        return round_instance

    def find_player_by_name(self, first_name, last_name):
        """
        Finds a player in the tournament by their first and last name.

        Args:
            first_name (str): The player's first name.
            last_name (str): The player's last name.

        Returns:
            Player: The found player object, or None if no match is found.
        """
        return next((player for player in self.selected_players
                     if player.first_name == first_name
                     and player.last_name == last_name), None)
