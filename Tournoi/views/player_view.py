class PlayerView :

    def get_player_details(self):
        last_name = input("Nom de famille : ")
        first_name = input("Prénom : ")
        date_of_birth = input("Date de naissance (AAAA-MM-JJ) : ")
        national_id = input("Identifiant : ")
        return last_name, first_name, date_of_birth, national_id

    def display_players(self, players):
        print("Liste des joueurs :")
        for i, player in enumerate(players, start=1):
            print(f"{i}. Nom de famille: Nom de famille: {player.last_name}, Prénom: {player.first_name}, Date de naissance: {player.date_of_birth}, Identifiant: {player.national_id}")

    def select_player_input(self):
        try:
            choice = int(input("Entrez le numéro du joueur que vous souhaitez sélectionner : "))
            return choice
        except ValueError:
            return None

    def display_selected_player(self, selected_player):
        if selected_player:
            print(f"Vous avez sélectionné le joueur : {selected_player.last_name} {selected_player.first_name}")
        else:
            print("Numéro de joueur invalide.")


