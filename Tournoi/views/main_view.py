class MainView:
    def display_main_menu(self):
        # Display main menu
        print("==========================================")
        print("           [ Menu Principal ]")
        print("==========================================")
        print("1. Enregistrer un Nouveau Joueur")
        print("2. Créer un Tournoi")
        print("3. Gestion des Données")
        print("4. Quitter")
        print("==========================================")
        return input("Choisir une option: ")

    def get_player_details(self):
        # Get player details
        print("Enregistrer un nouveau joueur:")
        from views.player_view import PlayerView
        player_view = PlayerView()
        return player_view.get_player_details()





