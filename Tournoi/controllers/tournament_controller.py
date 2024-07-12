from models.tournament import Tournament
from models.database import Database
from controllers.player_controller import PlayerController
from views.player_view import PlayerView
from views.tournament_view import TournamentView

class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.database = Database()
        self.player_view = PlayerView()
        self.player_controller = PlayerController()

    def create_tournament(self):
        name, location, start_date, end_date, description = self.tournament_view.get_tournament_details()
        number_of_rounds = self.tournament_view.get_round_count()
        number_of_players = self.tournament_view.get_player_count()
        tournament = Tournament(name, location, start_date, end_date, number_of_rounds, description, number_of_players)
        self.manage_tournament(tournament)

    def manage_tournament(self, tournament):
        while True:
            choice = self.tournament_view.show_tournament_menu()
            if choice == '1':
                players = self.database.load_players()
                self.player_view.display_players(players)
                selected_player = self.player_controller.select_player(players)
                if selected_player:
                    tournament.add_selected_player(selected_player)
                else:
                    print("Aucun joueur sélectionné.")
            elif choice == '2':
                last_name, first_name, date_of_birth, national_id = self.player_view.get_player_details()
                self.player_controller.create_player(last_name, first_name, date_of_birth, national_id)
                print("Joueur ajouté avec succès !")
            elif choice == '3':
                tournament.display_tournament_details()
                tournaments = self.database.load_tournaments()
                tournaments.append(tournament)
                self.database.save_tournament(tournaments)
                tournament.run_tournament()
                tournament.display_final_scores()
                break
            elif choice == '4':
                break
            else:
                print("Option invalide. Veuillez réessayer.")