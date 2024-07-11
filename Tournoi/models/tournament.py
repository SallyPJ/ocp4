import uuid
from models.player import Player
from models.round import Round

class Tournament:
    def __init__(self, name, location, start_date,end_date, number_of_rounds, description, number_of_players):
        self.reference = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.number_of_players = number_of_players
        self.selected_players = []
        self.rounds = []

    def to_dict(self):
        selected_players_dict = [player.to_dict() for player in self.selected_players]
        # Convertit un objet tournament en dictionnaire pour faciliter la sérialisation JSON
        return {
            "reference": self.reference,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "number_of_players": self.number_of_players,
            "selected_players": selected_players_dict
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data["number_of_rounds"],
            data["description"],
            data["number_of_players"]
        )
        tournament.selected_players = [Player.from_dict(player) for player in data.get("selected_players", [])]
        return tournament

    def display_tournament_details(self):
        print("Détails du tournoi créé :")
        print(f"Référence : {self.reference}")
        print(f"Nom : {self.name}")
        print(f"Lieu : {self.location}")
        print(f"Date de début : {self.start_date}")
        print(f"Date de fin : {self.end_date}")
        print(f"Nombre de tours : {self.number_of_rounds}")
        print(f"Description : {self.description}")
        print(f"Nombre de joueurs : {self.number_of_players}")
        print(f"Joueurs sélectionnés :")
        for player in self.selected_players:
            print(player)

    def add_selected_player(self,selected_player):
        self.selected_players.append(selected_player)

    def remove_player(self, player):
        self.selected_players.remove(player)

    def run_tournament(self):
        for round_num in range(1, self.number_of_rounds + 1):
            print(f"Round {round_num}:")
            round_obj = Round(self)
            round_obj.play_first_round()
            round_obj.update_scores()
            self.rounds.append(round_obj)

    def display_final_scores(self):
        print("Scores finaux:")
        for player in self.selected_players:
            print(f"{player.first_name} {player.last_name} : {player.total_points} points")