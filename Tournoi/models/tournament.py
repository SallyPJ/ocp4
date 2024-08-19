import uuid
from models.round import Round
from models.player import Player



class Tournament:
    def __init__(self, name: str, location: str, start_date: str, end_date: str, number_of_rounds: int,
                 number_of_players: int, description=None):
        self.reference = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.number_of_players = number_of_players
        self.description = description
        self.selected_players = []
        self.rounds = []


    def check_players_count(self) :
        return len(self.selected_players) == self.number_of_players

    def display_tournament_details(self):
        # Display tournament details
        print(f"Tournoi: {self.name}, Lieu: {self.location}, Dates: {self.start_date} - {self.end_date}")

    def run_tournament(self):
        # Run the tournament rounds
        for i in range(self.number_of_rounds):
            is_first_round = (i == 0)  # Vérifie si c'est le premier tour
            round = Round(self, round_number=i + 1, is_first_round=is_first_round)
            round.play_round()
            self.process_round_results(round)
            #self.rounds.append(round)  # Ajouter le round au tournoi





    def process_round_results(self, round):
        results = round.get_results()
        for match_result in results:
            if isinstance(match_result, dict) and len(match_result) == 2:
                # Assurez-vous que match_result est un dictionnaire avec exactement deux éléments
                player1_name, score1 = list(match_result.items())[0]
                player2_name, score2 = list(match_result.items())[1]

                # Trouvez les objets Player correspondant aux noms
                player1 = next(player for player in self.selected_players if player.first_name == player1_name)
                player2 = next(player for player in self.selected_players if player.first_name == player2_name)

                # Mettre à jour les points
                player1.total_points += score1
                player2.total_points += score2

                # Ajouter les adversaires aux listes correspondantes
                player1.opponents.append(player2_name)
                player2.opponents.append(player1_name)
            else:
                print(f"Unexpected match result format: {match_result}")
    def display_final_scores(self):
        # Display final scores of players
        print("Scores finaux:")
        for player in self.selected_players:
            print(f"{player.first_name}: {player.total_points}")

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
            "selected_players": [player.to_dict() for player in self.selected_players],  # Convert players to dict
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
            data.get("description", "")
            )
        tournament.reference = data.get("reference", str(uuid.uuid4()))
        tournament.selected_players = [Player.from_dict(player_data) for player_data in data.get("selected_players", [])]
        tournament.rounds = [Round.from_dict(round_data,tournament) for round_data in data.get("rounds", [])]
        return tournament


