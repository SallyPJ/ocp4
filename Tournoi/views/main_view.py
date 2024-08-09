class MainView:
    def display_main_menu(self):
        # Display main menu
        print("Menu principal:")
        print("1. Enregister un nouveau joueur")
        print("2. Afficher la liste des joueurs enregistrés")
        print("3. Créer un tournoi")
        print("4. Quitter")
        return input("Choisir une option: ")

    def get_player_details(self):
        # Get player details
        print("Register a new player:")
        from views.player_view import PlayerView
        player_view = PlayerView()
        return player_view.get_player_details()

    def display_players(self, players):
        # Display list of players
        print("Liste des joueurs enregistrés:")
        for player in players:
            print(player)



