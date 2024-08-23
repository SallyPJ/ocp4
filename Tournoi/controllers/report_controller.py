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

          The function repeatedly prompts the user for input until a valid choice is made.

          Parameters:
          None

          Returns:
          None
          """
        while True:
            choice = self.report_view.show_reports_main_menu() # Show the reports menu and get the user's choice
            if choice == '1':
                # Display registered players by alphabetical order
                loaded_players = self.database.load_players()  # Load players from the database
                players = sorted(loaded_players)  # Sort players alphabetically (last name)
                self.player_view.display_players_list(players) # Display the sorted list of players

            elif choice == '2':
                # Display a list of tournaments
                tournaments = self.database.load_tournaments()  # Load tournaments from the database
                uuid_index_map = self.tournament_view.display_tournaments_list(tournaments)  # Display tournament list
                user_input = self.tournament_view.get_tournament_selection()  # Get user selection
                selected_tournaments = self.tournament_controller.process_tournament_choices(
                    user_input, tournaments, uuid_index_map)  # Process the user's tournament choices
                for tournament in selected_tournaments:
                    # Display details of selected tournaments
                    self.tournament_view.display_all_tournament_details(tournament)

            elif choice == '3':
                # Generate and display an HTML report of all tournaments
                tournaments = self.database.load_tournaments()  # Load tournaments
                self.generate_html_report(tournaments)  # Generate the report
                break

            elif choice == '4':
                # Exit reporting menu et open Main Menu
                break

            else:
                print("Option invalide. Veuillez réessayer.")

    def generate_html_report(self, tournaments, output_file='tournament_report.html'):
        """
        Generate an HTML report for tournaments using a Jinja2 template and save it to a file.

        Args:
            tournaments (list): List of tournament objects to include in the report.
            output_file (str): Path to the output HTML file.
        """
        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('tournaments_report_template.html')

        # Render the template with tournament data
        html_output = template.render(tournaments=tournaments)

        # Write the rendered HTML to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)

        # Open the generated HTML file in the default web browser
        file_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{file_path}')
        print(f"Rapport généré avec succès : {output_file}")