from views.base_view import BaseView


class ReportView(BaseView):
    """
    The ReportView class is responsible for displaying the menu and options
    related to reporting functionalities within the application. This includes
    generating and displaying various reports for tournaments.

    Inherits from:
        BaseView: This class extends `BaseView`, and can reuse some basic methods
        for displaying messages.
    """

    def display_reports_main_menu(self):
        """
        Displays the main report menu, allowing the user to choose between generating
        a tournament HTML report or returning to the main menu.

        Returns:
            str: The option chosen by the user.
        """
        print("==========================================")
        print("           [ Menu des rapports ]")
        print("==========================================")
        print("1. Vue d'Ensemble des Tournois (HTML)")
        print("2. Retour au menu principal")
        return input("Choisir une option: ")

    def display_feedback(self, message_type, error_message=None):
        """
        Displays feedback messages to the user based on the provided message type.
        Handles specific error messages related to report generation or file access.

        Args:
            message_type (str): The type of message to display.
            error_message (str, optional): The error message to display.

        Returns:
            None
        """
        if message_type == "no_tournament":
            print("Aucun tournoi n'a été trouvé.")
        elif message_type == "file_not_found_error" and error_message is not None:
            print(f"Le fichier n'a pas été trouvé : {error_message}.")
        elif message_type == "io_error" and error_message is not None:
            print(f"Erreur d'accès à la base de données : {error_message}.")
        elif message_type == "report_success":
            print("Rapport généré avec succès")
        elif message_type == "report_generation_error" and error_message is not None:
            print(f"Erreur lors de la génération du rapport: {error_message}")
        elif message_type == "report_browser_error" and error_message is not None:
            print(f"Erreur lors de l'ouverture du rapport dans le navigateur: {error_message}")
        else:
            super().display_feedback(message_type)
