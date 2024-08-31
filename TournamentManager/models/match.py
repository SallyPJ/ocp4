from models.player import Player
class Match:
    def __init__(self, player1, player2, round_number, finished=False, in_progress=False):
        self.players = [player1, player2]
        self.round_number = round_number
        self.results = {player1.first_name: 0, player2.first_name: 0}
        self.finished = finished
        self.in_progress = in_progress

    def to_dict(self):
        return {
            "players": [
                {"id": player.id, "last_name": player.last_name, "first_name": player.first_name}
                for player in self.players
            ],
            "results": {player.first_name: self.results.get(player.first_name, 0) for player in self.players},
            "finished": self.finished,
            "in_progress": self.in_progress
        }

    @classmethod
    def from_dict(cls, data):
        # Extraire les joueurs à partir des données
        players = [Player.from_dict(player_data) for player_data in data["players"]]

        # Extraire le numéro de round en utilisant get pour éviter KeyError
        round_number = data.get("round_number", 1)  # Assumer le round 1 par défaut si non spécifié

        # Créer une instance de Match avec les données fournies ou des valeurs par défaut
        match = cls(players[0], players[1], round_number)
        match.results = data.get("results", {players[0].first_name: 0, players[1].first_name: 0})
        match.finished = data.get("finished", False)
        match.in_progress = data.get("in_progress", False)

        return match

    def get_match_results(self):
        return self.results
