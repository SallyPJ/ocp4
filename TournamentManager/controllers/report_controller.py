from jinja2 import Environment, FileSystemLoader
import os
import webbrowser

from controllers.tournament_controller import TournamentController
from models.database import Database
from views.player_view import PlayerView
from views.report_view import ReportView
from views.tournament_view import TournamentView


class ReportController:

    def __init__(self):
        # Initialize view and database
        self.database = Database()
        self.tournament_controller = TournamentController()
        self.report_view = ReportView()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

    def manage_reports(self):
        """
        Manages the report generation process, allowing users to choose from different report options.
        This method repeatedly prompts the user for input until a valid choice is made.
        1. Generate en HTML report for all tournaments
        2. Exit reporting menu and open Main Menu
        """
        while True:
            choice = self.report_view.display_reports_main_menu()  # Show the reports menu and get the user's choice
            if choice == '1':
                self.handle_generate_html_report()
                break
            elif choice == '2':
                # Exit reporting menu et open Main Menu
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def handle_generate_html_report(self):
        """
        Handles the process of generating and displaying the HTML report for all tournaments.
        """
        try:
            tournaments = self.database.load_tournaments()  # Load tournaments
            self.generate_html_report(tournaments)  # Generate the report
            self.open_report_in_browser('tournament_report.html')  # Open the report in the web browser
        except Exception as e:
            print(f"Une erreur est survenue lors de la création du rapport: {str(e)}")

    def generate_html_report(self, tournaments, output_file='tournament_report.html'):
        """
        Generate an HTML report for tournaments using a Jinja2 template and save it to a file.

        Args:
            tournaments (list): List of tournament objects to include in the report.
            output_file (str): Path to the output HTML file.
        """
        try:
            # Set up Jinja2 environment
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'views', 'templates')
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('tournaments_report_template.html')

            # Render the template with tournament data
            html_output = template.render(tournaments=tournaments)

            # Write the rendered HTML to the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_output)

            print(f"Rapport généré avec succès: {output_file}")
        except Exception as e:
            print(f"Erreur lors de la génération du rapport: {str(e)}")

    def open_report_in_browser(self, output_file):
        """
        Opens the specified HTML report in the default web browser.

        Args:
            output_file (str): Path to the HTML file to open.
        """
        try:
            file_path = os.path.abspath(output_file)
            webbrowser.open(f'file://{file_path}')
        except Exception as e:
            print(f"Erreur lors de l'ouverture du rapport dans le navigateur: {str(e)}")

