class ReportView:
    """
    ReportView is responsible for displaying the menu and options related to reporting functionalities
    within the application. This includes generating and displaying various reports for tournaments.
    """
    def display_reports_main_menu(self):
        print("==========================================")
        print("           [ Menu des rapports ]")
        print("==========================================")
        print("1. Vue d'Ensemble des Tournois (HTML)")
        print("2. Retour au menu principal")
        return input("Choisir une option: ")
