class MainView:
    def display_main_menu(self):
        print("1. Créer un nouveau joueur")
        print("2. Afficher la liste des joueurs enregistrés")
        print("3. Créer un tournoi")
        print("4. Quitter")
        choice = input("Choisissez une option : ")
        return choice


    def display_message(self, message):
        print(message)



