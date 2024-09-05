class MainView:
    """
        MainView is responsible for displaying the main menu
        to the user and capturing the user's selection.

    """
    def display_main_menu(self):
        """
        Display the main menu to the user.

        This method prints the main menu options to the console
        and prompts the user to choose an option.
        The menu includes options for managing players,
        tournaments, data, or exiting the application.

        Returns:
            str: The user's input, which corresponds to the menu option they selected.
        """
        print("==========================================")
        print("           [ Menu Principal ]")
        print("==========================================")
        print("1. Gestion des Joueurs")
        print("2. Gestion des Tournois")
        print("3. Gestion des Données")
        print("4. Quitter")
        print("==========================================")
        return input("Choisir une option: ")
