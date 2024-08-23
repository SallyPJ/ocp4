from models.tournament import Tournament
from models.database import Database
from models.round import Round
from controllers.player_controller import PlayerController
from views.tournament_view import TournamentView
from views.player_view import PlayerView
from utils import date_utils

class TournamentController:
    def __init__(self):
        # Initialize view, database, and player controller
        self.tournament_view = TournamentView()
        self.database = Database()
        self.player_controller = PlayerController()
        self.player_view = PlayerView()


    def create_tournament(self):
        # Create a new tournament
        details = self.tournament_view.get_tournament_details()
        number_of_rounds = self.tournament_view.get_round_count()
        number_of_players = self.player_view.get_player_count()
        tournament = Tournament(*details, number_of_rounds, number_of_players)
        self.manage_tournament(tournament)

    def manage_tournament(self, tournament):
        # Manage the tournament lifecycle
        while True:
            choice = self.tournament_view.show_tournament_menu(tournament)
            if choice == '1':
                # Select players for the tournament
                loaded_players = self.database.load_players()
                players = sorted(loaded_players)  # Le tri utilise la méthode __lt__ de la classe Player
                selected_players = self.select_multiple_players(players, tournament)
                if selected_players:
                    tournament.selected_players.extend(selected_players)
                    self.tournament_view.display_message("Joueurs ajoutés avec succès.")
                else:
                    self.tournament_view.display_message("Aucun joueur sélectionné.")
            elif choice == '2':
                # Start the tournament
                if self.check_players_count(tournament):
                    self.tournament_view.display_tournament_details(tournament)
                    tournaments = self.database.load_tournaments()
                    tournaments.append(tournament)
                    self.database.save_tournament(tournaments)
                    self.run_tournament(tournament)
                    self.tournament_view.display_final_scores(tournament)
                    self.tournament_view.get_tournament_feedbacks(tournament)
                    self.database.update_tournament(tournament)
                    break
                else:
                    self.tournament_view.display_message(f"Nombre incorrect de joueurs sélectionnés.\n"
                                                         f"Joueurs enregistrés : {len(tournament.selected_players)}, Joueurs attendus : {tournament.number_of_players}.\n"
                                                         f"Réinitialisation des joueurs effectuée.\n")
                    tournament.selected_players.clear()
            elif choice == '3':
                # Exit tournament management
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def select_multiple_players(self, players, tournament):
        # Select multiple players for the tournament
        while True:
            self.player_view.display_players_list(players)
            player_choices = self.tournament_view.select_players_input()
            selected_players = self.process_player_choices(player_choices, players)

            if selected_players:
                self.tournament_view.display_selected_players(selected_players)
                confirmation = self.tournament_view.confirm_selection()
                if confirmation.lower() == 'o':
                    return selected_players
                else:
                    self.tournament_view.display_message("Sélection des joueurs réinitialisée.")
            else:
                self.tournament_view.display_message("Sélection invalide. Veuillez réessayer.")

    def process_player_choices(self, choices, players):
        # Process player choices based on user input
        try:
            indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
            return [players[idx] for idx in indices if 0 <= idx < len(players)]
        except ValueError:
            self.tournament_view.display_message("Entrée invalide. Veuillez entrer des numéros valides.")
            return []



    def process_tournament_choices(self, user_input,tournaments, uuid_index_map):
        """
        Traite les choix de tournois basés sur l'entrée utilisateur.
        """
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]

            # Trouver les UUID correspondant aux indices
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices if 0 <= idx < len(tournaments)}

            # Trouver les tournois correspondant aux UUID sélectionnés
            selected_tournaments = [tournament for tournament in tournaments
                                    if tournament.reference in selected_uuids]
            if not selected_tournaments:
                self.tournament_view.display_message("Aucun tournoi sélectionné.")
            return selected_tournaments
        except ValueError:
            self.tournament_view.display_message("Entrée invalide. Veuillez entrer des numéros valides.")
            return []

    def run_tournament(self,tournament, round):
        from models.database import Database

        # Run the tournament rounds
        for i in range(tournament.number_of_rounds):
            is_first_round = (i == 0)  # Vérifie si c'est le premier tour
            # Enregistrer le start_time au début du round
            start_time = date_utils.get_current_datetime()
            round = Round(tournament, round_number=i + 1, is_first_round=is_first_round)
            round.start_time = start_time
            round.play_round()
            end_time = date_utils.get_current_datetime()
            round.end_time = end_time
            self.process_round_results(tournament,round)
            tournament.rounds.append(round)
            #self.rounds.append(round)  # Ajouter le round au tournoi
            Database.update_tournament(self)

    def check_players_count(self, tournament):
        return len(tournament.selected_players) == tournament.number_of_players

    def process_round_results(self, tournament, round):
        results = round.get_results()
        for match_result in results:
            if isinstance(match_result, dict) and len(match_result) == 2:
                # Assurez-vous que match_result est un dictionnaire avec exactement deux éléments
                player1_name, score1 = list(match_result.items())[0]
                player2_name, score2 = list(match_result.items())[1]

                # Trouvez les objets Player correspondant aux noms
                player1 = next(player for player in tournament.selected_players if player.first_name == player1_name)
                player2 = next(player for player in tournament.selected_players if player.first_name == player2_name)

                # Mettre à jour les points
                player1.total_points += score1
                player2.total_points += score2

                # Ajouter les adversaires aux listes correspondantes
                player1.opponents.append(player2_name)
                player2.opponents.append(player1_name)
            else:
                print(f"Unexpected match result format: {match_result}")