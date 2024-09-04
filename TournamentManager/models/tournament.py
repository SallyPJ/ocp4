import uuid
from models.round import Round
from models.player import Player


class Tournament:
    def __init__(self, name: str, location: str, start_date: str,
                 end_date: str, number_of_rounds: int,
                 number_of_players: int, description=None,
                 rounds_completed=False, in_progress=False):
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
        # Convert Tournament object to dictionary
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
            # Convert players to dict
            "selected_players": [player.to_dict() for player
                                 in self.selected_players],
            "rounds": [round.to_dict() for round in self.rounds]
        }

    @classmethod
    def from_dict(cls, data):
        # Create Tournament object from dictionary, can return default value
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
