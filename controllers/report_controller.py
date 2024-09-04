from jinja2 import Environment, FileSystemLoader
import os
import webbrowser

from controllers.tournament_controller import TournamentController
from models.database import Database
from views.player_view import PlayerView
from views.report_view import ReportView
from views.tournament_view import TournamentView


class ReportController:
    """
       The ReportController class manages the generation and display of reports within the application.

       It handles user interactions related to report generation, including creating HTML reports for tournaments
       and displaying them in the web browser. The controller interacts with the database to retrieve tournament data,
       and uses Jinja2 templates to format the reports.
    """
    def __init__(self):
        self.database = Database()
        self.tournament_controller = TournamentController()
        self.report_view = ReportView()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

    def run_report_menu(self):
        """
        Manages the report generation process, allowing users
        to choose from different report options.
        This method repeatedly prompts the user for input until
        a valid choice is made.
        1. Generate en HTML report for all tournaments
        2. Exit reporting menu and open Main Menu
        """
        while True:
            choice = self.report_view.display_reports_main_menu()
            if choice == '1':
                self.handle_generate_html_report()
                break
            elif choice == '2':
                break
            else:
                self.report_view.display_feedback("invalid_option")

    def handle_generate_html_report(self):
        """
        Handles the generation and display of an HTML report for all tournaments.
        This method loads the tournament data from the database, generates an HTML report using a Jinja2 template,
        and then opens the report in the default web browser.
        """
        try:
            tournaments = self.database.load_tournaments()
            if not tournaments:
                self.report_view.display_feedback("no_tournament")
                return
            self.generate_html_report(tournaments)
            self.open_report_in_browser('tournament_report.html')
        except FileNotFoundError as fnf_error:
            self.report_view.display_feedback("file_not_found_error", error_message=str(fnf_error))
        except IOError as io_error:
            self.report_view.display_feedback("io_error", error_message=str(io_error))

    def generate_html_report(self, tournaments, output_file='tournament_report.html'):
        """
        Generate an HTML report for tournaments using
        a Jinja2 template and save it to a file.

        Args:
            tournaments (list): List of tournament objects to include in the report.
            output_file (str): Path to the output HTML file.
        """
        try:
            template_dir = os.path.join(os.path.dirname(__file__),
                                        '..', 'views', 'templates')
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('tournaments_report_template.html')
            html_output = template.render(tournaments=tournaments)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_output)
            self.report_view.display_feedback("report_success")
        except Exception as e:
            self.report_view.display_feedback("report_generation_error",error_message=str(e))


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
            self.report_view.display_feedback("report_browser_error", error_message=str(e))


