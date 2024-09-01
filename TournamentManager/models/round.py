import random
from models.match import Match

class Round:
    def __init__(self, tournament, round_number, matches=None, is_first_round=False, start_time=None, end_time=None):
        self.players = tournament.selected_players
        self.pairs = []
        self.round_number = round_number
        self.matches = matches if matches is not None else []
        self.is_first_round = is_first_round
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "round_number": self.round_number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data, tournament):
        matches = [Match.from_dict(match_data) for match_data in data["matches"]]
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        return cls(tournament, data["round_number"], matches, start_time=start_time, end_time=end_time)

    def create_pairs(self):
        if self.is_first_round:
            self.create_random_pairs()
        else:
            self.create_pairs_based_on_points()

    def create_random_pairs(self):
        random.shuffle(self.players)
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                self.pairs.append(Match(self.players[i], self.players[i + 1], self.round_number))

    def create_pairs_based_on_points(self):
        self.players.sort(key=lambda player: player.total_points, reverse=True)

        grouped_players = {}
        for player in self.players:
            points = player.total_points
            if points not in grouped_players:
                grouped_players[points] = []
            grouped_players[points].append(player)

        for points, players in grouped_players.items():
            random.shuffle(players)

        self.players = [player for group in grouped_players.values() for player in group]

        available_players = self.players[:]
        while len(available_players) >= 2:
            player1 = available_players.pop(0)
            paired = False
            for i, player2 in enumerate(available_players):
                if not player1.has_played_against(player2):
                    match = Match(player1, player2, self.round_number)
                    self.pairs.append(match)
                    player1.add_opponent(player2)
                    player2.add_opponent(player1)
                    available_players.pop(i)
                    paired = True
                    break
            if not paired:
                player2 = available_players.pop(0)
                match = Match(player1, player2, self.round_number)
                self.pairs.append(match)
                player1.add_opponent(player2)
                player2.add_opponent(player1)