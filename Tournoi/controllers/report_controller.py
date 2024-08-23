from views.report_view import ReportView
from controllers.player_controller import PlayerController
from views.player_view import PlayerView
from models.database import Database
from views.tournament_view import TournamentView
from controllers.tournament_controller import TournamentController
from jinja2 import Environment, FileSystemLoader
import os
import webbrowser


class ReportController:

    def __init__(self):
        # Initialize view and database
        self.report_view = ReportView()
        self.player_controller = PlayerController()
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.database = Database()
        self.tournament_controller = TournamentController()



    def manage_reports(self):
        while True:
            choice = self.report_view.show_reports_main_menu()
            if choice == '1':
                # Display registered players by alphabetical order
                loaded_players = self.database.load_players()
                players = sorted(loaded_players)  # Le tri utilise la méthode __lt__ de la classe Player
                self.player_view.display_players_list(players)
            elif choice == '2':
                # Display tournaments list
                tournaments = self.database.load_tournaments()
                uuid_index_map = self.tournament_view.display_tournaments_list(tournaments)
                user_input = self.tournament_view.get_tournament_selection()
                selected_tournaments = self.tournament_controller.process_tournament_choices(user_input, tournaments, uuid_index_map)
                for tournament in selected_tournaments:
                    self.tournament_view.display_all_tournament_details(tournament)

            elif choice == '3':
                tournaments = self.database.load_tournaments()
                self.generate_html_report(tournaments)

                # Display the list of all tournaments
                break
            elif choice == '4':
                # Exit application
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def generate_html_report(self, tournaments, output_file='tournament_report.html'):
        """
        Génère un rapport HTML des tournois avec un sommaire cliquable en utilisant un template Jinja2.

        Args:
            tournaments (list): Liste d'objets tournoi à inclure dans le rapport.
            output_file (str): Chemin du fichier de sortie HTML.
        """
        # Configuration de Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('tournaments_report_template.html')

        # Rendre le template avec les données des tournois
        html_output = template.render(tournaments=tournaments)

        # Écrire le résultat dans un fichier
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)

        # Ouvrir le fichier HTML dans le navigateur par défaut
        file_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{file_path}')
        print(f"Rapport généré avec succès : {output_file}")