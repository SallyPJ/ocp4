import random
from models.match import Match


class Round:
    def __init__(self, tournament, round_number, matches=None,
                 is_first_round=False, start_time=None, end_time=None):
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
        matches = [Match.from_dict(match_data) for match_data
                   in data["matches"]]
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        round_instance = cls(tournament, data["round_number"], matches,
                             start_time=start_time, end_time=end_time)

        # Si les paires existent déjà, elles doivent être restaurées
        if "pairs" in data:
            round_instance.pairs = [Match.from_dict(match_data) for match_data in data["pairs"]]

        # Mettre à jour les total_points des joueurs
        for match in round_instance.matches:
            for player, score in match.match:
                # Trouver le joueur dans le tournoi et récupérer ses total_points
                player_in_tournament = next((p for p in tournament.selected_players if p.id == player.id), None)
                if player_in_tournament:
                    player.total_points = player_in_tournament.total_points  # Mise à jour du score à partir du tournoi

        return round_instance

    def create_pairs(self):
        if self.is_first_round:
            self.create_random_pairs()
        else:
            self.create_pairs_based_on_points()

    def create_random_pairs(self):
        random.shuffle(self.players)
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                self.pairs.append(Match(self.players[i],
                                        self.players[i + 1], self.round_number))

    def create_pairs_based_on_points(self):
        # Sort players by total points in descending order
        self.players.sort(key=lambda player: player.total_points,
                          reverse=True)

        # Group players by total points
        grouped_players = {}
        for player in self.players:
            points = player.total_points
            if points not in grouped_players:
                grouped_players[points] = []
            grouped_players[points].append(player)

        # Prepare the list of pairs
        self.pairs = []

        # Pair players with similar points
        available_players = self.players[:]
        while len(available_players) >= 2:
            player1 = available_players.pop(0)

            # Get a list of players with the same or
            # close points (up to one group lower if needed)
            possible_opponents = (
                self.get_possible_opponents(player1,
                                            grouped_players, available_players))

            # Find the best opponent among the possible ones
            player2 = self.find_best_opponent(player1, possible_opponents)
            if player2:
                match = Match(player1, player2, self.round_number)
                self.pairs.append(match)
                player1.add_opponent(player2)
                player2.add_opponent(player1)
                available_players.remove(player2)
            else:
                raise Exception("Aucun adversaire trouvé")

    def get_possible_opponents(self, player1, grouped_players, available_players):
        # Get the total points of player1
        player1_points = player1.total_points

        # Start with players with the same points
        possible_opponents = grouped_players.get(player1_points, [])
        possible_opponents = [player for player in possible_opponents
                              if player in available_players]

        # If enough opponents exist in the same group, don't look further
        if len(possible_opponents) >= 2:
            return possible_opponents

        # Iteratively consider players in the next lower groups if not enough opponents
        current_points = player1_points
        while len(possible_opponents) < 2:
            next_lower_points = self.get_next_lower_points(grouped_players,
                                                           current_points)
            if next_lower_points is None:
                break  # No more lower groups available
            possible_opponents.extend(
                [player for player in grouped_players[next_lower_points]
                 if player in available_players]
            )
            current_points = next_lower_points

        return possible_opponents

    def get_next_lower_points(self, grouped_players, current_points):
        """Find the next lower group of points available after the current points."""
        sorted_points = sorted(grouped_players.keys(), reverse=True)
        current_index = sorted_points.index(current_points)
        if current_index + 1 < len(sorted_points):
            return sorted_points[current_index + 1]
        return None

    def find_best_opponent(self, player1, possible_opponents):
        """Find the best opponent for player1 who has not played against them."""
        for player2 in possible_opponents:
            if not player1.has_played_against(player2):
                return player2
        # If all possible opponents have played against player1,
        # return the one with the fewest encounters
        min_encounters = min(player1.opponents.count(player2) for
                             player2 in possible_opponents)

        # Filter the opponents to those with the minimum number of encounters
        best_candidates = [player2 for player2 in possible_opponents if
                           player1.opponents.count(player2) == min_encounters]

        # Select randomly among the best candidates
        return random.choice(best_candidates)
